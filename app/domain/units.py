"""Small, explicit unit registry for the offline vertical slice.

This is intentionally not marketed as a complete LCA unit ontology.  It covers
the units used by the synthetic demonstration and fails closed for unknown or
incompatible conversions.  AWAM's real pilot should confirm the approved flow
and unit mappings before connecting licensed data.
"""

from __future__ import annotations

from dataclasses import dataclass


class UnitError(ValueError):
    """Raised when a quantity cannot be safely converted."""


@dataclass(frozen=True)
class UnitDefinition:
    dimension: str
    to_base: float


_UNITS: dict[str, UnitDefinition] = {
    "kg": UnitDefinition("mass", 1.0),
    "t": UnitDefinition("mass", 1000.0),
    "g": UnitDefinition("mass", 0.001),
    "MJ": UnitDefinition("energy", 1.0),
    "kWh": UnitDefinition("energy", 3.6),
    "m3": UnitDefinition("volume", 1.0),
    "L": UnitDefinition("volume", 0.001),
    "km": UnitDefinition("distance", 1.0),
    "t*km": UnitDefinition("transport", 1.0),
    "kg*km": UnitDefinition("transport", 0.001),
    "unit": UnitDefinition("count", 1.0),
}


def normalize_unit(unit: str) -> str:
    """Return a canonical spelling or raise for an unknown unit."""

    clean = unit.strip()
    aliases = {"m^3": "m3", "kilogram": "kg", "tonne": "t", "kwh": "kWh"}
    clean = aliases.get(clean, clean)
    if clean not in _UNITS:
        raise UnitError(f"Unknown unit: {unit!r}")
    return clean


def compatible(left: str, right: str) -> bool:
    """Whether two units belong to the same dimension."""

    try:
        return _UNITS[normalize_unit(left)].dimension == _UNITS[normalize_unit(right)].dimension
    except UnitError:
        return False


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between known units in the same dimension."""

    source = _UNITS[normalize_unit(from_unit)]
    target = _UNITS[normalize_unit(to_unit)]
    if source.dimension != target.dimension:
        raise UnitError(f"Incompatible units: {from_unit} -> {to_unit}")
    return value * source.to_base / target.to_base


def assert_quantity(value: float, unit: str, *, allow_negative: bool = False) -> None:
    """Validate a scalar quantity and its unit."""

    normalize_unit(unit)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise UnitError(f"Quantity must be numeric, got {value!r}")
    if not allow_negative and value < 0:
        raise UnitError(f"Quantity must be non-negative, got {value}")

