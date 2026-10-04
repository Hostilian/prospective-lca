"""Build two offline editorial previews, preserving the supplied display dataset."""

from __future__ import annotations

import argparse
from dataclasses import replace
from decimal import Decimal, ROUND_HALF_UP
import hashlib
from html import escape as esc
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.domain.models import load_project
from app.services.engine import calculate_scenario

DATA_PATH = ROOT / "demo" / "report_preview_data.json"
DATE = "4 October 2026"
VERSION = "1.0"
CATEGORIES = ["climate_change_kg_co2e", "water_consumption_m3", "cumulative_energy_mj"]
INDICATORS = ["Climate proxy", "Water proxy", "Primary energy proxy"]
SECTIONS = [("summary", "Summary"), ("study", "Study & boundary"), ("scenarios", "Scenario conditions"),
            ("results", "Comparisons"), ("contributions", "Baseline contributions"), ("drivers", "Process & background"),
            ("assumptions", "Assumptions"), ("limitations", "Limitations"), ("next", "Data & next steps"), ("appendix", "Appendix")]

CSS = """
:root{color-scheme:light dark;--paper:#fcfcfd;--ink:#172331;--muted:#4d5e70;--accent:#174f78;--line:#b9c5cf;--wash:#edf2f6;--bar1:#174f78;--bar2:#536577;--bar3:#a8b7c7;--focus:#9b4700}
*{box-sizing:border-box}html{scroll-padding-top:1rem}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--accent);text-underline-offset:.2em}a:hover{text-decoration-thickness:2px}a:focus-visible,button:focus-visible{outline:3px solid var(--focus);outline-offset:4px}.skip{position:absolute;top:-200px;left:16px;z-index:3;background:var(--paper);padding:12px}.skip:focus{top:8px}.switcher{border-bottom:1px solid var(--line);padding:14px max(22px,calc((100vw - 1180px)/2));display:flex;gap:22px;align-items:center;flex-wrap:wrap;font-size:.875rem}.switcher strong{margin-right:auto;font-weight:600}.switcher [aria-current]{color:var(--ink);text-decoration:none;font-weight:700}.layout{max-width:1180px;margin:auto;display:grid;grid-template-columns:185px minmax(0,1fr);gap:58px;padding:40px 24px 72px}.contents{align-self:start;position:sticky;top:26px;font-size:.875rem}.contents p{font-weight:700;margin:0 0 18px}.contents ol{list-style:none;padding:0;margin:0}.contents li{margin-bottom:10px}.contents a{display:block;text-decoration:none;color:var(--muted)}.contents a:hover{color:var(--accent);text-decoration:underline}.contents span{font-variant-numeric:tabular-nums;margin-right:8px;color:var(--accent)}main{min-width:0}header{padding:5px 0 34px;border-bottom:2px solid var(--ink)}.eyebrow{color:var(--accent);font-weight:700;font-size:.875rem;letter-spacing:.06em;text-transform:uppercase}.badge{display:inline-block;border:1px solid var(--accent);padding:3px 9px;margin:0 0 14px;color:var(--accent);font-weight:700;font-size:.875rem}h1{font-size:clamp(2.1rem,4.6vw,3.5rem);line-height:1.08;letter-spacing:-.04em;font-weight:650;max-width:21ch;margin:10px 0 18px}h2{font-size:1.75rem;line-height:1.25;letter-spacing:-.025em;margin:0 0 19px;font-weight:650}h3{font-size:1.125rem;line-height:1.4;margin:24px 0 8px}p{max-width:70ch;margin:0 0 14px}.subtitle{font-size:1.125rem;color:var(--muted)}.meta{font-size:.875rem;color:var(--muted);margin-top:18px}.notice{margin-top:24px;border-left:4px solid var(--accent);background:var(--wash);padding:16px 19px;max-width:75ch}.notice p{margin:0}.notice strong{display:block;margin-bottom:4px}.assumption{color:var(--muted);font-size:.875rem}.section{padding:38px 0;border-bottom:1px solid var(--line);scroll-margin-top:25px}.section-number{font-size:.875rem;color:var(--accent);font-weight:700;display:block;margin-bottom:8px}.lead{font-size:1.25rem;line-height:1.55;max-width:62ch}.note{font-size:.875rem;color:var(--muted);max-width:75ch}.fact-list{display:grid;grid-template-columns:145px minmax(0,1fr);gap:12px 22px;max-width:75ch}.fact-list dt{color:var(--muted)}.fact-list dd{margin:0}.boundary{border:1px solid var(--line);padding:15px;margin:24px 0;break-inside:avoid}.boundary svg{width:100%;max-width:690px;display:block;margin:auto}.boundary rect{fill:var(--wash);stroke:var(--line)}.boundary .core{fill:var(--paper);stroke:var(--accent);stroke-width:2}.boundary text{fill:var(--ink);font-size:16px}.boundary path{stroke:var(--accent);fill:none;stroke-width:1.5}.scenario{padding:20px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:175px minmax(0,1fr);gap:20px}.scenario:last-child{border-bottom:0}.scenario h3{margin:0}.scenario p{margin:0}.scenario .condition{font-size:.875rem;color:var(--muted);margin-top:8px}.legend{display:flex;gap:12px 22px;flex-wrap:wrap;margin:20px 0 12px;font-size:.875rem}.legend span{display:flex;align-items:center;gap:7px}.swatch{display:inline-block;width:20px;height:12px;background:var(--bar1)}.swatch.water{background:var(--bar2)}.swatch.energy{background:var(--bar3)}figure{margin:22px 0;break-inside:avoid}.chart{width:100%;max-width:760px;height:auto;display:block}.chart text{fill:var(--ink);font-family:inherit;font-size:16px}.chart .grid{stroke:var(--line);stroke-width:1}.chart .climate{fill:var(--bar1)}.chart .water{fill:var(--bar2)}.chart .energy{fill:var(--bar3)}.chart .scenario-label{font-weight:650}.chart .pct{font-variant-numeric:tabular-nums}.chart .credit{fill:url(#credit-hatch);stroke:var(--accent);stroke-width:1}.mobile-chart{display:none}figcaption{font-size:.875rem;color:var(--muted);max-width:75ch;margin-top:14px}.table-wrap{max-width:100%;margin:22px 0;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse;font-size:.875rem;font-variant-numeric:tabular-nums}caption{text-align:left;font-size:1rem;font-weight:650;padding-bottom:12px}th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:12px 10px}thead th{font-size:.875rem;color:var(--muted);font-weight:650;border-top:1px solid var(--line);border-bottom:2px solid var(--line)}.baseline{background:var(--wash);font-weight:650}.numeric{text-align:right}.rounding{padding:14px 0;border-bottom:1px solid var(--line)}.assumption-list{padding:0;list-style:none;counter-reset:ledger}.assumption-list li{padding:18px 0;border-bottom:1px solid var(--line)}.assumption-list h3{margin:0 0 7px;display:flex;gap:12px;align-items:baseline}.status{font-weight:600;color:var(--accent);font-size:.875rem;white-space:nowrap}.assumption-list p{margin:0 0 7px}.assumption-list .note{margin:0}.steps{padding-left:23px}.steps li{padding:0 0 16px}.steps strong{display:block}.steps p{margin:4px 0}.glossary{display:grid;grid-template-columns:175px minmax(0,1fr);gap:12px 20px}.glossary dt{font-weight:650}.glossary dd{margin:0}.technical{margin-top:26px;border-top:1px solid var(--line);padding-top:22px}code{font-family:ui-monospace,Consolas,monospace;font-size:.8rem;word-break:break-all}.hashes dt{font-weight:650}.hashes dd{margin:5px 0 16px}.print-button{display:none;border:1px solid var(--accent);background:var(--paper);color:var(--accent);padding:9px 13px;font:inherit;cursor:pointer;font-size:.875rem}.js .print-button{display:block}footer{font-size:.875rem;color:var(--muted);padding-top:30px}.reviewer .layout{display:block;max-width:1030px;padding-top:24px}.reviewer .contents{position:static;border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:32px}.reviewer .contents p{display:none}.reviewer .contents ol{display:flex;gap:10px 22px;flex-wrap:wrap}.reviewer .contents li{margin:0}.reviewer h1{max-width:26ch;font-size:clamp(2rem,4.3vw,3rem)}.reviewer .section{padding:31px 0}.reviewer .scenario{grid-template-columns:190px minmax(0,1fr)}.reviewer .lead{font-size:1.125rem}.reviewer .fact-list{max-width:none}.reviewer .section-number{display:inline-block;margin-right:14px}.reviewer h2{display:inline-block;font-size:1.6rem}.reviewer .evidence{border-top:2px solid var(--accent);padding-top:18px;margin-top:22px}
@media(prefers-color-scheme:dark){:root{--paper:#101922;--ink:#edf2f7;--muted:#b4c2d0;--accent:#8fc6ee;--line:#526476;--wash:#202e3d;--bar1:#8fc6ee;--bar2:#b3c4d6;--bar3:#e1e7ef;--focus:#efb482}}
@media(max-width:800px){.layout{display:block;padding:28px 22px 56px}.contents{position:static;border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:28px}.contents p{margin-bottom:12px}.contents ol{display:flex;flex-wrap:wrap;gap:6px 18px}.contents li{margin:0}.contents span{display:none}.switcher{gap:12px 18px}.switcher strong{width:100%}.reviewer .layout{padding:28px 22px 56px}.fact-list{grid-template-columns:120px minmax(0,1fr);gap:10px 14px}}
@media(max-width:520px){body{font-size:16px}.layout,.reviewer .layout{padding:24px 18px 45px}.contents{font-size:.875rem}.contents ol{gap:8px 14px}.section{padding:30px 0}header{padding-bottom:26px}h1{font-size:2.15rem}h2{font-size:1.5rem}.lead{font-size:1.125rem}.scenario,.reviewer .scenario{display:block}.scenario h3{margin-bottom:10px}.desktop-chart{display:none}.mobile-chart{display:block}.chart{max-width:340px}.fact-list,.glossary{display:block}.fact-list dt,.glossary dt{margin-top:14px;font-weight:650}.fact-list dd,.glossary dd{margin-top:3px}.boundary{padding:10px 4px}.boundary .wide-diagram{display:none}.boundary .narrow-diagram{display:block}.assumption-list h3{display:block}.status{display:block;margin-top:4px}th,td{padding:10px 5px}.result-table{font-size:.875rem}.result-table th:first-child{width:32%}.result-table td{white-space:nowrap}.result-table th{font-size:.875rem}.technical table{font-size:.875rem}.reconcile td{white-space:normal}}
.narrow-diagram{display:none}
@media print{@page{size:A4;margin:15mm 14mm 17mm} :root{color-scheme:light;--paper:#fff;--ink:#172331;--muted:#425265;--accent:#174f78;--line:#9aaaba;--wash:#edf2f6;--bar1:#174f78;--bar2:#536577;--bar3:#a8b7c7}body{font-size:10pt;line-height:1.45;print-color-adjust:exact;-webkit-print-color-adjust:exact}.switcher,.contents,.print-button,.skip{display:none!important}.layout,.reviewer .layout{display:block;padding:0;max-width:none}header{padding-top:0;break-after:page}h1,.reviewer h1{font-size:30pt}h2,.reviewer h2{font-size:19pt}h3{font-size:12pt}p,.note{max-width:none}.section,.reviewer .section{padding:18px 0}.section-number{font-size:9pt}.lead,.reviewer .lead{font-size:12pt}h2,h3{break-after:avoid}figure,table,.boundary,.assumption-list li,.scenario,.steps li,.notice{break-inside:avoid}thead{display:table-header-group}th,td{padding:7px 5px;font-size:9pt}.scenario{gap:12px}.desktop-chart{display:block}.mobile-chart{display:none}.chart{max-width:640px}.section#results,.section#contributions,.section#drivers,.section#assumptions,.section#appendix{break-before:page}footer{font-size:9pt}a{color:inherit;text-decoration:none}.meta,.note,figcaption,.assumption,.status,.legend{font-size:9pt}.technical{break-before:page}.glossary{grid-template-columns:145px 1fr}code{font-size:8pt}}
"""

