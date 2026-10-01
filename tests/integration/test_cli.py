import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class CLITests(unittest.TestCase):
    def test_demo_cli_writes_review_package(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "demo"
            result = subprocess.run([sys.executable, "-m", "app.cli", "demo", "--out", str(output)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ["index.html", "report.html", "run.json", "manifest.json", "results.csv", "contributions.csv", "assumptions.csv"]:
                self.assertTrue((output / name).exists(), name)
            run = json.loads((output / "run.json").read_text())
            self.assertEqual(len(run["results"]), 5)
            report = (output / "report.html").read_text()
            self.assertIn("Synthetic demonstration", report)
            self.assertIn("Assumption ledger", report)

