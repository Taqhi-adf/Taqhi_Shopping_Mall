from datetime import date

def in_range(value, minimum=None, maximum=None):
    if value is None:
        return None
    if minimum is not None and value < minimum:
        return False
    if maximum is not None and value > maximum:
        return False
    return True

def assess_product(product: dict, weather: dict) -> dict:
    expiry = product.get("ExpiryDate")
    expiry_ok = True
    if expiry:
        expiry_date = expiry if isinstance(expiry, date) else date.fromisoformat(str(expiry))
        expiry_ok = expiry_date >= date.today()

    temp_ok = in_range(
        weather.get("temperature_c"),
        product.get("MinTempC"),
        product.get("MaxTempC"),
    )
    humidity_ok = in_range(
        weather.get("relative_humidity"),
        None,
        product.get("MaxRelativeHumidity"),
    )

    pressure_has_limits = (
        product.get("MinPressureHpa") is not None
        or product.get("MaxPressureHpa") is not None
    )
    pressure_ok = (
        in_range(
            weather.get("surface_pressure_hpa"),
            product.get("MinPressureHpa"),
            product.get("MaxPressureHpa"),
        )
        if pressure_has_limits else None
    )

    checks = [expiry_ok, temp_ok, humidity_ok]
    if pressure_ok is not None:
        checks.append(pressure_ok)

    if not expiry_ok:
        status = "DO_NOT_RELEASE"
        risk = "HIGH"
    elif any(x is False for x in checks):
        status = "OUTSIDE_DOCUMENTED_LIMITS"
        risk = "HIGH" if product.get("Hazardous") else "MEDIUM"
    else:
        status = "WITHIN_DOCUMENTED_LIMITS"
        risk = "LOW"

    return {
        "product_id": product["ProductID"],
        "expiry_ok": expiry_ok,
        "temperature_ok": temp_ok,
        "humidity_ok": humidity_ok,
        "pressure_ok": pressure_ok,
        "risk_level": risk,
        "status": status,
        "reason": (
            "Deterministic comparison of live environmental measurements and "
            "documented demo limits. Real operations must use approved specifications."
        ),
    }
