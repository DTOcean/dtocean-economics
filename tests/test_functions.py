# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 12:36:48 2017

@author: mtopper
"""

import pytest
import numpy as np
import pandas as pd

from dtocean_economics.functions import (get_combined_lcoe,
                                         get_discounted_cost,
                                         get_discounted_energy,
                                         get_lcoe,
                                         get_phase_breakdown,
                                         get_present_values,
                                         get_total_cost,
                                         get_total_energy)


@pytest.mark.parametrize("capex, opex, expected", [
    (1, None, 1),
    (None, 1, 1),
    (1, 1, 2),
])
def test_get_combined_lcoe_capex(capex, opex, expected):
    
    result = get_combined_lcoe(capex, opex)
    
    assert result == expected


@pytest.mark.parametrize("test_input, expected", [
    (0., 200031),
    (0.1, 173580.34),
    (0.2, 152801),
])
def test_get_discounted_cost(bom, test_input, expected):

    result = get_discounted_cost(bom, test_input)

    assert np.isclose(result, expected)
    

@pytest.mark.parametrize("test_input, expected", [
    (0., 33),
    (0.1, 28.1818),
    (0.2, 24.4444),
])
def test_get_discounted_energy(energy_record, test_input, expected):
    
    result = get_discounted_energy(energy_record, test_input)

    assert np.isclose(result, expected)
    
    
def test_get_lcoe():
    
    result = get_lcoe(1, 10)
    
    assert result == 0.1
    
    
def test_get_phase_breakdown(bom):
    
    result = get_phase_breakdown(bom)
    
    assert set(result.keys()) == set(["Test", "Other"])
    assert result["Test"] == 31.
    assert result["Other"] == 200000.
    

def test_get_phase_breakdown_none(bom):

    none_bom = bom[pd.isnull(bom["phase"])]
    
    result = get_phase_breakdown(none_bom)
    
    assert result is None
    

@pytest.mark.parametrize("test_input, expected", [
    (0., [0, 10, 20]),
    (0.1, [0, 9.0909, 16.5289]),
    (0.2, [0, 8.3333,  13.8888]),
])
def test_get_present_values(test_input, expected):
    
    value = np.array([0, 10, 20])
    year = np.array([0, 1, 2])
    
    result = get_present_values(value, year, test_input)
    
    assert np.isclose(result, expected).all()


def test_get_total_cost(bom):
    
    result = get_total_cost(bom)
    
    assert result == 200031.


def test_get_total_energy(energy_record):
    
    result = get_total_energy(energy_record)
    
    assert result == 33.
