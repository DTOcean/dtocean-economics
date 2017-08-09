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

"""

import pandas as pd


def estimate_cost_per_power(total_rated_power,
                            unit_cost,
                            phase=None):
        
    cost = total_rated_power * unit_cost
    cost_bom = make_phase_bom([1], [cost], [0], phase)
    
    return cost_bom


def estimate_energy(lifetime,
                    year_energy,
                    network_efficiency=None):
    
    # Note units of energy are kW
    
    if network_efficiency is not None:
        net_coeff = network_efficiency
    else:
        net_coeff = 1.
        
    energy_kw = [0] + [year_energy * net_coeff] * lifetime
    energy_year = range(lifetime + 1)

    energy_record = make_energy_record(energy_kw, energy_year)
        
    return energy_record


def estimate_opex(lifetime,
                  total_rated_power=None,
                  opex_estimate=None,
                  annual_repair_cost_estimate=None,
                  annual_array_mttf_estimate=None,
                  phase=None):
    
    # Note, units of mttf is hours
        
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
    
    opex_bom = make_phase_bom(opex_quantity,
                              opex_unit_cost,
                              opex_year,
                              phase)
        
    return opex_bom


def make_phase_bom(quantities, costs, years, phase=None):
    
    if not (len(quantities) == len(costs) == len(years)):
        
        errStr = ("Number of quantities, unit costs and project years must be "
                  "equal")
        raise ValueError(errStr)
        
    phase_years = [phase] * len(years)
    
    raw_costs = {'phase': phase_years,
                 'quantity': quantities,
                 'unitary_cost': costs,
                 'project_year': years}
        
    phase_bom = pd.DataFrame(raw_costs)
    
    return phase_bom


def make_energy_record(kws, years):
    
    if not (len(kws) == len(years)):
        
        errStr = "Number of energy values and project years must be equal"
        raise ValueError(errStr)
    
    energy_raw = {'project_year': years,
                  'energy': kws}
    energy_record = pd.DataFrame(energy_raw)
    
    return energy_record
