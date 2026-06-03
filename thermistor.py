"""Thermistor Measurement Pipeline
Module 1: Thermal Sensors — Assignment

Implement the four functions below. Each uses the precision resistor
excitation circuit from Lecture 2.

Circuit: VDAC → Op-Amp Buffer → R_prec (10kΩ, 0.25%) → R_T (NTC) → GND
         ADC Ch.1 measures V across R_prec
         ADC Ch.2 measures V across R_T
"""

import numpy as np


def calculate_current(v_r, r_prec=10000):
    """Calculate excitation current from voltage across precision resistor.

    Args:
        v_r: Voltage across precision resistor (V)
        r_prec: Precision resistor value (Ω), default 10000

    Returns:
        Current in amps
    """
    # TODO: implement
    pass


def calculate_resistance(v_t, current):
    """Calculate thermistor resistance from voltage and current.

    Args:
        v_t: Voltage across thermistor (V)
        current: Current through circuit (A)

    Returns:
        Resistance in ohms
    """
    # TODO: implement
    pass


def beta_temperature(r_t, r0=10000, t0_c=25, beta=3890):
    """Calculate temperature from thermistor resistance using beta equation.

    T = 1 / (1/T0 + (1/β) · ln(R_T/R0))

    Args:
        r_t: Measured thermistor resistance (Ω)
        r0: Reference resistance (Ω), default 10000
        t0_c: Reference temperature (°C), default 25
        beta: Beta coefficient (K), default 3890

    Returns:
        Temperature in degrees Celsius
    """
    # TODO: implement (remember to convert to/from Kelvin)
    pass


def self_heating_error(current, r_t, delta=1e-3):
    """Calculate self-heating temperature error.

    ΔT = (I² · R_T) / δ

    Args:
        current: Excitation current (A)
        r_t: Thermistor resistance (Ω)
        delta: Dissipation constant (W/°C), default 1e-3

    Returns:
        Temperature error in °C
    """
    # TODO: implement
    pass


def measure_temperature(v_r, v_t, r_prec=10000, r0=10000, t0_c=25, beta=3890):
    """Complete measurement pipeline: ADC voltages → temperature.

    Uses all four functions above to go from raw voltage readings
    to a calibrated temperature with self-heating verification.

    Args:
        v_r: Voltage across precision resistor (V)
        v_t: Voltage across thermistor (V)
        r_prec, r0, t0_c, beta: Circuit and sensor parameters

    Returns:
        dict with keys:
            'current_uA': current in microamps
            'resistance': thermistor resistance in ohms
            'temperature_C': temperature in degrees Celsius
            'self_heating_mC': self-heating error in millidegrees Celsius
    """
    # TODO: implement using your functions above
    pass
