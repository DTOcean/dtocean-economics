# -*- coding: utf-8 -*-

#    Copyright (C) 2016  Marta Silva, Mathew Topper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

Created on Thu Mar 05 16:16:39 2015
Functions to be used within DTOcean tool

"""

import pandas as pd


def get_combined_lcoe(lcoe_capex=None, lcoe_opex=None):
    
    if lcoe_capex is None and lcoe_opex is None: return
    
    lcoe = 0.        
    
    if lcoe_capex is not None:
        lcoe += lcoe_capex
        
    if lcoe_opex is not None:
        lcoe += lcoe_opex
        
    return lcoe


def get_discounted_cost(bill_of_materials, discount_rate):
    
    costs = bill_of_materials['quantity'] * bill_of_materials['unitary_cost']
    
    present_values = get_present_values(costs,
                                        bill_of_materials['project_year'],
                                        discount_rate)
                        
    discounted_cost = present_values.sum()
    
    return discounted_cost


def get_discounted_energy(energy_output, discount_rate):

    present_values = get_present_values(energy_output['energy'],
                                        energy_output['project_year'],
                                        discount_rate)
                                            
    discounted_energy = present_values.sum()
        
    return discounted_energy


def get_lcoe(discounted_cost, discounted_energy):
    
    lcoe = float(discounted_cost) / discounted_energy
    
    return lcoe


def get_phase_breakdown(bom):
    
    # Check for null phases
    null_phases = pd.isnull(bom["phase"])
    
    # No breakdown available
    if null_phases.all(): return None

    # Replace any null phase values
    bom.loc[pd.isnull(bom["phase"]), "phase"] = "Other"
    
    phase_groups = bom.groupby("phase")
    
    phase_breakdown = {}
    
    for phase_name, phase_bom in phase_groups:
        
        phase_cost = get_total_cost(phase_bom)
        phase_breakdown[phase_name] = phase_cost
        
    return phase_breakdown


def get_present_values(value, yr, dr):

    """
    Function to calculate present value
    It should be applied to a table with costs and year cost occurs, and to 
      energy output table
    Costs could be calculated with the above function. 
    It can be applied in an item by item basis, or on the sum by year
    """
    
    present_value = (value / ((1 + dr) ** yr))
    
    return present_value


def get_total_cost(bom):
    
    result = (bom['unitary_cost'] * bom['quantity']).sum()
                            
    return result


def get_total_energy(energy_record):
    
    result = energy_record['energy'].sum()
                            
    return result


