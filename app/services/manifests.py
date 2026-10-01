"""Run manifests and reproducibility fingerprints."""

from __future__ import annotations

from datetime import datetime, timezone
import platform
from pathlib import Path
import sys
import uuid
from typing import Any

from app import __version__
from app.domain.models import Project, dump_json
from app.services.hashing import sha256_json


def build_manifest(project: Project, run_data: dict[str, Any], selected_scenario_ids: list[str]) -> dict[str, Any]:
    project_payload = project.to_dict()
    input_fingerprint = sha256_json({"project": project_payload, "scenarios": selected_scenario_ids})
    assumptions_payload = {
        "choices": project_payload.get("choices", []),
        "scenario_transformations": run_data.get("transformation_diffs", {}),
    }
    result_fingerprint = sha256_json({"results": run_data.get("results", []), "comparisons": run_data.get("comparisons", [])})
    run_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"awam-lca:{input_fingerprint}"))
    return {
        "run_uuid": run_uuid,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "application_version": __version__,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "project_id": project.id,
        "scenario_ids": selected_scenario_ids,
        "calculation_engine": run_data.get("metadata", {}).get("calculation_engine"),
        "input_manifest_hash": input_fingerprint,
        "assumption_ledger_hash": sha256_json(assumptions_payload),
        "result_artifact_hash": result_fingerprint,
        "database": {
            "name": "synthetic-original-inventory",
            "version": "0.1",
            "licensed_data_included": False,
        },
        "validation": run_data.get("validation", {}),
        "limitations": [
            "Synthetic demonstration only; no AWAM or licensed inventory data.",
            "Impact factors are illustrative proxies, not an approved LCIA method.",
            "Scientific choices remain subject to AWAM review.",
        ],
    }


def write_manifest(manifest: dict[str, Any], path: str | Path) -> None:
    dump_json(manifest, path)

