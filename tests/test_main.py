# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 12:36:48 2017

@author: mtopper
"""

from dtocean_economics import main


def test_main(bom, energy_record):
    
    opex_bom = bom.copy()
    
    result = main(bom, opex_bom, energy_record)
    
    for value in result.values():
        assert value is not None


def test_main_no_capex(bom, energy_record):
    
    opex_bom = bom.copy()
    capex_empty = bom.drop(bom.index)
    
    result = main(capex_empty, opex_bom, energy_record)
    
    assert result["CAPEX breakdown"] is None
    assert result["CAPEX"] is None
    assert result["Discounted CAPEX"] is None
    assert result["LCOE CAPEX"] is None


def test_main_no_opex(bom, energy_record):
    
    opex_empty = bom.drop(bom.index)
    
    result = main(bom, opex_empty, energy_record)
    
    assert result["OPEX breakdown"] is None
    assert result["OPEX"] is None
    assert result["Discounted OPEX"] is None
    assert result["LCOE OPEX"] is None
    
    
def test_main_no_energy(bom, energy_record):
    
    opex_bom = bom.copy()
    energy_empty = energy_record.drop(energy_record.index)
    
    result = main(bom, opex_bom, energy_empty)
    
    assert result["Energy"] is None
    assert result["Discounted Energy"] is None
    assert result["LCOE CAPEX"] is None
    assert result["LCOE OPEX"] is None
    assert result["LCOE"] is None
