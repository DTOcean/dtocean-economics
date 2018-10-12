# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 12:36:48 2017

@author: mtopper
"""

from dtocean_economics import main


def test_main(bom, opex_costs, energy_record):
        
    result = main(bom, opex_costs, energy_record)
        
    for value in result.values():
        assert value is not None


def test_main_no_capex(bom, opex_costs, energy_record):
    
    capex_empty = bom.drop(bom.index)
    result = main(capex_empty, opex_costs, energy_record)
    
    assert result["CAPEX breakdown"] is None
    assert result["CAPEX"] is None
    assert result["Discounted CAPEX"] is None


def test_main_no_opex(bom, energy_record):
    
    opex_empty = bom.drop(bom.index)
    
    result = main(bom, opex_empty, energy_record)
    
    assert result["OPEX"] is None
    assert result["Discounted OPEX"] is None
    
    
def test_main_no_energy(bom, opex_costs, energy_record):
    
    energy_empty = energy_record.drop(energy_record.index)
    result = main(bom, opex_costs, energy_empty)
    
    assert result["Energy"] is None
    assert result["Discounted Energy"] is None
