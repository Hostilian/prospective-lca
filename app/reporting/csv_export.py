"""CSV exports for scenario results and the assumption ledger."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def write_csv_exports(run_data: dict[str, Any], output_dir: str | Path) -> list[Path]:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    result_path = target / "results.csv"
    with result_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["scenario_id", "scenario_name", "year", "pathway", "category", "impact", "baseline_difference", "baseline_percent_difference"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        comparisons = {x["scenario_id"]: x for x in run_data.get("comparisons", [])}
        baseline_id = run_data["project"]["baseline_scenario_id"]
        for result in run_data.get("results", []):
            comparison = comparisons.get(result["scenario_id"], {})
            for category, impact in result["impacts"].items():
                writer.writerow({
                    "scenario_id": result["scenario_id"],
                    "scenario_name": result["scenario_name"],
                    "year": result["year"],
                    "pathway": result["pathway"],
                    "category": category,
                    "impact": f"{impact:.12g}",
                    "baseline_difference": "0" if result["scenario_id"] == baseline_id else f"{comparison.get('difference', {}).get(category, 0.0):.12g}",
                    "baseline_percent_difference": "0" if result["scenario_id"] == baseline_id else f"{comparison.get('percent_difference', {}).get(category, 0.0):.12g}",
                })
    written.append(result_path)

    contribution_path = target / "contributions.csv"
    with contribution_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["scenario_id", "item_id", "item_name", "stage", "layer", "category", "quantity", "unit", "factor", "impact", "source", "is_credit"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in run_data.get("results", []):
            for contribution in result["contributions"]:
                row = dict(contribution)
                row["scenario_id"] = result["scenario_id"]
                writer.writerow(row)
    written.append(contribution_path)

    assumptions_path = target / "assumptions.csv"
    with assumptions_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["id", "category", "statement", "value", "unit", "source", "status", "rationale", "critical"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for choice in run_data["project"].get("choices", []):
            writer.writerow({key: choice.get(key, "") for key in fieldnames})
    written.append(assumptions_path)
    return written

