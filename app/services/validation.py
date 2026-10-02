"""Pre-run validation with explicit, actionable findings."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from app.domain.models import ApprovalState, Project, Scenario
from app.domain.units import UnitError, assert_quantity, compatible, normalize_unit


@dataclass
class ValidationIssue:
    code: str
    severity: str
    message: str
    location: str
    remediation: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class ValidationReport:
    mode: str
    selected_scenarios: list[str]
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [x for x in self.issues if x.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [x for x in self.issues if x.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "selected_scenarios": self.selected_scenarios,
            "ok": self.ok,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "issues": [x.to_dict() for x in self.issues],
        }


def _issue(report: ValidationReport, code: str, severity: str, message: str, location: str, remediation: str) -> None:
    report.issues.append(ValidationIssue(code, severity, message, location, remediation))


def _scenario_map(project: Project) -> dict[str, Scenario]:
    return {scenario.id: scenario for scenario in project.scenarios}


def validate_project(project: Project, *, mode: str = "demo", selected_scenario_ids: list[str] | None = None) -> ValidationReport:
    """Validate structure, comparability, provenance, and approval gates."""

    if mode not in {"demo", "production"}:
        raise ValueError("mode must be 'demo' or 'production'")
    selected = selected_scenario_ids or [x.id for x in project.scenarios]
    report = ValidationReport(mode=mode, selected_scenarios=selected)
    scenarios = _scenario_map(project)
    inventory = {item.id: item for item in project.inventory}

    required_study = {
        "goal": "State the decision or question the study supports.",
        "functional_unit": "Define the functional unit and reference flow.",
        "system_boundary": "Define included and excluded life-cycle stages.",
        "geography": "Provide a geography.",
        "baseline_year": "Provide a baseline year.",
        "target_years": "Provide at least one target year.",
        "impact_method": "Name the approved LCIA method and categories.",
    }
    for key, remediation in required_study.items():
        if not project.study.get(key):
            severity = "error" if mode == "production" else "warning"
            _issue(report, "MISSING_STUDY_FIELD", severity, f"Study field '{key}' is missing.", f"study.{key}", remediation)

    if project.baseline_scenario_id not in scenarios:
        _issue(report, "BASELINE_NOT_FOUND", "error", "The baseline scenario ID does not resolve.", "baseline_scenario_id", "Choose one existing scenario as the baseline.")
    elif project.baseline_scenario_id not in selected:
        _issue(report, "BASELINE_NOT_SELECTED", "error", "The baseline scenario must be included when results are compared.", "selected_scenarios", "Include the project baseline in the selected scenario set.")

    if len(scenarios) != len(project.scenarios):
        _issue(report, "DUPLICATE_SCENARIO_ID", "error", "Scenario IDs must be unique.", "scenarios", "Rename duplicate scenario IDs before running.")

    if len(inventory) != len(project.inventory):
        _issue(report, "DUPLICATE_INVENTORY_ID", "error", "Inventory item IDs must be unique.", "inventory", "Give each inventory item a unique ID.")
    if not project.impact_categories:
        _issue(report, "MISSING_IMPACT_CATEGORIES", "error", "At least one impact category is required.", "impact_categories", "Define the categories used by the inventory factors.")
    if len(selected) != len(set(selected)):
        _issue(report, "DUPLICATE_SELECTED_SCENARIO", "error", "A scenario was selected more than once.", "selected_scenarios", "Select each scenario only once.")

    choice_ids = {choice.id for choice in project.choices}
    if len(choice_ids) != len(project.choices):
        _issue(report, "DUPLICATE_CHOICE_ID", "error", "Assumption/choice IDs must be unique.", "choices", "Give each assumption a stable unique ID.")

    if project.synthetic_only and mode == "production":
        _issue(report, "SYNTHETIC_PROJECT_BLOCKED", "error", "A synthetic-only project cannot be labelled as a production run.", "synthetic_only", "Use demo mode or replace the inventory with an approved real pilot.")

    for scenario_id in selected:
        scenario = scenarios.get(scenario_id)
        if scenario is None:
            _issue(report, "SCENARIO_NOT_FOUND", "error", f"Scenario '{scenario_id}' was requested but is missing.", f"scenarios.{scenario_id}", "Select an existing scenario ID.")
            continue
        if not scenario.narrative.strip():
            _issue(report, "MISSING_SCENARIO_NARRATIVE", "error", "Every scenario needs a readable narrative.", f"scenarios.{scenario.id}.narrative", "Explain the pathway, technology maturity, and major changes.")
        if scenario.background_year is not None and scenario.background_year != scenario.year:
            _issue(report, "TEMPORAL_MISMATCH", "error", f"Foreground year {scenario.year} and background year {scenario.background_year} differ.", f"scenarios.{scenario.id}", "Align the years or document and approve a defensible temporal bridge.")
        if scenario.geography != project.study.get("geography"):
            _issue(report, "GEOGRAPHY_MISMATCH", "warning", f"Scenario geography {scenario.geography!r} differs from study geography {project.study.get('geography')!r}.", f"scenarios.{scenario.id}.geography", "Confirm whether the scenario is intentionally regionalised.")
        if scenario.foreground_id == "":
            _issue(report, "MISSING_FOREGROUND_ID", "error", "Scenario has no foreground identifier.", f"scenarios.{scenario.id}.foreground_id", "Provide a stable foreground model ID.")
        if scenario.background_id == "":
            _issue(report, "MISSING_BACKGROUND_ID", "error", "Scenario has no background identifier.", f"scenarios.{scenario.id}.background_id", "Provide a stable background model ID.")

        seen_transformations: set[str] = set()
        for transformation in scenario.transformations:
            if transformation.scenario_id != scenario.id:
                _issue(report, "TRANSFORMATION_SCENARIO_MISMATCH", "error", f"Transformation {transformation.id!r} belongs to another scenario.", f"scenarios.{scenario.id}.transformations", "Set scenario_id to the containing scenario ID.")
            if transformation.id in seen_transformations:
                _issue(report, "DUPLICATE_TRANSFORMATION_ID", "error", f"Transformation ID {transformation.id!r} is duplicated within the scenario.", f"scenarios.{scenario.id}.transformations", "Use a unique stable transformation ID.")
            seen_transformations.add(transformation.id)
            target_parts = transformation.target.split(":", 1)
            item_id = target_parts[0]
            if item_id not in inventory:
                _issue(report, "UNKNOWN_TRANSFORMATION_TARGET", "error", f"Transformation targets unknown inventory item {item_id!r}.", f"scenarios.{scenario.id}.transformations.{transformation.id}", "Choose an existing item or add it to the approved foreground inventory.")
                continue
            item = inventory[item_id]
            try:
                if transformation.operation in {"scale_quantity", "set_quantity"}:
                    if len(target_parts) != 2 or target_parts[1] != "quantity":
                        _issue(report, "INVALID_QUANTITY_TARGET", "error", f"Quantity target {transformation.target!r} must end in ':quantity'.", f"transformations.{transformation.id}.target", "Use item_id:quantity.")
                    if transformation.unit and not compatible(transformation.unit, item.unit):
                        _issue(report, "UNIT_INCOMPATIBLE", "error", f"{transformation.unit} cannot be applied to {item.unit}.", f"transformations.{transformation.id}.unit", "Use a compatible unit.")
                    if transformation.operation == "scale_quantity":
                        # The value is a dimensionless multiplier. Its optional unit
                        # labels the affected flow and must not imply conversion.
                        if transformation.unit and normalize_unit(transformation.unit) != normalize_unit(item.unit):
                            _issue(report, "SCALE_UNIT_MISMATCH", "error", f"Scale multiplier for {item.id!r} cannot relabel {item.unit} as {transformation.unit}.", f"transformations.{transformation.id}.unit", "Use the inventory unit or omit the unit for a dimensionless multiplier.")
                        assert_quantity(transformation.value, "unit")
                    else:
                        assert_quantity(transformation.value, transformation.unit or item.unit, allow_negative=item.is_credit)
                elif transformation.operation in {"scale_factor", "set_factor"}:
                    if len(target_parts) != 2 or target_parts[1] not in item.factors:
                        _issue(report, "UNKNOWN_FACTOR_TARGET", "error", f"Transformation factor target {transformation.target!r} is not defined.", f"transformations.{transformation.id}.target", "Use item_id:impact_category from the inventory.")
                    assert_quantity(transformation.value, "unit", allow_negative=False)
                else:
                    _issue(report, "UNKNOWN_OPERATION", "error", f"Unknown transformation operation {transformation.operation!r}.", f"transformations.{transformation.id}.operation", "Use scale_quantity, set_quantity, scale_factor, or set_factor.")
            except UnitError as exc:
                _issue(report, "INVALID_QUANTITY", "error", str(exc), f"transformations.{transformation.id}", "Correct the number and unit.")
            if not transformation.evidence_source:
                severity = "error" if mode == "production" else "warning"
                _issue(report, "MISSING_TRANSFORMATION_PROVENANCE", severity, "Every transformation needs an evidence source.", f"transformations.{transformation.id}.evidence_source", "Add a paper, measurement, engineering note, or explicit interview decision.")
            if mode == "production" and transformation.approval_state != ApprovalState.SCIENTIST_APPROVED:
                _issue(report, "UNAPPROVED_TRANSFORMATION", "error", f"Transformation {transformation.id} is not scientist-approved.", f"transformations.{transformation.id}.approval_state", "Have the scientific owner review and approve it.")

    for choice in project.choices:
        if mode == "production" and choice.critical and choice.status != ApprovalState.SCIENTIST_APPROVED:
            _issue(report, "UNAPPROVED_CHOICE", "error", f"Critical choice {choice.id} is {choice.status.value}.", f"choices.{choice.id}.status", "Resolve and approve the choice with AWAM's scientific owner.")
        if not choice.source:
            severity = "error" if mode == "production" and choice.critical else "warning"
            _issue(report, "MISSING_CHOICE_SOURCE", severity, f"Choice {choice.id} has no source or provenance.", f"choices.{choice.id}.source", "Record the source, measurement, method, or decision note.")

    for item in project.inventory:
        try:
            assert_quantity(item.quantity, item.unit, allow_negative=item.is_credit)
        except UnitError as exc:
            _issue(report, "INVALID_INVENTORY_QUANTITY", "error", str(exc), f"inventory.{item.id}", "Correct the inventory quantity/unit.")
        if not item.source:
            _issue(report, "MISSING_INVENTORY_SOURCE", "error" if mode == "production" else "warning", f"Inventory item {item.id} has no source note.", f"inventory.{item.id}.source", "Add a measurement, literature source, or synthetic-data declaration.")
        for category in project.impact_categories:
            if category not in item.factors:
                _issue(report, "MISSING_FACTOR", "error", f"Inventory item {item.id!r} has no factor for {category!r}.", f"inventory.{item.id}.factors", "Provide an explicit factor or remove the category from the study.")
            else:
                try:
                    assert_quantity(item.factors[category], "unit", allow_negative=True)
                except UnitError as exc:
                    _issue(report, "INVALID_FACTOR", "error", str(exc), f"inventory.{item.id}.factors.{category}", "Use a finite numeric factor.")

    return report
