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
Created on Tue Mar 17 16:06:59 2015

Main economic analysis used within DTOcean tool

"""

from .functions import (costs_from_bom,
                        get_discounted_values,
                        get_phase_breakdown,
                        get_total_cost)


def main(capex, opex, energy, discount_rate=0.):
    
    # Note, nominal units of energy and costs are kWs and Euro
    # Year 0 represents costs prior to beginning of operations
    
    # Define the results dictionary
    result = {"CAPEX": None,
              "Discounted CAPEX": None,
              "CAPEX breakdown": None,
              "OPEX": None,
              "Discounted OPEX": None,
              "Energy": None,
              "Discounted Energy": None}
   
    ### COSTS
        
    # CAPEX
    if not capex.empty:
        
        breakdown = get_phase_breakdown(capex)
        total = get_total_cost(capex)

        costs_df = costs_from_bom(capex)
        discounted = get_discounted_values(costs_df, discount_rate)

        if breakdown is not None: result["CAPEX breakdown"] = breakdown
            
        result["CAPEX"] = total
        result["Discounted CAPEX"] = discounted.iloc[0]
    
    # OPEX
    if not opex.empty:
        
        opex_by_year = opex.set_index('project_year')
        total = opex_by_year.sum()
        discounted = get_discounted_values(opex, discount_rate)
            
        result["OPEX"] = total
        result["Discounted OPEX"] = discounted

    ### ENERGY
    
    # Can exit if no energy records are provided
    if energy.empty: return result
    
    energy_by_year = energy.set_index('project_year')
    total = energy_by_year.sum()
    discounted = get_discounted_values(energy, discount_rate)
     
    result["Energy"] = total
    result["Discounted Energy"] = discounted
    
    return result
