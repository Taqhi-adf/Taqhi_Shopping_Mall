def test_weather_shape():
    sample = {
        "temperature_c": 32.0,
        "relative_humidity": 55,
        "surface_pressure_hpa": 1006,
        "wind_speed_kmh": 10,
        "precipitation_mm": 0,
        "weather_code": 1,
    }

    assert isinstance(sample["temperature_c"], (int, float))
    assert isinstance(sample["relative_humidity"], (int, float))
    assert isinstance(sample["surface_pressure_hpa"], (int, float))