# Keep the warning in the first mobile viewport and give pale graphic marks enough contrast.
CSS += """
:root{--bar3:#72879b}
.boundary .narrow-diagram{display:none}
@media(prefers-color-scheme:dark){:root{--bar3:#e1e7ef}}
@media(max-width:520px){.contents{display:none!important}.boundary .narrow-diagram{display:block}header{display:flex;flex-direction:column;align-items:flex-start}header .notice{order:1;margin-top:14px}header .meta{order:2}}
@media print{:root{--bar3:#72879b}.boundary .narrow-diagram{display:none!important}.boundary .wide-diagram{display:block!important}header{break-after:auto}#study,#scenarios{break-before:page}.chart{max-width:560px}#results .chart{max-width:520px}#results figure,#results .table-wrap{margin:14px 0}.rounding{padding:8px 0;break-inside:avoid}.section-number{break-after:avoid}.transformations th:last-child,.transformations td:last-child{white-space:nowrap}.transformations code{font-size:8pt}}
"""


def sig3(value: str) -> str:
    number = Decimal(value)
    quantum = Decimal(1).scaleb(number.adjusted() - 2)
    return format(number.quantize(quantum, rounding=ROUND_HALF_UP), "f")


def percent(value: str, baseline: str) -> Decimal:
    return (Decimal(value) - Decimal(baseline)) / Decimal(baseline) * 100


