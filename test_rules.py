from rules import assess_product

def test_safe_product():
    product = {
        "ProductID": "TEST-001",
        "ExpiryDate": "2999-12-31",
        "MinTempC": 2,
        "MaxTempC": 8,
        "MaxRelativeHumidity": 70,
        "MinPressureHpa": None,
        "MaxPressureHpa": None,
        "Hazardous": False,
    }
    weather = {
        "temperature_c": 5,
        "relative_humidity": 50,
        "surface_pressure_hpa": 1005,
    }

    result = assess_product(product, weather)

    assert result["status"] == "WITHIN_DOCUMENTED_LIMITS"

def test_temperature_exception():
    product = {
        "ProductID": "TEST-002",
        "ExpiryDate": "2999-12-31",
        "MinTempC": 2,
        "MaxTempC": 8,
        "MaxRelativeHumidity": 70,
        "MinPressureHpa": None,
        "MaxPressureHpa": None,
        "Hazardous": False,
    }
    weather = {
        "temperature_c": 35,
        "relative_humidity": 50,
        "surface_pressure_hpa": 1005,
    }

    result = assess_product(product, weather)

    assert result["temperature_ok"] is False
    assert result["status"] == "OUTSIDE_DOCUMENTED_LIMITS"
