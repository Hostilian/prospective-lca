"""Protect data provenance and offline output in both presentation variants."""

from decimal import Decimal
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from app.domain.models import load_project
from app.services.engine import run_project
from app.services.manifests import build_manifest
from tools.build_report_previews import build, decomposition, percent, sig3
from tools.review_diagnostics import review_diagnostics
from tools.verify_review_package import verify_package

ROOT = Path(__file__).resolve().parents[2]


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        for key in ("src", "srcset"):
            if key in attributes:
                self.resources.append(attributes[key])
        if tag == "link" and "href" in attributes:
            self.resources.append(attributes["href"])


class PreviewTests(unittest.TestCase):
    def test_credit_denominator_and_quantity_factor_interaction(self):
        project = load_project(ROOT / "demo/sample_project/project.json")
        diagnostics = review_diagnostics(project)
        base, central, _, _, ambitious = diagnostics["credit_stress"]
        # Independent fixed-data checks: subtract the signed credit in BOTH cases.
        self.assertAlmostEqual(base["zero_credit"], 176.4 + 45 + 14.4 + 2.88 + 0.00084)
        self.assertAlmostEqual(central["signed_credit"], -70 * 1.2 * 0.25)
        expected_change = (136.170756 / 238.68084 - 1) * 100
        self.assertAlmostEqual(central["zero_credit_change_percent"], expected_change)
        self.assertAlmostEqual(ambitious["zero_credit"], 64.40463)
        for row in diagnostics["order_check"]:
            self.assertAlmostEqual(row["quantity_first"] + row["factor_after_quantity"], row["combined"] - row["reference"])
            self.assertAlmostEqual(row["factor_first"] + row["quantity_after_factor"], row["combined"] - row["reference"])
        # Central electricity interaction: Δq × Δf = (420×0.82−420)×(0.24−0.42).
        self.assertAlmostEqual(diagnostics["order_check"][0]["interaction"], (420 * 0.82 - 420) * (0.24 - 0.42))

    def test_package_verification_rejects_modified_calculation_and_document(self):
        project = load_project(ROOT / "demo/sample_project/project.json")
        selected = [s.id for s in project.scenarios]
        run = run_project(project, mode="demo", selected_scenario_ids=selected)
        manifest = build_manifest(project, run, selected)
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            run_path = package / "run.json"
            manifest_path = package / "manifest.json"
            run_path.write_text(json.dumps(run), encoding="utf-8")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            build(package)
            self.assertEqual(verify_package(package)["status"], "passed")
            document = package / "reviewer/index.html"
            document.write_text(document.read_text(encoding="utf-8") + "altered", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Artifact fingerprint mismatch"):
                verify_package(package)
            build(package)
            manifest["result_artifact_hash"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manifest mismatch"):
                build(package)
            manifest_path.write_text(json.dumps(build_manifest(project, run, selected)), encoding="utf-8")
            run["results"][0]["impacts"]["climate_change_kg_co2e"] += 1
            run_path.write_text(json.dumps(run), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "differs from the reproducible source model"):
                build(package)

    def test_supplied_display_precision_is_preserved_and_discrepancy_disclosed(self):
        data = json.loads((ROOT / "demo/report_preview_data.json").read_text(encoding="utf-8"))
        self.assertEqual(data["scenarios"][3]["totals"][1], "1.800")
        self.assertEqual(data["scenarios"][4]["totals"][1], "0.8667")
        self.assertEqual(data["scenarios"][1]["supplied_percent"][0], "-47.93")
        self.assertEqual(f'{percent("115.2", "221.2"):.2f}', "-47.92")
        self.assertEqual(sig3("1.800"), "1.80")
        self.assertEqual(sig3("2363"), "2360")
        self.assertEqual(sig3("166.5"), "167")
        self.assertEqual(sum(Decimal(x["value"]) for x in data["baseline_climate_contributions"]), Decimal("221.18084"))

    def test_two_offline_previews_preserve_source_artifacts_and_reconcile_decomposition(self):
        project = load_project(ROOT / "demo/sample_project/project.json")
        selected = [s.id for s in project.scenarios]
        run = run_project(project, mode="demo", selected_scenario_ids=selected)
        manifest = build_manifest(project, run, selected)
        _, derived = decomposition(project, run)
        # An independent quantity/factor product reproduces the reported ordered split.
        for scenario, row in zip(project.scenarios[1:], derived):
            qty = {i.id: i.quantity for i in project.inventory}
            factors = {i.id: i.factors["climate_change_kg_co2e"] for i in project.inventory}
            for t in scenario.transformations:
                item, _ = t.target.split(":")
                if t.operation == "scale_quantity":
                    qty[item] *= t.value
            expected_mid = sum(qty[i.id] * i.factors["climate_change_kg_co2e"] for i in project.inventory)
            for t in scenario.transformations:
                item, category = t.target.split(":")
                if t.operation == "set_factor" and category == "climate_change_kg_co2e":
                    factors[item] = t.value
            expected_final = sum(qty[i.id] * factors[i.id] for i in project.inventory)
            self.assertAlmostEqual(row["quantity_only"], expected_mid)
            self.assertAlmostEqual(row["full"], expected_final)
            self.assertAlmostEqual(row["process_quantity_change"] + row["background_factor_change"], expected_final - row["baseline"])
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            (package / "run.json").write_text(json.dumps(run), encoding="utf-8")
            (package / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (package / "report.html").write_text("original source report", encoding="utf-8")
            before = (package / "run.json").read_bytes()
            build(package)
            self.assertEqual((package / "run.json").read_bytes(), before)
            self.assertEqual((package / "report.html").read_text(encoding="utf-8"), "original source report")
            preview_manifest = json.loads((package / "preview-manifest.json").read_text(encoding="utf-8"))
            for name in ["index.html", "customer/index.html", "reviewer/index.html"]:
                content = (package / name).read_text(encoding="utf-8")
                parser = ResourceParser()
                parser.feed(content)
                self.assertEqual(parser.resources, [])
                self.assertEqual(len(parser.ids), len(set(parser.ids)))
                self.assertNotIn("@import", content)
                self.assertNotIn("fetch(", content)
                self.assertLess(len(content.encode("utf-8")), 300_000)
                self.assertIn("not for scientific or external decision-making", content)
                self.assertIn("not an approved life-cycle impact assessment method", content)
                self.assertIn("Automated consistency checks only, not scientific verification", content)
                self.assertIn("-47.93%", content)
                self.assertIn("-47.92%", content)
                self.assertEqual(hashlib.sha256((package / name).read_bytes()).hexdigest(), preview_manifest["html_sha256"][name])
