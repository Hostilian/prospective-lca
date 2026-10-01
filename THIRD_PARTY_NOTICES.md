# Third-party notices

The offline vertical slice currently uses only the Python standard library at runtime.

The planned optional integrations refer to external projects and documentation:

| Component | Intended role | Project/licence note |
|---|---|---|
| openLCA IPC / `olca-ipc` | Connect to a user-started openLCA IPC server | Use the upstream project’s current licence and version; do not vendor the client without checking it. |
| openLCA | Approved calculation engine supplied by AWAM | External application; database and model licences remain separate. |
| Brightway | Optional prospective-background calculation route | Use the selected Brightway release and its dependency licences. |
| premise | Optional IAM-to-LCA background transformation | Use the selected premise release and its dependency licences; record IAM and database versions. |
| ecoinvent | Possible licensed background inventory | No ecoinvent data is present. Follow the applicable ecoinvent licence, including developer/integration terms where relevant. |

This file is a project-level notice, not legal advice. A real AWAM pilot needs a dependency licence audit and a data-redistribution decision before packaging.

