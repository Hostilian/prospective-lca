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
