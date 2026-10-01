"""Always-available adapter for the original, clearly marked demo inventory."""

from __future__ import annotations

from typing import Any

from app.domain.models import Project
from app.services.engine import run_project


class SyntheticAdapter:
    name = "synthetic"

    def calculate(self, project: Project, scenario_ids: list[str]) -> dict[str, Any]:
        return run_project(project, mode="demo", selected_scenario_ids=scenario_ids)

