"""Command-line entry point for the workbench."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from app.adapters.openlca import OpenLCAAdapter
from app.domain.models import dump_json, load_project
from app.reporting.csv_export import write_csv_exports
from app.reporting.html_report import write_html_report
from app.services.engine import CalculationBlocked, run_project
from app.services.manifests import build_manifest, write_manifest
from app.services.validation import validate_project


def _default_project() -> Path:
    return Path(__file__).resolve().parents[1] / "demo" / "sample_project" / "project.json"


def _run(args: argparse.Namespace, *, command_name: str) -> int:
    project_path = Path(args.project)
    out_dir = Path(args.out)
    project = load_project(project_path)
    selected = [x.strip() for x in args.scenarios.split(",")] if getattr(args, "scenarios", None) else [x.id for x in project.scenarios]
    try:
        run_data = run_project(project, mode=args.mode, selected_scenario_ids=selected)
    except CalculationBlocked as exc:
        print("Calculation blocked by validation.", file=sys.stderr)
        for issue in exc.report.errors:
            print(f"- {issue.code}: {issue.message} ({issue.remediation})", file=sys.stderr)
        if args.json:
            print(__import__("json").dumps(exc.report.to_dict(), indent=2))
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(project, run_data, selected)
    dump_json(run_data, out_dir / "run.json")
    write_manifest(manifest, out_dir / "manifest.json")
    write_html_report(run_data["project"], run_data, manifest, out_dir / "report.html")
    write_html_report(run_data["project"], run_data, manifest, out_dir / "index.html")
    write_csv_exports(run_data, out_dir)
    print(f"{command_name} complete")
    print(f"Project: {project.name}")
    print(f"Scenarios: {', '.join(selected)}")
    print(f"Output: {out_dir.resolve()}")
    print(f"Run UUID: {manifest['run_uuid']}")
    print(f"Warnings: {len(run_data['validation']['issues']) - run_data['validation']['error_count']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="awam-lca", description="Local-first prospective-LCA workbench")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="Run the original synthetic demonstration")
    demo.add_argument("--project", default=str(_default_project()))
    demo.add_argument("--out", default="exports/demo")
    demo.add_argument("--scenarios", default=None)
    demo.add_argument("--mode", choices=["demo", "production"], default="demo")
    demo.add_argument("--json", action="store_true")
    demo.set_defaults(handler=lambda args: _run(args, command_name="Synthetic demo"))

    for name, help_text in [("run", "Run selected scenarios and export a review package"), ("export", "Run and export a review package")]:
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("--project", default=str(_default_project()))
        cmd.add_argument("--out", default="exports/run")
        cmd.add_argument("--scenarios", default=None)
        cmd.add_argument("--mode", choices=["demo", "production"], default="production" if name == "run" else "demo")
        cmd.add_argument("--json", action="store_true")
        cmd.set_defaults(handler=lambda args, name=name: _run(args, command_name=name.title()))

    validate = sub.add_parser("validate", help="Validate a project without running it")
    validate.add_argument("--project", default=str(_default_project()))
    validate.add_argument("--mode", choices=["demo", "production"], default="production")
    validate.add_argument("--scenarios", default=None)
    validate.add_argument("--json", action="store_true")

    probe = sub.add_parser("probe-openlca", help="Probe an approved local openLCA IPC endpoint")
    probe.add_argument("--endpoint", default="http://localhost:8080")

    serve = sub.add_parser("serve", help="Serve an exported report/dashboard locally")
    serve.add_argument("--dir", default="exports/demo")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        project = load_project(args.project)
        selected = [x.strip() for x in args.scenarios.split(",")] if args.scenarios else None
        report = validate_project(project, mode=args.mode, selected_scenario_ids=selected)
        if args.json:
            import json
            print(json.dumps(report.to_dict(), indent=2))
        else:
            print(f"Validation {'passed' if report.ok else 'blocked'}: {len(report.errors)} errors, {len(report.warnings)} warnings")
            for issue in report.issues:
                print(f"[{issue.severity}] {issue.code}: {issue.message} — {issue.remediation}")
        return 0 if report.ok else 2
    if args.command == "probe-openlca":
        result = OpenLCAAdapter(args.endpoint).probe()
        print(f"reachable={result.reachable} status={result.status} endpoint={result.endpoint}\n{result.message}")
        return 0 if result.reachable else 1
    if args.command == "serve":
        from app.ui.server import serve_directory
        serve_directory(args.dir, host=args.host, port=args.port)
        return 0
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())

