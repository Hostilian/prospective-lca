"""Adapter contracts used to keep engine integrations replaceable."""

from __future__ import annotations

from typing import Any, Protocol

from app.domain.models import Project


class CalculationAdapter(Protocol):
    name: str

    def calculate(self, project: Project, scenario_ids: list[str]) -> dict[str, Any]:
        ...

