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

import pandas as pd

from .functions import (get_discounted_cost,
                        get_discounted_energy,
                        get_lcoe)


def main(discount_rate,
         device_cost,
         electrical_bom,
         moorings_bom,
         installation_bom,
         capex_oandm,
         opex_bom,
         energy_bom,
         network_efficiency,
         lifetime,
         n_devices,
         power_rating,
         electrical_estimate,
         moorings_estimate,
         install_estimate,
         opex_estimate,
         annual_repair_cost_estimate,
         annual_array_mttf_estimate,
         annual_energy):
    
    result = {"CAPEX": None,
              "Discounted CAPEX": None,
              "CAPEX breakdown": None,
              "OPEX": None,
              "Discounted OPEX": None,
              "Total cost": None,
              "Total cost breakdown": None,
              "Energy": None,
              "Discounted Energy": None,
              "LCOE CAPEX": None,  
              "LCOE OPEX": None,
              "LCOE": None}
                  
    # Discount rate (default to zero)
    if discount_rate is None:
        discount_rate = 0.0
    else:
        discount_rate = discount_rate
        
    # Total rated power
    total_rated_power = None
    
    if (n_devices is not None and
        power_rating is not None):
        
        total_rated_power = n_devices * power_rating
    
    ## COSTS
        
    # Capex results
    capex_costs, cap_costs_breakdown = get_capex_costs(n_devices,
                                                       device_cost,
                                                       electrical_bom,
                                                       moorings_bom,
                                                       installation_bom,
                                                       capex_oandm,
                                                       total_rated_power,
                                                       electrical_estimate,
                                                       moorings_estimate,
                                                       install_estimate)
    
    if not capex_costs.empty:
        
        capex_total = (capex_costs['unitary_cost'] *
                                            capex_costs['quantity']).sum()
        
        discounted_capex = get_discounted_cost(capex_costs,
                                               discount_rate)
                                                         
        # Record cost breakdown
        capex_breakdown = cap_costs_breakdown
        
        result["CAPEX"] = capex_total
        result["Discounted CAPEX"] = discounted_capex
        result["CAPEX breakdown"] = capex_breakdown
    
    # Opex results
    if opex_bom is None:
        opex_bom = estimate_opex_bom(opex_bom,
                                     total_rated_power,
                                     opex_estimate,
                                     annual_repair_cost_estimate,
                                     annual_array_mttf_estimate,
                                     lifetime)
    
    if opex_bom is not None:
        
        opex_total = (opex_bom['unitary_cost'] *
                                            opex_bom['quantity']).sum()
        
        discounted_opex = get_discounted_cost(opex_bom,
                                              discount_rate)
        
        result["OPEX"] = opex_total
        result["Discounted OPEX"] = discounted_opex
        
    # CAPEX vs OPEX Breakdown
    if (capex_total is not None and 
        opex_total is not None):
        
        cost_breakdown = {"CAPEX": capex_total,
                          "OPEX": opex_total}
        
        result["Total cost"] = capex_total + opex_total
        result["Total cost breakdown"] = cost_breakdown
                          

    ## ENERGY
    if energy_bom is None:
        energy_bom = estimate_energy_bom(network_efficiency,
                                         annual_energy,
                                         lifetime)
    
    # Calculate the discounted energy
    if energy_bom is not None:        

        energy_total = energy_bom['energy'].sum()
        discounted_energy = get_discounted_energy(energy_bom,
                                                  discount_rate)
                
        result["Energy"] = energy_total
        result["Discounted Energy"] = discounted_energy
                                                        
    if (discounted_capex is not None and
        discounted_energy is not None):
        
        LCOE_CAPEX = get_lcoe(discounted_capex,
                              discounted_energy)
        
        result["LCOE CAPEX"] = LCOE_CAPEX        
                                           
    if (discounted_opex is not None and
        discounted_energy is not None):
        
        LCOE_OPEX = get_lcoe(discounted_opex,
                             discounted_energy)
        
        result["LCOE OPEX"] = LCOE_OPEX
        
    if LCOE_CAPEX is None and LCOE_OPEX is None: return result
    
    # Calculate final lcoe
    LCOE_total = 0.        
    
    if LCOE_CAPEX is not None:
        LCOE_total += LCOE_CAPEX
        
    if LCOE_OPEX is not None:
        LCOE_total += LCOE_OPEX
        
    result["LCOE"] = LCOE_total
    
    return result


