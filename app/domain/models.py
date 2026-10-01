"""Serializable domain models for a reviewable prospective-LCA project."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any
import json


class ApprovalState(str, Enum):
    UNRESOLVED = "unresolved"
    PROPOSED = "proposed"
    SCIENTIST_APPROVED = "scientist_approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


def _state(value: str | ApprovalState | None) -> ApprovalState:
    if value is None:
        return ApprovalState.UNRESOLVED
    return value if isinstance(value, ApprovalState) else ApprovalState(value)


@dataclass
class Choice:
    """A scientific or governance choice with a visible approval state."""

    id: str
    category: str
    statement: str
    value: Any = None
    unit: str | None = None
    source: str | None = None
    rationale: str | None = None
    status: ApprovalState = ApprovalState.UNRESOLVED
    author: str | None = None
    reviewer: str | None = None
    uncertainty: str | None = None
    critical: bool = True
    last_modified: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Choice":
        data = dict(raw)
        data["status"] = _state(data.get("status"))
        return cls(**data)


@dataclass
class Transformation:
    """One explicit, machine-readable foreground or background change."""

    id: str
    scenario_id: str
    operation: str
    target: str
    value: float
    unit: str | None = None
    formula: str = ""
    evidence_source: str | None = None
    rationale: str | None = None
    approval_state: ApprovalState = ApprovalState.PROPOSED
    uncertainty: str | None = None
    applicable_geography: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Transformation":
        data = dict(raw)
        data["approval_state"] = _state(data.get("approval_state"))
        return cls(**data)


@dataclass
class InventoryItem:
    """An illustrative inventory exchange and its synthetic impact factors."""

    id: str
    name: str
    stage: str
    layer: str
    quantity: float
    unit: str
    factors: dict[str, float]
    source: str
    is_credit: bool = False
    notes: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "InventoryItem":
        return cls(**raw)


@dataclass
class Scenario:
    id: str
    name: str
    year: int
    pathway: str
    geography: str
    foreground_id: str
    background_id: str
    narrative: str
    tags: list[str] = field(default_factory=list)
    transformations: list[Transformation] = field(default_factory=list)
    assumption_ids: list[str] = field(default_factory=list)
    background_year: int | None = None
    background_pathway: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Scenario":
        data = dict(raw)
        data["transformations"] = [Transformation.from_dict(x) for x in data.get("transformations", [])]
        return cls(**data)


@dataclass
class Project:
    id: str
    name: str
    description: str
    synthetic_only: bool
    baseline_scenario_id: str
    study: dict[str, Any]
    impact_categories: dict[str, dict[str, str]]
    choices: list[Choice]
    inventory: list[InventoryItem]
    scenarios: list[Scenario]
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Project":
        data = dict(raw)
        data["choices"] = [Choice.from_dict(x) for x in data.get("choices", [])]
        data["inventory"] = [InventoryItem.from_dict(x) for x in data.get("inventory", [])]
        data["scenarios"] = [Scenario.from_dict(x) for x in data.get("scenarios", [])]
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for choice in data["choices"]:
            choice["status"] = choice["status"].value
        for scenario in data["scenarios"]:
            for transformation in scenario["transformations"]:
                transformation["approval_state"] = transformation["approval_state"].value
        return data


def load_project(path: str | Path) -> Project:
    """Load a JSON project definition."""

    source = Path(path)
    with source.open("r", encoding="utf-8") as handle:
        return Project.from_dict(json.load(handle))


def dump_json(data: Any, path: str | Path) -> None:
    """Write stable, human-readable JSON."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")

