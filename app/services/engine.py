"""Deterministic synthetic calculation and scenario comparison engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from app.domain.models import InventoryItem, Project, Scenario
from app.domain.units import convert
from app.services.validation import ValidationReport, validate_project


class CalculationBlocked(RuntimeError):
    """Raised when validation prevents a calculation."""

    def __init__(self, report: ValidationReport):
        self.report = report
        super().__init__("Calculation blocked by validation: " + "; ".join(x.message for x in report.errors))


@dataclass
class Contribution:
    item_id: str
    item_name: str
    stage: str
    layer: str
    quantity: float
    unit: str
    category: str
    factor: float
    impact: float
    source: str
    is_credit: bool


@dataclass
class ScenarioResult:
    scenario_id: str
    scenario_name: str
    year: int
    pathway: str
    impacts: dict[str, float]
    by_layer: dict[str, dict[str, float]]
    by_stage: dict[str, dict[str, float]]
    contributions: list[Contribution]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data


@dataclass
class Comparison:
    scenario_id: str
    baseline_id: str
    difference: dict[str, float]
    percent_difference: dict[str, float | None]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _factor_for(item: InventoryItem, category: str) -> float:
    return float(item.factors.get(category, 0.0))


def _apply_transformations(scenario: Scenario, quantities: dict[str, float], factors: dict[str, dict[str, float]], item_units: dict[str, str]) -> list[dict[str, Any]]:
    diff: list[dict[str, Any]] = []
    for transformation in scenario.transformations:
        target_parts = transformation.target.split(":", 1)
        item_id = target_parts[0]
        if transformation.operation == "scale_quantity":
            before = quantities[item_id]
            quantities[item_id] = before * transformation.value
            after = quantities[item_id]
        elif transformation.operation == "set_quantity":
            before = quantities[item_id]
            target_unit = item_units[item_id]
            quantities[item_id] = convert(transformation.value, transformation.unit or target_unit, target_unit)
            after = quantities[item_id]
        elif transformation.operation == "scale_factor":
            category = target_parts[1]
            before = factors[item_id][category]
            factors[item_id][category] = before * transformation.value
            after = factors[item_id][category]
        elif transformation.operation == "set_factor":
            category = target_parts[1]
            before = factors[item_id][category]
            factors[item_id][category] = transformation.value
            after = factors[item_id][category]
        else:
            raise ValueError(f"Unsupported transformation: {transformation.operation}")
        diff.append({
            "id": transformation.id,
            "scenario_id": scenario.id,
            "operation": transformation.operation,
            "target": transformation.target,
            "input_value": transformation.value,
            "input_unit": transformation.unit,
            "result_unit": item_units[item_id] if transformation.operation.endswith("quantity") else None,
            "before": before,
            "after": after,
            "formula": transformation.formula,
            "evidence_source": transformation.evidence_source,
            "approval_state": transformation.approval_state.value,
        })
    return diff


def calculate_scenario(project: Project, scenario: Scenario) -> tuple[ScenarioResult, list[dict[str, Any]]]:
    """Calculate the synthetic inventory with explicit transformation diffs."""

    quantities = {item.id: item.quantity for item in project.inventory}
    factors = {item.id: dict(item.factors) for item in project.inventory}
    transformation_diff = _apply_transformations(scenario, quantities, factors, {item.id: item.unit for item in project.inventory})
    impacts = {category: 0.0 for category in project.impact_categories}
    by_layer: dict[str, dict[str, float]] = {}
    by_stage: dict[str, dict[str, float]] = {}
    contributions: list[Contribution] = []

    for item in project.inventory:
        for category in project.impact_categories:
            factor = factors[item.id].get(category, 0.0)
            impact = quantities[item.id] * factor
            impacts[category] += impact
            by_layer.setdefault(item.layer, {}).setdefault(category, 0.0)
            by_layer[item.layer][category] += impact
            by_stage.setdefault(item.stage, {}).setdefault(category, 0.0)
            by_stage[item.stage][category] += impact
            contributions.append(Contribution(item.id, item.name, item.stage, item.layer, quantities[item.id], item.unit, category, factor, impact, item.source, item.is_credit))

    return ScenarioResult(scenario.id, scenario.name, scenario.year, scenario.pathway, impacts, by_layer, by_stage, contributions), transformation_diff


def compare_results(results: list[ScenarioResult], baseline_id: str) -> list[Comparison]:
    baseline = next((x for x in results if x.scenario_id == baseline_id), None)
    if baseline is None:
        raise ValueError(f"Baseline result not found: {baseline_id}")
    comparisons: list[Comparison] = []
    for result in results:
        if result.scenario_id == baseline_id:
            continue
        difference: dict[str, float] = {}
        percent: dict[str, float | None] = {}
        for category, value in result.impacts.items():
            base = baseline.impacts.get(category, 0.0)
            delta = value - base
            difference[category] = delta
            percent[category] = None if base == 0 else delta / base * 100.0
        comparisons.append(Comparison(result.scenario_id, baseline_id, difference, percent))
    return comparisons


def run_project(project: Project, *, mode: str = "demo", selected_scenario_ids: list[str] | None = None) -> dict[str, Any]:
    selected = selected_scenario_ids or [x.id for x in project.scenarios]
    validation = validate_project(project, mode=mode, selected_scenario_ids=selected)
    if not validation.ok:
        raise CalculationBlocked(validation)
    scenario_map = {x.id: x for x in project.scenarios}
    results: list[ScenarioResult] = []
    diffs: dict[str, list[dict[str, Any]]] = {}
    for scenario_id in selected:
        result, diff = calculate_scenario(project, scenario_map[scenario_id])
        results.append(result)
        diffs[scenario_id] = diff
    comparisons = compare_results(results, project.baseline_scenario_id)
    return {
        "project": project.to_dict(),
        "validation": validation.to_dict(),
        "results": [result.to_dict() for result in results],
        "comparisons": [comparison.to_dict() for comparison in comparisons],
        "transformation_diffs": diffs,
        "metadata": {
            "calculation_engine": "AWAM synthetic adapter 0.1",
            "scientific_status": "illustrative synthetic calculation; not an LCIA result",
        },
    }
