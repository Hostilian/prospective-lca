# Source register

Access date for all web sources below: **2026-09-29**.

| ID | Source | Type | Claim or decision supported |
|---|---|---|---|
| S-01 | https://www.awam.fraunhofer.pt/ | Official AWAM profile | AWAM is a Fraunhofer Portugal research centre working across water, energy, resource management, process technologies, and resource valorisation. |
| S-02 | https://www.awam.fraunhofer.pt/en/technologies.html | Official AWAM technology page | AWAM describes LCA as a tool for developing, optimising, and evaluating processes, products, and engineering systems. |
| S-03 | https://www.awam.fraunhofer.pt/content/dam/portugal/awam/technologies/AWAM%20Specsheet_LCA_EN.pdf | Official AWAM specification sheet | AWAM’s LCA service uses openLCA and databases such as ecoinvent, according to the public specification sheet. |
| S-04 | https://www.iso.org/standard/37456.html | Official standard page | ISO 14040 covers LCA principles/framework, goal and scope, inventory, impact assessment, interpretation, reporting, critical review, limitations, and optional elements. |
| S-05 | https://www.iso.org/standard/38498.html | Official standard page | ISO 14044 specifies requirements and guidelines for LCA, including goal/scope, inventory, LCIA, interpretation, reporting, critical review, and limitations. |
| S-06 | https://publications.jrc.ec.europa.eu/repository/handle/JRC129632 | European Commission JRC report | PLANET BIO reviews prospective LCA for novel/emerging bio-based products and emphasises consistent, comprehensive assessment of future environmental burdens. |
| S-07 | https://doi.org/10.1007/s11367-023-02265-8 | Peer-reviewed terminology paper | Future-oriented LCA terms require careful distinction; temporal positionality and technology maturity matter. |
| S-08 | https://doi.org/10.1111/jiec.12690 | Peer-reviewed prospective-LCA guidance | Prospective LCA needs explicit future scenarios, technology development assumptions, and transparent modelling choices. Verify full paper wording before quoting. |
| S-09 | https://www.openlca.org/download/ | Official openLCA page | The current official download page surfaced openLCA 2.7.0 on access date. Verify the exact build/OS before a pilot. |
| S-10 | https://www.openlca.org/features/ | Official openLCA feature page | openLCA provides an IPC server and supports integration from Python/JS/TS/C# plus ILCD exchange. |
| S-11 | https://greendelta.github.io/openLCA-ApiDoc/ | Official API documentation | openLCA IPC exposes JSON-RPC/REST/gRPC-related API documentation and model/result endpoints. |
| S-12 | https://github.com/GreenDelta/olca-ipc.py | Upstream client repository | `olca-ipc` is a Python client for openLCA IPC; the repository page surfaced version 2.6.3 in its project metadata during research. |
| S-13 | https://docs.brightway.dev/en/latest/ | Official Brightway documentation | Brightway is a documented LCA software framework suitable as a potential calculation route. |
| S-14 | https://premise.readthedocs.io/en/latest/ | Official premise documentation | The current documentation is labelled premise 2.5.2 and covers IAM scenarios, transformation, validation, export, and the Python API. |
| S-15 | https://premise.readthedocs.io/en/latest/reference/compatibility.html | Official premise compatibility page | The documentation lists supported ecoinvent versions and requires explicit source/version/model metadata. |
| S-16 | https://premise.readthedocs.io/en/latest/getting_started/overview.html | Official premise guidance | Reproducibility requires recording premise/version, source database, ecoinvent system model, IAM file checksum/release, constructor options, and custom inputs. |
| S-17 | https://support.ecoinvent.org/licensing | Official ecoinvent licensing page | Integrating ecoinvent data into internal software/tools may require a developer licence; the workbench therefore excludes licensed data by default. |
| S-18 | https://support.ecoinvent.org/system-models | Official ecoinvent guidance | System models treat allocation/substitution differently; the workbench must make the selected system model explicit. |

## Evidence discipline

`S-01`–`S-18` are sources for the research brief, not proof that Mara requested a particular pilot. The exact pilot and internal AWAM workflow remain reported interview context or unresolved until Mara confirms them. No number in the synthetic demo is sourced from these pages.


## Reviewer-context update — 5 October 2026

| ID | Primary source | Use in this package |
|---|---|---|
| S-19 | [Fraunhofer Portugal governance](https://www.fraunhofer.pt/en/about/governance-boards.html) | Mara Silva's senior-scientist role and AWAM section presidency; professional identity only. |
| S-20 | [ORCID 0000-0003-2765-3987](https://orcid.org/0000-0003-2765-3987) | Self-asserted employment/education; older biography noted. |
| S-21 | [SETAC 2026 programme](https://www.setac.org/static/66e406ee-b1ba-46b8-a8f165c4cbf438ad/Full-Maastricht-Programme-Book.pdf) | Public winery-by-product LCA presentation. |
| S-22 | [Silva et al., Recycling 2026, 11(9), 155](https://www.mdpi.com/2313-4321/11/9/155) | Functional-unit and process-energy/sensitivity review context; no data imported. |
| S-23 | [GitHub upload-artifact documentation](https://github.com/actions/upload-artifact) | Official `v7` artifact upload syntax and retention settings. |

S-03's official AWAM LCA sheet was also rechecked. See [reviewer context](docs/reviewer-context.md) for the distinction between verified facts and proposed review priorities. The private interview identity and internal requirements are not independently confirmed by these sources. No synthetic result is derived from this research.
