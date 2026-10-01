# Data governance

## Rules

1. Keep licensed and confidential data outside the repository.
2. Do not upload ecoinvent, AWAM project files, credentials, or tokens to external services.
3. Store only metadata needed for reproducibility in manifests.
4. Use an allowlisted local data root for real pilot files.
5. Sanitize logs and exports.
6. Mark every data source as measured, literature, engineering, synthetic, or unresolved.
7. Record versions and checksums for source databases and IAM files without copying protected contents.
8. Give every assumption and transformation an owner, source, and approval state.
9. Separate internal review packages from any externally communicated result.
10. Confirm IP, publication, confidentiality, retention, and paid-work terms before production work.

## ecoinvent boundary

The repository deliberately contains no ecoinvent dataset. The public ecoinvent licensing page states that integrating ecoinvent data into software/tools, including internal tools, may call for a developer licence. That is a prompt for AWAM’s legal/data owner to confirm the correct arrangement, not a legal conclusion by this prototype.

## Real-pilot file layout suggestion

```text
local-data/
  approved/
    openlca-descriptors/
    project-inputs/
    source-register/
  licensed/              # ignored; never committed
  confidential/          # ignored; never committed
  exports-internal/      # access-controlled review packages
```

