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

    def test_set_quantity_converts_to_inventory_unit(self):
        transformation = self.project.scenarios[1].transformations[0]
        transformation.operation = "set_quantity"
        transformation.value = 3600
        transformation.unit = "MJ"
        run = run_project(self.project, mode="demo", selected_scenario_ids=["baseline-2025", "central-2030"])
        electricity = next(c for c in run["results"][1]["contributions"] if c["item_id"] == "electricity_grid")
        self.assertEqual(electricity["unit"], "kWh")
        self.assertEqual(electricity["quantity"], 1000)
        self.assertEqual(run["transformation_diffs"]["central-2030"][0]["after"], 1000)
        self.assertEqual(run["transformation_diffs"]["central-2030"][0]["result_unit"], "kWh")
