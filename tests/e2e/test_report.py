from pathlib import Path
import unittest

from app.domain.models import load_project
from app.reporting.html_report import render_report
from app.services.engine import run_project
from app.services.manifests import build_manifest


ROOT = Path(__file__).resolve().parents[2]


class ReportE2ETests(unittest.TestCase):
    def test_report_has_scope_scenarios_validation_and_accessible_chart(self):
        project = load_project(ROOT / "demo" / "sample_project" / "project.json")
        selected = [x.id for x in project.scenarios]
        run = run_project(project, mode="demo", selected_scenario_ids=selected)
        manifest = build_manifest(project, run, selected)
        html = render_report(run["project"], run, manifest)
        for marker in ["Study definition", "Scenario results", "Comparison to baseline", "Assumption ledger", "Validation", "Reproducibility", "role=\"img\"", "Synthetic demonstration"]:
            self.assertIn(marker, html)

