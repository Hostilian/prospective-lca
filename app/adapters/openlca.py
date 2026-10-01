"""Opt-in openLCA IPC connectivity probe.

The adapter intentionally stops at a safe probe and descriptor contract until
AWAM supplies an approved openLCA version, database, model, LCIA method and
licensed-data workflow.  It never bundles or uploads ecoinvent data.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class ProbeResult:
    reachable: bool
    endpoint: str
    status: int | None
    message: str


class OpenLCAAdapter:
    name = "openlca-ipc"

    def __init__(self, endpoint: str = "http://localhost:8080") -> None:
        self.endpoint = endpoint.rstrip("/")

    def probe(self, timeout: float = 2.0) -> ProbeResult:
        """Try a harmless GET; a failed probe is actionable, not fatal to demo mode."""

        request = Request(self.endpoint, method="GET", headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310 - explicit user-provided local endpoint
                return ProbeResult(True, self.endpoint, response.status, "Endpoint responded; use IPC descriptor calls next.")
        except HTTPError as exc:
            return ProbeResult(True, self.endpoint, exc.code, "Endpoint is reachable but did not accept the probe path; use the configured IPC API.")
        except (URLError, TimeoutError, OSError) as exc:
            return ProbeResult(False, self.endpoint, None, f"Endpoint unavailable: {exc}. Start the approved openLCA IPC server and retry.")

    @staticmethod
    def json_rpc_request(method: str, params: dict[str, Any], request_id: int = 1) -> bytes:
        """Build a JSON-RPC payload without sending it or embedding credentials."""

        return json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}).encode("utf-8")