def table(headers, rows, *, caption="", cls=""):
    head = "".join(f'<th scope="col">{x}</th>' for x in headers)
    body = "".join(f'<tr{attrs}>' + f'<th scope="row">{cells[0]}</th>' + "".join(f'<td>{x}</td>' for x in cells[1:]) + "</tr>" for attrs, cells in rows)
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<div class="table-wrap"><table class="{cls}">{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def change_chart(data, mobile=False):
    width = 340 if mobile else 760
    left, zero = (16, 266) if mobile else (20, 649)
    top, step = 60, 126 if mobile else 118
    height = top + step * 4 + 12
    css = "mobile-chart" if mobile else "desktop-chart"
    pieces = [f'<svg class="chart {css}" viewBox="0 0 {width} {height}" role="img" aria-label="Synthetic proxy percentage changes from the 2025 reference. Every future case decreases all three proxies under its proposed conditions. Exact values follow in the appendix.">', '<title>Change from supplied 2025 reference totals</title>']
    for tick in ([-100, -50, 0] if mobile else [-100, -75, -50, -25, 0]):
        x = zero + tick / 100 * (zero - left)
        pieces += [f'<path class="grid" d="M{x} 38V{height-5}"/>', f'<text x="{x}" y="22" text-anchor="{"start" if tick == -100 else "end" if tick == 0 else "middle"}">{tick}%</text>']
    for i, row in enumerate(data["scenarios"][1:]):
        y = top + step * i
        pieces.append(f'<text class="scenario-label" x="{left}" y="{y}">{esc(row["label"])}</text>')
        for j, indicator in enumerate(["climate", "water", "energy"]):
            pct = percent(row["totals"][j], data["scenarios"][0]["totals"][j])
            bar = -float(pct) / 100 * (zero - left)
            by = y + 14 + j * 25
            pieces += [f'<rect class="{indicator}" x="{zero-bar:.3f}" y="{by}" width="{bar:.3f}" height="15"/>', f'<text class="pct" x="{zero+8}" y="{by+13}">{pct:.2f}%</text>']
    pieces.append("</svg>")
    return "".join(pieces)


def contributions_chart(data, mobile=False):
    width = 340 if mobile else 760
    zero, right = (65, 257) if mobile else (100, 660)
    scale = (right - zero) / 180
    step = 76 if mobile else 67
    height = 58 + 6 * step
    css = "mobile-chart" if mobile else "desktop-chart"
    hatch = "credit-hatch-mobile" if mobile else "credit-hatch-desktop"
    pieces = [f'<svg class="chart {css}" viewBox="0 0 {width} {height}" role="img" aria-label="Baseline climate proxy contributions in kg carbon dioxide equivalent per tonne. Grid electricity 176.4; process heat 45; fertiliser credit minus 17.5; transport 14.4; enzyme 2.88; water 0.00084. Credit extends left of zero.">', '<title>Signed baseline climate proxy contributions</title>', f'<defs><pattern id="{hatch}" patternUnits="userSpaceOnUse" width="6" height="6"><path d="M-1 1L1 -1M0 6L6 0M5 7L7 5" stroke="var(--accent)" stroke-width="1.5"/></pattern></defs>']
    for tick in [-20, 0, 60, 120, 180]:
        x = zero + tick * scale
        pieces += [f'<path class="grid" d="M{x} 38V{height}"/>', f'<text x="{x}" y="22" text-anchor="middle">{tick}</text>']
    for i, row in enumerate(data["baseline_climate_contributions"]):
        val = float(row["value"])
        y = 61 + step * i
        x = zero + min(0, val) * scale
        bar = abs(val) * scale
        label = "Fertiliser credit (subtraction)" if val < 0 else row["label"]
        fill = f' style="fill:url(#{hatch})"' if val < 0 else ""
        pieces += [f'<text x="16" y="{y}">{esc(label)}</text>', f'<rect class="{"credit" if val < 0 else "climate"}"{fill} x="{x:.5f}" y="{y+12}" width="{bar:.5f}" height="16"/>', f'<text x="{right+6}" y="{y+26}">{esc(row["value"])}</text>']
    pieces.append("</svg>")
    return "".join(pieces)


def boundary():
    return """<figure class="boundary"><svg class="wide-diagram" viewBox="0 0 690 265" role="img" aria-label="One tonne of wet pomace enters conversion. Electricity, heat, water, enzyme and transport supply the process. Recovered outputs are unspecified. An assumed avoided-fertiliser credit is subtracted. Cultivation and current pomace treatment are outside this defined boundary."><rect x="216" y="10" width="258" height="66"/><text x="345" y="37" text-anchor="middle">Electricity · heat · water</text><text x="345" y="59" text-anchor="middle">Enzyme · transport</text><path d="M345 76V111m-5 -7l5 7l5 -7"/><rect x="6" y="113" width="180" height="66"/><text x="96" y="140" text-anchor="middle">1 tonne wet pomace</text><text x="96" y="161" text-anchor="middle">at the process gate</text><path d="M186 146h30m-7 -5l7 5l-7 5"/><rect class="core" x="216" y="113" width="258" height="66"/><text x="345" y="142" text-anchor="middle">Conversion process</text><text x="345" y="163" text-anchor="middle">Gate-to-gate</text><path d="M474 146h30m-7 -5l7 5l-7 5"/><rect x="504" y="113" width="180" height="66"/><text x="594" y="140" text-anchor="middle">Recovered outputs</text><text x="594" y="161" text-anchor="middle">yields unspecified</text><path d="M345 179V206m-5 -7l5 7l5 -7"/><text x="345" y="231" text-anchor="middle">Avoided mineral-fertiliser credit</text><text x="345" y="253" text-anchor="middle">Assumed subtraction; evidence needed</text></svg><svg class="narrow-diagram" viewBox="0 0 330 420" role="img" aria-label="Wet pomace and electricity, heat, water, enzyme and transport enter the conversion process. Recovered outputs have unspecified yields. An assumed fertiliser credit is subtracted."><rect x="15" y="10" width="300" height="68"/><text x="165" y="36" text-anchor="middle">1 tonne wet pomace at the gate</text><text x="165" y="58" text-anchor="middle">Electricity · heat · water</text><text x="165" y="76" text-anchor="middle">Enzyme · transport</text><path d="M165 78v42m-5 -7l5 7l5 -7"/><rect class="core" x="15" y="120" width="300" height="64"/><text x="165" y="147" text-anchor="middle">Conversion process</text><text x="165" y="169" text-anchor="middle">Gate-to-gate</text><path d="M165 184v40m-5 -7l5 7l5 -7"/><rect x="15" y="224" width="300" height="64"/><text x="165" y="251" text-anchor="middle">Recovered outputs</text><text x="165" y="273" text-anchor="middle">Yields unspecified</text><path d="M165 288v40m-5 -7l5 7l5 -7"/><text x="165" y="350" text-anchor="middle">Avoided mineral-fertiliser credit</text><text x="165" y="376" text-anchor="middle">Assumed subtraction</text><text x="165" y="400" text-anchor="middle">Evidence needed</text></svg><figcaption>The current fate of pomace, crop cultivation, complete product life cycles and output yields are not defined in this narrow demonstration.</figcaption></figure>"""


def decomposition(project, run):
    baseline = next(r for r in run["results"] if r["scenario_id"] == project.baseline_scenario_id)
    base = baseline["impacts"][CATEGORIES[0]]
    rows, raw = [], []
    for scenario in project.scenarios:
        if scenario.id == project.baseline_scenario_id:
            continue
        quantity_case = replace(scenario, transformations=[t for t in scenario.transformations if t.operation.endswith("quantity")])
        intermediate, _ = calculate_scenario(project, quantity_case)
        final, _ = calculate_scenario(project, scenario)
        mid, total = intermediate.impacts[CATEGORIES[0]], final.impacts[CATEGORIES[0]]
        values = [base, mid, total, mid - base, total - mid]
        raw.append({"scenario_id": scenario.id, "baseline": base, "quantity_only": mid, "full": total,
                    "process_quantity_change": mid - base, "background_factor_change": total - mid})
        rows.append(("", [esc(scenario.name.replace(" pathway", ""))] + [f"{x:.4f}" for x in values]))
    return table(["Synthetic case", "Reference", "Process only", "Combined", "Process change", "Factor change"], rows,
                 caption="Ordered climate-proxy decomposition · kg CO2e per tonne", cls="decomposition"), raw


def narratives(project, reviewer=False):
    extra = " All quantities and factors are synthetic and proposed." if reviewer else ""
    content = [f'<div class="scenario"><h3>Reference · 2025</h3><div><p>The original synthetic process uses 420 kWh of electricity and 180 kWh of heat per tonne of wet pomace.</p><p class="condition">Electricity climate factor: 0.42 kg CO2e/kWh. This is an illustrative factor, not a measured Portuguese grid value.{extra}</p></div></div>']
    for scenario in project.scenarios[1:]:
        changes = {t.target: t.value for t in scenario.transformations}
        changes_list = [("electricity_grid", "electricity"), ("process_heat", "heat"), ("process_water", "water"), ("enzymes", "enzyme"), ("feedstock_transport", "transport activity")]
        amounts = [f'{(1-Decimal(str(changes[item+":quantity"])))*100:g}% less {label}' for item, label in changes_list]
        credit = (Decimal(str(changes["avoided_fertiliser:quantity"])) - 1) * 100
        body = "; ".join(amounts) + f"; {credit:g}% larger assumed fertiliser credit."
        factor = changes["electricity_grid:climate_change_kg_co2e"]
        water = changes["electricity_grid:water_consumption_m3"]
        background = f"Electricity climate factor changes to {factor:g} kg CO2e/kWh; its water factor changes to {water:g} m3/kWh."
        if "process_heat:climate_change_kg_co2e" in changes:
            background += " Heat climate factor also changes from 0.25 to 0.18 kg CO2e/kWh."
        content.append(f'<div class="scenario"><h3>{esc(scenario.name.replace(" pathway", ""))}</h3><div><p><strong>Process conditions.</strong> {body}</p><p class="condition"><strong>Supply conditions.</strong> {background}{extra}</p></div></div>')
    return "".join(content)


def assumption_ledger(project):
    statements = [
        ("Study purpose", "This example demonstrates a workflow. It does not answer a customer's investment question."),
        ("Common reference", "Compare the processing of one tonne of wet grape pomace. Moisture and product quality still need to be specified for a real study."),
        ("Study boundary", "Include conversion, electricity, heat, water, enzyme, transport and an assumed fertiliser credit. Agree a full comparison boundary before the pilot."),
        ("Modelling approach", "The source calls this an attributional demonstration. The appropriate approach and use of avoided burdens remain unresolved for a real pilot."),
        ("Electricity supply", "Change the synthetic electricity factors by case and year. Select documented, approved background data for a real study."),
        ("Process scale-up", "Use simple multipliers for process quantities. Replace these with engineering evidence, scale and yield assumptions."),
        ("Fertiliser credit", "Subtract an assumed avoided mineral-fertiliser burden. Confirm the displaced product, nutrient equivalence and co-product treatment."),
        ("Impact indicators", "Use original illustrative climate, water-use and primary-energy proxies. Select an approved life-cycle impact assessment method for the pilot.")]
    parts = []
    for choice, (title, statement) in zip(project.choices, statements):
        parts.append(f'<li><h3>{title}<span class="status">{esc(choice.status.value.title())}</span></h3><p>{statement}</p><p class="note">Responsible owner: to confirm. Source: {esc(choice.source)}. Recorded by: {esc(choice.author)}; this does not indicate approval.</p></li>')
    return '<ol class="assumption-list">' + "".join(parts) + "</ol>"


def appendix(data, project, run, manifest, data_hash, reviewer):
    glossary = [
        ("Life-cycle assessment (LCA)", "An assessment of environmental burdens across the defined stages of a product or process."),
        ("Prospective", "Conditional future cases. They are neither forecasts nor probabilities."),
        ("Functional unit (FU)", "The common reference used to compare cases; here, one tonne of wet pomace processed."),
        ("Foreground", "Process quantities and operating choices."), ("Background", "Supplying systems and the factors used for their burdens."),
        ("Proxy", "A demonstration indicator used in place of an approved assessment."),
        ("Life-cycle impact assessment (LCIA)", "Converting inventory flows into indicators with a specified method."),
        ("Credit", "A modelled subtraction for an avoided activity. It needs evidence and an agreed comparison."),
        ("Counterfactual", "What would happen without the proposed process, including the current pomace treatment."),
        ("CO2e", "Carbon dioxide equivalent, the unit used here for the illustrative climate indicator."),
        ("kWh / MJ / m3", "Kilowatt-hours / megajoules / cubic metres."),
        ("Allocation", "Rules for assigning burdens to multiple products or functions.")]
    terms = '<dl class="glossary">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in glossary) + "</dl>"
    exact = table(["Synthetic case", "Climate (kg CO2e)", "Water (m3)", "Energy (MJ)"],
                  [("", [esc(row["label"])] + row["totals"]) for row in data["scenarios"]], caption="Exact supplied totals · per tonne of wet pomace")
    reconciliation = []
    for row in data["scenarios"][1:]:
        for j, indicator in enumerate(INDICATORS):
            computed = percent(row["totals"][j], data["scenarios"][0]["totals"][j])
            delta = computed - Decimal(row["supplied_percent"][j])
            reconciliation.append(("", [esc(row["label"]) + "<br>" + indicator, row["supplied_percent"][j] + "%", f"{computed:.2f}%", f"{delta:+.4f}"]))
    recon = table(["Case / indicator", "Supplied", "Recomputed", "Difference (points)"], reconciliation,
                  caption="Supplied versus recomputed changes", cls="reconcile")
    identifiers = table(["Case", "Source identifier"], [("", [esc(r["label"]), f'<code>{esc(r["id"])}</code>']) for r in data["scenarios"]])
    ids = "<p>Ledger identifiers: " + "; ".join(f"<code>{esc(c.id)}</code>" for c in project.choices) + ".</p>"
    hashes = "".join(f'<dt>{label}</dt><dd><code>{esc(str(manifest[key]))}</code></dd>' for key, label in [("run_uuid", "Calculation run ID"), ("input_manifest_hash", "Calculation input fingerprint"), ("assumption_ledger_hash", "Calculation assumption-ledger fingerprint"), ("result_artifact_hash", "Calculation result fingerprint")])
    validation = manifest["validation"]
    transform_rows = []
    for s in project.scenarios:
        for t in s.transformations:
            transform_rows.append(("", [esc(s.name), f'<code>{esc(t.target)}</code>', esc(t.formula), esc(t.evidence_source), esc(t.approval_state.value)]))
    transforms = "".join(table(["Input target", "Transformation", "Source", "Status"],
        [("", row[1][1:]) for row in transform_rows if row[1][0] == esc(s.name)],
        caption=f"Original transformations · {esc(s.name)}", cls="transformations") for s in project.scenarios[1:])
    return f"""<h3>Plain-language glossary</h3>{terms}
<div class="technical"><h3>Exact figures and rounding</h3><p>The main table uses three significant figures, rounded to nearest with ties away from zero: for example, 221.2 becomes 221, 166.5 becomes 167, 1.800 becomes 1.80 and 2363 becomes 2360. No source value is replaced. The chart uses two-decimal percentages computed from the exact supplied display totals below.</p>{exact}
<p class="note">Change = (future total − reference total) ÷ reference total × 100. The supplied percentages appear to have used finer source precision; that is an inference from the repository's calculation output, not a change to the supplied dataset. Differences below compare the unrounded recomputation with the supplied percentage, in percentage points.</p>{recon}
<p>Exact supplied contribution labels: {"; ".join(esc(x["label"]) + " " + x["value"] for x in data["baseline_climate_contributions"])} kg CO2e per tonne. Their arithmetic sum is <strong>221.18084</strong>; the brief reports the rounded sum as <strong>221.18</strong> and the headline total as <strong>221.2</strong>.</p>
<h3>Source identifiers</h3>{identifiers}{ids}<p>Project ID: <code>{esc(project.id)}</code>. Engine: AWAM Prospective LCA Workbench {esc(manifest["application_version"])}. Preview document version: {VERSION}.</p>
<h3>Reproducibility and software checks</h3><dl class="hashes">{hashes}<dt>Preview display-data fingerprint (SHA-256)</dt><dd><code>{data_hash}</code></dd></dl>
<p>The calculation fingerprints refer to the repository run, including its full-precision results. They do not certify the rounded display dataset or these HTML documents. A separate preview manifest records each HTML file's SHA-256 fingerprint. Licensed data included: <strong>{str(manifest["database"]["licensed_data_included"]).lower()}</strong>.</p>
<p>Automated consistency checks only, not scientific verification: {validation["error_count"]} errors and {validation["warning_count"]} warnings in demonstration mode. All eight scientific ledger choices remain proposed. No scientist approval, independent verification, critical review or ISO compliance is claimed.</p>
<h3>Evidence register</h3><ul><li>Preview display totals, percentages and contributions: supplied customer-report brief.</li><li>Process quantities, factors and scenario multipliers: original synthetic project definition, <code>demo/sample_project/project.json</code>.</li><li>Assumption statements and statuses: Synthetic demonstration design note, as recorded in that project file.</li><li>Decomposition: calculated here from those existing synthetic transformations, process quantities first and factors second.</li></ul>
<p class="assumption">[ASSUMPTION] English, no supplied branding, customer identity and decision unspecified. Customer version explains terms for a new reader; methods version assumes a technical reviewer. Scientific owner and author/contact details remain to be confirmed.</p>
<h3>Transformation detail</h3>{transforms}</div>"""


def render(data, project, run, manifest, mode, data_hash, root=False):
    reviewer = mode == "reviewer"
    name = "Methods review" if reviewer else "Customer report"
    other = "Customer report" if reviewer else "Methods review"
    target = "customer/index.html" if reviewer else "reviewer/index.html"
    other_href = target if root else "../" + target
    toc = "".join(f'<li><a href="#{key}"><span>{i:02d}</span>{label}</a></li>' for i, (key, label) in enumerate(SECTIONS, 1))
    title = "Grape pomace: methods & evidence review" if reviewer else "Grape pomace: a prospective study preview"
    summary = "This document shows how a prospective life-cycle assessment (LCA) could compare grape-pomace processing in Portugal in 2025, 2030 and 2040. The numbers are synthetic placeholders and use illustrative proxies, rather than an approved life-cycle impact assessment (LCIA) method. A customer-specific study needs measured process data, an agreed comparison and reviewed modelling choices before it can inform a decision."
    total_rows = [((' class="baseline"' if i == 0 else ""), [esc(row["label"])] + [sig3(x) for x in row["totals"]]) for i, row in enumerate(data["scenarios"])]
    totals = table(["Synthetic case", "Climate proxy<br>(kg CO2e)", "Water proxy<br>(m3)", "Primary energy proxy<br>(MJ)"], total_rows, caption="Illustrative totals · per tonne of wet pomace", cls="result-table")
    driver_table, _ = decomposition(project, run)
    if reviewer:
        review_note = '<div class="evidence"><strong>Evidence status</strong><p>One original synthetic inventory; five conditional cases; eight proposed choices. The current pomace treatment, product yields, customer decision, real database and approved impact method are unresolved.</p></div>'
    else:
        review_note = ""
    sections = {
        "summary": f'<p class="lead">{summary}</p>{review_note}',
        "study": f'''<p>The purpose is to demonstrate a traceable comparison of future process and supply conditions. It is not a study of a named customer's operation.</p><dl class="fact-list"><dt>Common reference</dt><dd>1 tonne of wet grape pomace processed. This is the functional unit: the same amount is compared in every case.</dd><dt>Location</dt><dd>Portugal.</dd><dt>Time</dt><dd>Reference year 2025; conditional future years 2030 and 2040.</dd><dt>Included stages</dt><dd>Conversion at the processing facility, electricity, process heat, water, enzyme, transport and an assumed avoided mineral-fertiliser credit.</dd><dt>Unresolved comparison</dt><dd>The current fate of pomace and the displaced products have not been specified.</dd></dl>{boundary()}''',
        "scenarios": f'<p>These are conditional combinations of process quantities and supplying-system factors. Their labels do not identify verified Portuguese grid projections or describe how likely a case is.</p>{narratives(project, reviewer)}<p class="note">Every multiplier and factor remains a proposed synthetic assumption. Water volumes do not measure local water scarcity; the primary-energy proxy lacks an approved accounting basis.</p>',
        "results": f'''<p>Read each change against the same 2025 reference and the conditions above. Lower proxy totals in this demonstration do not establish technology feasibility or an environmental advantage for a real plant.</p><div class="legend"><span><i class="swatch" aria-hidden="true"></i>Climate proxy</span><span><i class="swatch water" aria-hidden="true"></i>Water proxy</span><span><i class="swatch energy" aria-hidden="true"></i>Primary energy proxy</span></div><figure>{change_chart(data)}{change_chart(data, True)}<figcaption>Percentage change from the supplied 2025 totals. Bars extend left from 0%; the three bars in every group follow the legend order. All values use illustrative inputs and proxies.</figcaption></figure>{totals}<p class="note rounding"><strong>Rounding disclosure.</strong> Totals above use three significant figures; chart labels use two decimal places. Supplied percentages and recomputations differ slightly because the display totals are rounded. Exact supplied figures, original percentages and the arithmetic comparison are preserved in the appendix.</p>''',
        "contributions": f'''<p>Electricity is the largest positive climate-proxy contribution in the synthetic reference case. The fertiliser credit is a subtraction that depends on an unconfirmed substitution assumption.</p><figure>{contributions_chart(data)}{contributions_chart(data, True)}<figcaption>Climate proxy · kg CO2e per tonne of wet pomace. Positive burdens extend right of zero; the hatched credit extends left. Water's 0.00084 contribution is labelled exactly and its bar is not exaggerated.</figcaption></figure><p class="note">The six supplied contributions sum to 221.18084; the supplied rounded sum is 221.18 and the supplied headline total is 221.2. The credit reduces the illustrative total but does not demonstrate actual fertiliser displacement.</p>''',
        "drivers": f'''<p><strong>Process changes</strong> alter electricity, heat, water, enzyme, transport and assumed recovery quantities. <strong>Background changes</strong> alter the factors used for electricity supply and, in the ambitious case, heat supply.</p><p>The existing synthetic model allows a separate arithmetic check: change process quantities first while retaining reference factors, then change supply factors. This gives the following climate-proxy decomposition.</p>{driver_table}<p class="note">All columns are derived from the original synthetic model, rounded here to four decimal places for reconciliation. “Process change” = process-only minus reference; “factor change” = combined minus process-only. Their sum equals combined minus reference before rounding. This order assigns the quantity–factor interaction to the factor step; reversing the order changes the split. This is an illustrative causal accounting choice, not scientific validation.</p><p class="note">The table uses full-precision model totals, separate from the fixed supplied display totals. Heat-factor change is included in the final column for the ambitious case. Item labels such as foreground/background in the source inventory are not treated as proof of what caused a reduction.</p><p>For a real decomposition, provide scenario-specific process quantities, yields and uncertainty ranges; matched electricity and heat datasets with provenance, year and geography; and an agreed method for reporting interactions and credits.</p>''',
        "assumptions": '<p>All eight entries remain proposed. The sentences below clarify the recorded values without changing their source status or inventing approval.</p>' + assumption_ledger(project),
        "limitations": '''<div class="notice"><strong>Synthetic demonstration — not for scientific or external decision-making.</strong><p>Climate, water-use and primary-energy values are illustrative proxies. They are not results from an approved LCIA method.</p></div><ul><li>No confirmed customer goal, measured plant inventory, output mass balance or product quality definition.</li><li>No agreed current-pomace-treatment comparison, allocation rule or evidence of fertiliser substitution.</li><li>No approved inventory database, documented future grid scenario or reviewed impact method.</li><li>No uncertainty analysis, sensitivity ranges or independent data-quality review.</li><li>Software checks test consistency. They do not establish scientific validity, ISO compliance or feasibility.</li></ul><p>A decision study needs these gaps resolved, with an accountable scientific owner reviewing the model, calculations and interpretation. The narrow demonstration boundary cannot support a claim about the complete product life cycle.</p>''',
        "next": '''<p>Start with a short pilot definition, then collect records for the same reference flow. Do not infer missing quantities from these example results.</p><ol class="steps"><li><strong>Agree the question and comparison.</strong><p>Provide the customer name, decision, decision date, current pomace treatment, alternative process and intended products. Confirm moisture, quality and the study boundary.</p></li><li><strong>Supply measured operating records.</strong><p>Electricity and heat demand; heat source; water intake and discharge; enzyme dose; incoming and outgoing mass, moisture and yields; seasonal throughput; transport mass and distance. Give units, measurement dates, source files and uncertainty ranges.</p></li><li><strong>Resolve recovery and substitution.</strong><p>Provide product composition, nutrient equivalence, market/use conditions and evidence of what the recovered output actually displaces. Agree allocation and whether any avoided-burden credit is appropriate.</p></li><li><strong>Choose future conditions and methods.</strong><p>Document process scale-up, engineering changes, background datasets, versions, geographic coverage, years and an approved impact method. Record who owns and reviews each choice.</p></li><li><strong>Review before communicating results.</strong><p>Check mass and energy balances, independently reconcile calculations, test key assumptions and uncertainty, and agree what can be claimed. Fill customer, author and contact details before sharing even this demonstration.</p></li></ol>''',
        "appendix": appendix(data, project, run, manifest, data_hash, reviewer)
    }
    labels = dict(SECTIONS)
    body = "".join(f'<section class="section" id="{key}" aria-labelledby="heading-{key}"><span class="section-number">{i:02d}</span><h2 id="heading-{key}">{labels[key]}</h2>{sections[key]}</section>' for i, (key, _) in enumerate(SECTIONS, 1))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Synthetic grape-pomace methodology preview. Illustrative inputs and proxies; not for scientific or external decision-making."><title>{title} | {name}</title><style>{CSS}</style></head>
<body class="{mode}"><a class="skip" href="#main">Skip to report</a><nav class="switcher" aria-label="Report versions"><strong>Prospective assessment · methodology preview</strong><a href="#main" aria-current="page">{name}</a><a href="{other_href}">{other}</a><button class="print-button" type="button" id="print-report">Print / save PDF</button></nav><div class="layout"><nav class="contents" aria-label="Report contents"><p>In this document</p><ol>{toc}</ol></nav><main id="main"><header><span class="badge">Illustrative · synthetic inputs</span><div class="eyebrow">{name}</div><h1>{title}</h1><p class="subtitle">Methodology preview and workflow demonstration</p><p class="meta">{DATE} · Document {VERSION}<br>Customer: [Name to confirm] · Author: [Author to confirm]<br>Contact: [Contact to confirm]</p><div class="notice"><strong>Synthetic demonstration — not for scientific or external decision-making.</strong><p>Illustrative climate, water-use and primary-energy proxies; not an approved life-cycle impact assessment method.</p></div></header>{body}<footer>Prepared as a workflow demonstration. Scientific owner and communication approval remain to be confirmed.</footer></main></div><script>document.documentElement.classList.add('js');document.getElementById('print-report').addEventListener('click',function(){{window.print()}});</script></body></html>'''


def build(package):
    data_bytes = DATA_PATH.read_bytes()
    data = json.loads(data_bytes)
    project = load_project(ROOT / "demo" / "sample_project" / "project.json")
    run = json.loads((package / "run.json").read_text(encoding="utf-8"))
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    data_hash = hashlib.sha256(data_bytes).hexdigest()
    # Refuse to attach source fingerprints to a different project/scenario package.
    if run["project"] != project.to_dict() or manifest["scenario_ids"] != [s.id for s in project.scenarios]:
        raise ValueError("Preview requires the unchanged full synthetic project package")
    output_hashes = {}
    for mode in ["customer", "reviewer"]:
        target = package / mode / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        contents = render(data, project, run, manifest, mode, data_hash)
        target.write_text(contents, encoding="utf-8", newline="\n")
        output_hashes[f"{mode}/index.html"] = hashlib.sha256(target.read_bytes()).hexdigest()
    homepage = package / "index.html"
    homepage.write_text(render(data, project, run, manifest, "customer", data_hash, root=True), encoding="utf-8", newline="\n")
    output_hashes["index.html"] = hashlib.sha256(homepage.read_bytes()).hexdigest()
    _, driver_data = decomposition(project, run)
    (package / "preview-manifest.json").write_text(json.dumps({"document_version": VERSION, "date": DATE,
        "display_data_sha256": data_hash, "html_sha256": output_hashes, "source_calculation_manifest": "manifest.json",
        "decomposition_order": "process quantities first; supplying-system factors second",
        "derived_decomposition": driver_data}, indent=2) + "\n", encoding="utf-8")
    print("Built customer and methods-review previews; source calculation report retained as report.html")
    for path in output_hashes:
        print(f"{path}: {(package / path).stat().st_size:,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True, help="Existing full synthetic demo export directory")
    build(parser.parse_args().package)
