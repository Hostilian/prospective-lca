"""Self-contained HTML report and local dashboard rendering."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.{digits}g}"
    return str(value)


def _hotspot_svg(result: dict[str, Any], category: str, width: int = 860, height: int = 290) -> str:
    rows = [x for x in result.get("contributions", []) if x["category"] == category]
    rows.sort(key=lambda x: abs(x["impact"]), reverse=True)
    rows = rows[:8]
    max_value = max((abs(x["impact"]) for x in rows), default=1.0)
    bar_height = 25
    left = 250
    chart = [f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="Hotspot chart for {escape(category)}">']
    chart.append(f'<text x="{left}" y="20" class="axis">Contribution ({escape(category)})</text>')
    for index, row in enumerate(rows):
        y = 35 + index * 30
        bar_width = max(1.0, (abs(row["impact"]) / max_value) * (width - left - 30))
        color = "#9b4dca" if row["impact"] >= 0 else "#0e7490"
        label = escape(row["item_name"][:34])
        chart.append(f'<text x="0" y="{y + 16}" class="label">{label}</text>')
        chart.append(f'<rect x="{left}" y="{y}" width="{bar_width:.2f}" height="{bar_height}" rx="6" fill="{color}"/>')
        chart.append(f'<text x="{left + bar_width + 8:.2f}" y="{y + 17}" class="value">{_fmt(row["impact"], 4)}</text>')
    chart.append("</svg>")
    return "".join(chart)


def _comparison_table(run_data: dict[str, Any], categories: dict[str, dict[str, str]]) -> str:
    comparisons = {x["scenario_id"]: x for x in run_data.get("comparisons", [])}
    baseline_id = run_data["project"]["baseline_scenario_id"]
    rows: list[str] = []
    for result in run_data.get("results", []):
        cells = [f"<td><strong>{escape(result['scenario_name'])}</strong><br><small>{escape(result['scenario_id'])}</small></td>", f"<td>{result['year']}</td>", f"<td>{escape(result['pathway'])}</td>"]
        comparison = comparisons.get(result["scenario_id"], {})
        for category, meta in categories.items():
            value = result["impacts"].get(category, 0.0)
            if result["scenario_id"] == baseline_id:
                cells.append(f"<td>{_fmt(value)} <small>{escape(meta.get('unit', ''))}</small><br><span class='muted'>baseline</span></td>")
            else:
                delta = comparison.get("difference", {}).get(category, 0.0)
                pct = comparison.get("percent_difference", {}).get(category)
                cells.append(f"<td>{_fmt(value)} <small>{escape(meta.get('unit', ''))}</small><br><span class='{'negative' if delta < 0 else 'positive'}'>{_fmt(delta)} ({_fmt(pct)}%)</span></td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    headings = "".join(f"<th>{escape(meta.get('label', category))}<br><small>{escape(meta.get('unit', ''))}</small></th>" for category, meta in categories.items())
    return f"<table><thead><tr><th>Scenario</th><th>Year</th><th>Pathway</th>{headings}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def render_report(project: dict[str, Any], run_data: dict[str, Any], manifest: dict[str, Any]) -> str:
    categories = project.get("impact_categories", {})
    baseline = project.get("baseline_scenario_id")
    first_result = next((x for x in run_data.get("results", []) if x["scenario_id"] == baseline), run_data.get("results", [{}])[0] if run_data.get("results") else {})
    first_category = next(iter(categories), "")
    validation = run_data.get("validation", {})
    issues = validation.get("issues", [])
    issue_rows = "".join(f"<tr><td><span class='pill {escape(item['severity'])}'>{escape(item['severity'])}</span></td><td>{escape(item['code'])}</td><td>{escape(item['message'])}</td><td>{escape(item['remediation'])}</td></tr>" for item in issues)
    choice_rows = "".join(f"<tr><td>{escape(item.get('id',''))}</td><td>{escape(item.get('category',''))}</td><td>{escape(item.get('statement',''))}</td><td><span class='pill {escape(item.get('status',''))}'>{escape(item.get('status',''))}</span></td><td>{escape(str(item.get('source') or '—'))}</td></tr>" for item in project.get("choices", []))
    scenario_cards = "".join(f"<article class='scenario'><div><span class='eyebrow'>{escape(result['scenario_id'])}</span><h3>{escape(result['scenario_name'])}</h3><p>{result['year']} · {escape(result['pathway'])}</p></div><div class='metric-grid'>" + "".join(f"<div><span>{escape(meta.get('label', category))}</span><strong>{_fmt(result['impacts'].get(category))}</strong><small>{escape(meta.get('unit',''))}</small></div>" for category, meta in categories.items()) + "</div></article>" for result in run_data.get("results", []))
    report_title = escape(project.get("name", "Prospective LCA report"))
    banner = "Synthetic demonstration—not for scientific or external decision-making." if project.get("synthetic_only") else "Review-controlled prospective-LCA workbench output."
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{report_title}</title>
<style>
:root{{--ink:#1f2937;--muted:#64748b;--line:#d8dee8;--paper:#f7f8fb;--card:#fff;--accent:#4f46e5;--purple:#9b4dca;--teal:#0e7490;--green:#16803c;--red:#b42318}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}} main{{max-width:1240px;margin:auto;padding:32px 22px 60px}} header{{background:linear-gradient(135deg,#20264c,#373b7a);color:white;padding:30px;border-radius:24px;margin-bottom:22px;box-shadow:0 12px 30px #2225}} h1{{font-size:34px;line-height:1.1;margin:8px 0 10px;letter-spacing:-.03em}} h2{{margin:30px 0 12px;font-size:22px}} h3{{margin:4px 0;font-size:18px}} p{{margin:7px 0}} .eyebrow{{font-size:11px;letter-spacing:.11em;text-transform:uppercase;font-weight:700;color:#b8c2ff}} .banner{{display:inline-block;background:#fff3c4;color:#6a4b00;border-radius:999px;padding:7px 12px;font-weight:700;font-size:13px}} .meta{{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}} .meta span{{background:#ffffff18;border:1px solid #ffffff28;border-radius:12px;padding:8px 12px}} .card,.scenario{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:19px;box-shadow:0 4px 12px #1e293b08}} .scenario-grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}} .scenario{{display:flex;flex-direction:column;gap:16px}} .metric-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px}} .metric-grid div{{background:#f3f5fa;border-radius:12px;padding:10px}} .metric-grid span,.metric-grid small{{display:block;color:var(--muted);font-size:12px}} .metric-grid strong{{display:block;font-size:20px;margin:3px 0}} table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}} th,td{{text-align:left;vertical-align:top;padding:11px 12px;border-bottom:1px solid var(--line)}} th{{background:#eef0f7;font-size:12px;text-transform:uppercase;letter-spacing:.05em}} tr:last-child td{{border-bottom:0}} small,.muted{{color:var(--muted)}} .positive{{color:var(--red)}} .negative{{color:var(--green)}} .pill{{display:inline-block;border-radius:999px;padding:2px 8px;font-size:11px;font-weight:700;background:#e5e7eb}} .pill.error,.pill.unresolved{{background:#fee4e2;color:var(--red)}} .pill.warning,.pill.proposed{{background:#fff3c4;color:#6a4b00}} .pill.scientist_approved{{background:#dbf6e5;color:var(--green)}} .chart-wrap{{overflow-x:auto;padding:10px 0}} svg{{min-width:760px;max-width:100%;height:auto}} svg .axis{{fill:var(--muted);font-size:12px}} svg .label{{fill:var(--ink);font-size:12px}} svg .value{{fill:var(--ink);font-size:12px;font-weight:700}} .two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} @media(max-width:800px){{.two{{grid-template-columns:1fr}}}} code{{background:#eef0f7;padding:2px 5px;border-radius:5px}} footer{{margin-top:36px;color:var(--muted);font-size:13px}}
</style></head><body><main>
<header><div class="eyebrow">AWAM Prospective LCA Workbench · review package</div><h1>{report_title}</h1><p>{escape(project.get('description',''))}</p><p class="banner">{escape(banner)}</p><div class="meta"><span><b>Baseline:</b> {escape(str(baseline))}</span><span><b>Functional unit:</b> {escape(str(project.get('study',{}).get('functional_unit','—')))}</span><span><b>Run:</b> <code>{escape(manifest.get('run_uuid','—'))}</code></span></div></header>
<section class="card"><h2>Study definition</h2><div class="two"><div><p><b>Goal</b><br>{escape(str(project.get('study',{}).get('goal','—')))}</p><p><b>Boundary</b><br>{escape(str(project.get('study',{}).get('system_boundary','—')))}</p><p><b>Geography</b><br>{escape(str(project.get('study',{}).get('geography','—')))}</p></div><div><p><b>Impact method</b><br>{escape(str(project.get('study',{}).get('impact_method','—')))}</p><p><b>Baseline year</b><br>{escape(str(project.get('study',{}).get('baseline_year','—')))}</p><p><b>Target years</b><br>{escape(', '.join(str(x) for x in project.get('study',{}).get('target_years',[])))}</p></div></div></section>
<h2>Scenario results</h2><div class="scenario-grid">{scenario_cards}</div>
<h2>Comparison to baseline</h2>{_comparison_table(run_data, categories)}
<h2>Hotspot view</h2><div class="card"><p class="muted">The chart is a contribution ranking for the baseline only. Negative values are shown as credits; this is not a validated LCIA hotspot analysis.</p><div class="chart-wrap">{_hotspot_svg(first_result, first_category)}</div></div>
<h2>Assumption ledger</h2>{f'<table><thead><tr><th>ID</th><th>Category</th><th>Statement</th><th>Status</th><th>Source</th></tr></thead><tbody>{choice_rows}</tbody></table>' if choice_rows else '<div class="card">No assumptions recorded.</div>'}
<h2>Validation</h2><div class="card"><p><b>Status:</b> <span class="pill {'scientist_approved' if validation.get('ok') else 'error'}">{'pass' if validation.get('ok') else 'blocked'}</span> · {validation.get('error_count',0)} errors · {validation.get('warning_count',0)} warnings</p></div>{f'<table><thead><tr><th>Severity</th><th>Code</th><th>Finding</th><th>Remediation</th></tr></thead><tbody>{issue_rows}</tbody></table>' if issue_rows else ''}
<h2>Reproducibility</h2><div class="card"><table><tbody><tr><th>Input manifest hash</th><td><code>{escape(manifest.get('input_manifest_hash','—'))}</code></td></tr><tr><th>Assumption ledger hash</th><td><code>{escape(manifest.get('assumption_ledger_hash','—'))}</code></td></tr><tr><th>Result artifact hash</th><td><code>{escape(manifest.get('result_artifact_hash','—'))}</code></td></tr><tr><th>Licensed data included</th><td>{escape(str(manifest.get('database',{}).get('licensed_data_included',False)))}</td></tr></tbody></table></div>
<footer>Generated by AWAM Prospective LCA Workbench {escape(manifest.get('application_version',''))}. Read the scientific limitations before using any result. An approved AWAM scientist remains the owner of modelling choices and interpretation.</footer>
</main></body></html>"""


def write_html_report(project: dict[str, Any], run_data: dict[str, Any], manifest: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_report(project, run_data, manifest), encoding="utf-8")
    return target

