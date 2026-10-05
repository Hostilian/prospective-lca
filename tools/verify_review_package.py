"""Check calculation provenance and every fingerprint in a review package."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.domain.models import load_project
from app.services.engine import run_project
from app.services.manifests import build_manifest
from tools.review_diagnostics import review_diagnostics


def verify_calculation(project, run, manifest):
    selected = [s.id for s in project.scenarios]
    expected = run_project(project, mode="demo", selected_scenario_ids=selected)
    if run != expected:
        raise ValueError("Calculation export differs from the reproducible source model")
    expected_manifest = build_manifest(project, expected, selected)
    for key in ("run_uuid", "application_version", "project_id", "scenario_ids", "calculation_engine",
                "input_manifest_hash", "assumption_ledger_hash", "result_artifact_hash", "database", "validation"):
        if manifest.get(key) != expected_manifest[key]:
            raise ValueError(f"Calculation manifest mismatch: {key}")


def verify_package(package):
    project = load_project(ROOT / "demo/sample_project/project.json")
    run = json.loads((package / "run.json").read_text(encoding="utf-8"))
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    verify_calculation(project, run, manifest)
    preview = json.loads((package / "preview-manifest.json").read_text(encoding="utf-8"))
    display_hash = hashlib.sha256((ROOT / "demo/report_preview_data.json").read_bytes()).hexdigest()
    if preview["display_data_sha256"] != display_hash:
        raise ValueError("Supplied display dataset fingerprint mismatch")
    expected_paths = {"index.html", "customer/index.html", "reviewer/index.html"}
    if set(preview["html_sha256"]) != expected_paths:
        raise ValueError("Review HTML manifest has an unexpected artifact set")
    fingerprints = dict(preview["html_sha256"])
    fingerprints["review-diagnostics.json"] = preview["review_diagnostics_sha256"]
    for name, fingerprint in fingerprints.items():
        if hashlib.sha256((package / name).read_bytes()).hexdigest() != fingerprint:
            raise ValueError(f"Artifact fingerprint mismatch: {name}")
    diagnostics = json.loads((package / "review-diagnostics.json").read_text(encoding="utf-8"))
    if diagnostics != review_diagnostics(project):
        raise ValueError("Review diagnostics differ from the source model")
    return {"status": "passed", "scope": "synthetic calculation, display data, three HTML files and review diagnostics",
            "scientific_approval": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify_package(args.package), indent=2))
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f"Review package verification failed: {error}\n")
