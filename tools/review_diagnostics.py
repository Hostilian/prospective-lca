"""Deterministic review checks for the fixed synthetic demonstration."""

from dataclasses import replace

from app.services.engine import calculate_scenario

CLIMATE = "climate_change_kg_co2e"


def review_diagnostics(project):
    """Expose credit dependence and the quantity/factor interaction.

    Credit removal is an arithmetic stress case, not an alternative treatment
    system or a probability distribution. No inventory or headline is changed.
    """
    results = {s.id: calculate_scenario(project, s)[0] for s in project.scenarios}
    baseline = results[project.baseline_scenario_id]
    reference = baseline.impacts[CLIMATE]
    reference_credit = sum(c.impact for c in baseline.contributions if c.category == CLIMATE and c.is_credit)
    gross_reference = reference - reference_credit
    credits, interactions = [], []
    for scenario in project.scenarios:
        result = results[scenario.id]
        net = result.impacts[CLIMATE]
        credit = sum(c.impact for c in result.contributions if c.category == CLIMATE and c.is_credit)
        gross = net - credit
        credits.append({"scenario_id": scenario.id, "net": net, "signed_credit": credit,
                        "half_credit": gross + 0.5 * credit, "zero_credit": gross,
                        "zero_credit_change_percent": (gross - gross_reference) / gross_reference * 100})
        if scenario.id == project.baseline_scenario_id:
            continue
        quantity_case = replace(scenario, transformations=[t for t in scenario.transformations if t.operation.endswith("quantity")])
        factor_case = replace(scenario, transformations=[t for t in scenario.transformations if t.operation.endswith("factor")])
        quantity = calculate_scenario(project, quantity_case)[0].impacts[CLIMATE]
        factor = calculate_scenario(project, factor_case)[0].impacts[CLIMATE]
        interactions.append({"scenario_id": scenario.id, "reference": reference, "combined": net,
                             "quantity_only": quantity, "factor_only": factor,
                             "quantity_first": quantity - reference, "factor_after_quantity": net - quantity,
                             "factor_first": factor - reference, "quantity_after_factor": net - factor,
                             "interaction": net - quantity - factor + reference})
    return {"schema_version": 1, "category": CLIMATE, "unit": "kg CO2e per tonne of wet pomace",
            "status": "Synthetic arithmetic diagnostics; no scientific approval or uncertainty distribution.",
            "credit_stress": credits, "order_check": interactions}