def get_capex_costs(n_devices,
                    device_cost,
                    electrical_bom,
                    moorings_bom,
                    installation_bom,
                    capex_oandm,
                    total_rated_power,
                    electrical_estimate,
                    moorings_estimate,
                    install_estimate):
    
    # Collect extra capex costs
    capex_unit_cost = []
    capex_quantity = []
    capex_year = []     
    cap_costs_breakdown = {}
    
    if (device_cost is not None and
        n_devices is not None):
        
        capex_unit_cost.append(device_cost)
        capex_quantity.append(n_devices)
        capex_year.append(0)
        
        cap_costs_breakdown["Devices"] = device_cost * \
                                                    n_devices
        
    # Build capex cost dataframe
    capex_cost_raw = {'unitary_cost': capex_unit_cost,
                      'quantity': capex_quantity,
                      'project_year': capex_year}
        
    capex_costs = pd.DataFrame(capex_cost_raw)
    
    # Add electrical costs if available
    if electrical_bom is not None:
        
        cap_costs_breakdown["Electrical Sub-Systems"] = (
                                electrical_bom['unitary_cost'] * 
                                    electrical_bom['quantity']).sum()
                            
        capex_costs = pd.concat([capex_costs, electrical_bom])
        
    elif (total_rated_power is not None and
          electrical_estimate is not None):
        
        cost = total_rated_power * electrical_estimate
        
        raw_costs = {'quantity': [1],
                     'unitary_cost': [cost],
                     'project_year': [0]}
                     
        electrical_costs = pd.DataFrame(raw_costs)
        
        cap_costs_breakdown["Electrical Sub-Systems"] = cost
                            
        capex_costs = pd.concat([capex_costs, electrical_costs])
        
    # Add moorings costs if available
    if moorings_bom is not None:

        cap_costs_breakdown["Mooring and Foundations"] = (
                                    moorings_bom['unitary_cost'] *
                                        moorings_bom['quantity']).sum()
                            
        capex_costs = pd.concat([capex_costs, moorings_bom])
        
    elif (total_rated_power is not None and
          moorings_estimate is not None):
        
        cost = total_rated_power * moorings_estimate
        
        raw_costs = {'quantity': [1],
                     'unitary_cost': [cost],
                     'project_year': [0]}
                     
        moorings_costs = pd.DataFrame(raw_costs)
        
        cap_costs_breakdown["Mooring and Foundations"] = cost
                            
        capex_costs = pd.concat([capex_costs, moorings_costs])
        
    # Add installation costs if available
    if installation_bom is not None:

        cap_costs_breakdown["Installation"] = (
                                    installation_bom['unitary_cost'] *
                                        installation_bom['quantity']).sum()
                            
        capex_costs = pd.concat([capex_costs, installation_bom])
        
    elif (total_rated_power is not None and
          install_estimate is not None):
        
        cost = total_rated_power * install_estimate
        
        raw_costs = {'quantity': [1],
                     'unitary_cost': [cost],
                     'project_year': [0]}
                     
        install_costs = pd.DataFrame(raw_costs)
        
        cap_costs_breakdown["Installation"] = cost
                            
        capex_costs = pd.concat([capex_costs, install_costs])
        
    # And O&M Condition Monitering Capex
    if capex_oandm is not None:
        
        cost = capex_oandm
                    
        raw_costs = {'quantity': [1],
                     'unitary_cost': [cost],
                     'project_year': [0]}
                     
        oandm_costs = pd.DataFrame(raw_costs)
        
        cap_costs_breakdown["Condition Monitoring"] = cost
                            
        capex_costs = pd.concat([capex_costs, oandm_costs]) 
        
    return capex_costs, cap_costs_breakdown


def estimate_opex_bom(total_rated_power,
                      opex_estimate,
                      annual_repair_cost_estimate,
                      annual_array_mttf_estimate,
                      lifetime):
    
    if lifetime is None: return None
    
    # Collect opex costs
    annual_costs = 0.
        
    if (total_rated_power is not None and
        opex_estimate is not None):
        
        annual_costs += total_rated_power * opex_estimate
        
    if (annual_repair_cost_estimate is not None and
        annual_array_mttf_estimate is not None):
        
        year_mttf = annual_array_mttf_estimate / 24. / 365.25
        failure_cost = annual_repair_cost_estimate / year_mttf
        
        annual_costs += failure_cost
        
    opex_unit_cost = [0.] + [annual_costs] * lifetime
    opex_quantity = [1] * (lifetime + 1)
    opex_year = range(lifetime + 1)
    
    opex_cost_raw = {'unitary_cost': opex_unit_cost,
                     'quantity': opex_quantity,
                     'project_year': opex_year}
                     
    opex_costs = pd.DataFrame(opex_cost_raw)
        
    return opex_costs


def estimate_energy_bom(network_efficiency,
                        year_energy,
                        lifetime):
    
    # If no O&M results are given then use the basic design energy
    if year_energy is None or lifetime is None: return
    
    # Create energy table
    energy_data = None
    
    if network_efficiency is not None:
        net_coeff = network_efficiency
    else:
        net_coeff = 1.
        
    energy_kw = [0] + [year_energy * 1e3 * net_coeff] * \
                                        lifetime
    energy_year = range(lifetime + 1)

    energy_raw = {'project_year': energy_year,
                  'energy': energy_kw}
    energy_data = pd.DataFrame(energy_raw)
        
    return energy_data
