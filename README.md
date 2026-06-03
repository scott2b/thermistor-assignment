# Assignment: Thermistor Measurement Pipeline

Implement the measurement functions for an NTC thermistor using the precision resistor excitation method.

## Setup

```bash
pip install numpy pytest
```

## Instructions

Edit `thermistor.py` and implement the four functions. Each function has a docstring explaining what to do.

Run the tests locally before pushing:

```bash
pytest test_thermistor.py -v
```

## Grading

Push your completed `thermistor.py` to this repo. GitHub Actions will run the test suite automatically. Check the Actions tab for your results.

| Test | Points |
|------|--------|
| `test_calculate_current` | 20 |
| `test_calculate_resistance` | 20 |
| `test_beta_temperature` | 30 |
| `test_self_heating` | 10 |
| `test_full_pipeline` | 20 |
| **Total** | **100** |
