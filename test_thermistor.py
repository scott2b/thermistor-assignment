"""Autograded tests for thermistor assignment.

Note: These tests verify correct implementation of the equations from
Lecture 2. The expected values are derived from the beta equation with
R0=10kΩ, T0=25°C, β=3890K. Seeing the expected values doesn't help
you skip the implementation — you still need to write the code.
"""

import pytest
import numpy as np
from thermistor import (
    calculate_current,
    calculate_resistance,
    beta_temperature,
    self_heating_error,
    measure_temperature,
)


class TestCalculateCurrent:
    """20 points"""

    def test_basic(self):
        assert abs(calculate_current(1.25) - 0.000125) < 1e-9

    def test_different_voltage(self):
        assert abs(calculate_current(0.5) - 0.00005) < 1e-9

    def test_custom_resistor(self):
        assert abs(calculate_current(1.0, r_prec=20000) - 0.00005) < 1e-9


class TestCalculateResistance:
    """20 points"""

    def test_basic(self):
        assert abs(calculate_resistance(0.625, 0.000125) - 5000) < 1

    def test_equal_resistances(self):
        i = calculate_current(0.5)
        r = calculate_resistance(0.5, i)
        assert abs(r - 10000) < 1

    def test_high_resistance(self):
        r = calculate_resistance(0.9, 0.0001)
        assert abs(r - 9000) < 1


class TestBetaTemperature:
    """30 points"""

    def test_at_reference(self):
        """R = R0 should give exactly T0"""
        t = beta_temperature(10000)
        assert abs(t - 25.0) < 0.01

    def test_hot(self):
        """R = 5000 Ω (below R0, so hotter)"""
        t = beta_temperature(5000)
        assert abs(t - 41.74) < 0.1

    def test_cold(self):
        """R = 50000 Ω (above R0, so colder)"""
        t = beta_temperature(50000)
        assert abs(t - (-5.19)) < 0.5

    def test_extreme_cold(self):
        """R = 300000 Ω (very cold)"""
        t = beta_temperature(300000)
        assert t < -30

    def test_different_beta(self):
        """Different material constant"""
        t1 = beta_temperature(5000, beta=3890)
        t2 = beta_temperature(5000, beta=4500)
        assert t1 != t2


class TestSelfHeating:
    """10 points"""

    def test_basic(self):
        dt = self_heating_error(125e-6, 10000)
        assert abs(dt - 0.15625) < 0.001

    def test_zero_current(self):
        assert self_heating_error(0, 10000) == 0


class TestFullPipeline:
    """20 points"""

    def test_basic(self):
        result = measure_temperature(1.25, 0.625)
        assert isinstance(result, dict)
        assert abs(result['temperature_C'] - 41.74) < 0.1
        assert abs(result['current_uA'] - 125) < 0.1
        assert abs(result['resistance'] - 5000) < 1
        assert 'self_heating_mC' in result

    def test_equal_voltages(self):
        """Equal voltages means R_T = R_prec = 10kΩ, so T = 25°C"""
        result = measure_temperature(0.5, 0.5)
        assert abs(result['temperature_C'] - 25.0) < 0.1
