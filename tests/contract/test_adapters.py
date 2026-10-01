import unittest

from app.adapters.openlca import OpenLCAAdapter
from app.adapters.premise import ProspectiveBackgroundAdapter


class AdapterContractTests(unittest.TestCase):
    def test_openlca_payload_is_json_rpc(self):
        payload = OpenLCAAdapter.json_rpc_request("data/get", {"@type": "Process"})
        self.assertIn(b'"jsonrpc": "2.0"', payload)
        self.assertIn(b'"method": "data/get"', payload)

    def test_premise_boundary_is_explicitly_not_ready(self):
        data = ProspectiveBackgroundAdapter.availability()
        self.assertFalse(data["ready"])
        self.assertIn("licensing", data["reason"])
