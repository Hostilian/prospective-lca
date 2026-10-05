# Review-package verification

5 October 2026 · Report edition 1.1 · Engine 0.1.1

The package is ready for technical discussion with its synthetic status intact. Scientific acceptance remains open; no real AWAM inventory or approved LCIA has been calculated.

| Check | Outcome | Evidence |
|---|---|---|
| Source data | Pass | Exact supplied totals, percentages and contribution labels retained; source inventory unchanged. |
| Presentation arithmetic | Pass | Decimal recomputation and disclosed rounding; supplied values and full-precision calculation remain separate. |
| Diagnostics | Pass | Independent credit/denominator and quantity × factor interaction checks; both decomposition orders reconcile. |
| Calculation integrity | Pass | Source recalculation and manifest comparison reject altered exports before report generation. |
| Document integrity | Pass | Three HTML hashes and diagnostic JSON fingerprint/content verified; modified HTML rejected. |
| Automated tests | Pass | 23 offline tests; compile check for application, tests and tools. |
| Production gate | Pass | Synthetic/proposed project is blocked; expected exit code 2. |
| Mobile/desktop | Pass | Both routes at 375 × 812 and 1440 × 1000 in light/dark; no horizontal overflow or clipped chart labels. |
| Entry status | Pass | Synthetic and unapproved-method notice visible in all eight checked first viewports. |
| Text contrast | Pass in checked views | Rendered text colour pairs meet 4.5:1, or 3:1 for large text; graphic colour and direct labels supplement each other. |
| JavaScript disabled | Pass | Ten sections and both core charts remain readable; variant links work; optional print control is hidden. |
| Keyboard entry | Pass | Skip link receives focus and moves to main content in both routes. |
| Network/console | Pass | No initial external requests or browser execution errors. |
| A4 print | Pass | Study brief: 14 pages; technical report: 15 pages. Pages rendered and inspected; no extracted text outside checked margins. Charts and core tables remain together. |
| File size | Pass | Each standalone HTML is below 57 KB and the 300 KB limit. |

Browser checks use Chromium; they are not a claim of full WCAG certification or exhaustive cross-browser coverage. Printouts were generated for QA. HTML, JSON and CSV remain the review exports.

The container and GitHub workflow now build and verify the same review routes. CI retains a ZIP with its source revision and checksums; Pages also publishes it. Consult the linked workflow for remote execution status.

## Scientific gates retained

The treatment service/reference flow, moisture, outputs and counterfactual are unresolved. Credit exclusion does not model an alternative treatment system. Simple scale multipliers and future factors remain synthetic. An approved model/database/method, measured process balance, study-specific sensitivities, uncertainty treatment and named scientific acceptance are required for a real pilot.

The author is recorded as Eren Ozturk. The audience is an LCA/process researcher; introductory glossary material and identity/contact placeholders have been removed. Public professional research supports that audience choice without asserting Dr. Mara Silva's approval or personal preferences.
