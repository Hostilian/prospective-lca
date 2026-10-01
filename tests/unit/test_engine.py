import copy
import unittest
from pathlib import Path

from app.domain.models import load_project
from app.services.engine import run_project
from app.services.hashing import sha256_json
from app.services.manifests import build_manifest


PROJECT = Path(__file__).resolve().parents[2] / "demo" / "sample_project" / "project.json"


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.project = load_project(PROJECT)
        self.scenarios = [x.id for x in self.project.scenarios]

    def test_all_scenarios_execute(self):
        run = run_project(self.project, mode="demo", selected_scenario_ids=self.scenarios)
        self.assertEqual(len(run["results"]), 5)
        self.assertEqual(len(run["comparisons"]), 4)
        self.assertIn("background", run["results"][0]["by_layer"])
        self.assertIn("foreground", run["results"][0]["by_layer"])

    def test_repeated_run_is_deterministic(self):
        first = run_project(self.project, mode="demo", selected_scenario_ids=self.scenarios)
        second = run_project(self.project, mode="demo", selected_scenario_ids=self.scenarios)
        self.assertEqual(sha256_json(first["results"]), sha256_json(second["results"]))
        manifest_a = build_manifest(self.project, first, self.scenarios)
        manifest_b = build_manifest(self.project, second, self.scenarios)
        self.assertEqual(manifest_a["run_uuid"], manifest_b["run_uuid"])
        self.assertEqual(manifest_a["result_artifact_hash"], manifest_b["result_artifact_hash"])

    def test_transform_change_changes_result(self):
        first = run_project(self.project, mode="demo", selected_scenario_ids=self.scenarios)
        self.project.scenarios[1].transformations[0].value = 0.5
        second = run_project(self.project, mode="demo", selected_scenario_ids=self.scenarios)
        self.assertNotEqual(sha256_json(first["results"]), sha256_json(second["results"]))

