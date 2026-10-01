import copy
import unittest
from pathlib import Path

from app.domain.models import load_project
from app.services.validation import validate_project


PROJECT = Path(__file__).resolve().parents[2] / "demo" / "sample_project" / "project.json"


class ValidationTests(unittest.TestCase):
    def test_demo_passes(self):
        project = load_project(PROJECT)
        report = validate_project(project, mode="demo")
        self.assertTrue(report.ok)

    def test_production_blocks_synthetic_and_proposed_choices(self):
        project = load_project(PROJECT)
        report = validate_project(project, mode="production")
        codes = {issue.code for issue in report.errors}
        self.assertIn("SYNTHETIC_PROJECT_BLOCKED", codes)
        self.assertIn("UNAPPROVED_CHOICE", codes)
        self.assertIn("UNAPPROVED_TRANSFORMATION", codes)

    def test_baseline_must_be_selected(self):
        project = load_project(PROJECT)
        report = validate_project(project, mode="demo", selected_scenario_ids=["central-2030"])
        self.assertIn("BASELINE_NOT_SELECTED", {issue.code for issue in report.errors})

    def test_temporal_mismatch_is_specific(self):
        project = load_project(PROJECT)
        project.scenarios[1].background_year = 2029
        report = validate_project(project, mode="demo", selected_scenario_ids=["baseline-2025", "central-2030"])
        self.assertIn("TEMPORAL_MISMATCH", {issue.code for issue in report.errors})

    def test_unknown_target_is_specific(self):
        project = load_project(PROJECT)
        project.scenarios[1].transformations[0].target = "not-a-flow:quantity"
        report = validate_project(project, mode="demo", selected_scenario_ids=["baseline-2025", "central-2030"])
        self.assertIn("UNKNOWN_TRANSFORMATION_TARGET", {issue.code for issue in report.errors})

