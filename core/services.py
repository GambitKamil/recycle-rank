from decimal import Decimal

COEFFICIENTS = {
    "metal": Decimal("5.0"),
    "ewaste": Decimal("6.0"),
    "plastic": Decimal("3.0"),
    "glass": Decimal("2.0"),
    "paper": Decimal("1.5"),
    "organic": Decimal("1.0"),
}

def coef(category: str) -> Decimal:
    return COEFFICIENTS.get(category, Decimal("1.0"))
