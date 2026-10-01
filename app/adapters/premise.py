"""Optional premise/Brightway adapter boundary.

No premise or ecoinvent dependency is required for the offline demo.  The
adapter records the metadata that must be pinned before a future background
database can be generated safely.
"""

from __future__ import annotations

import importlib.util
from typing import Any


class ProspectiveBackgroundAdapter:
    name = "premise-brightway"

    @staticmethod
    def availability() -> dict[str, Any]:
        return {
            "premise_installed": importlib.util.find_spec("premise") is not None,
            "brightway_installed": importlib.util.find_spec("bw2data") is not None,
            "licensed_database_present": False,
            "ready": False,
            "reason": "Requires AWAM-approved premise/Brightway route, source database, IAM scenario, and licensing review.",
        }

    @staticmethod
    def required_metadata(*, premise_version: str, source_database: str, source_version: str, system_model: str, iam_model: str, pathway: str, year: int) -> dict[str, Any]:
        return {
            "premise_version": premise_version,
            "source_database": source_database,
            "source_version": source_version,
            "system_model": system_model,
            "iam_model": iam_model,
            "pathway": pathway,
            "year": year,
            "status": "requires_scientist_and_license_approval",
        }

