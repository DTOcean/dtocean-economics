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

Economic functions to be used within DTOcean tool

*df_lcoe: calculated the levelized cost of energy using a bill of materials
table, a energy output table, and a discount rate. Uses the first 2 functions 
previously described and applies to every row of the tables, and uses the sum 
of the outputs to calculate the lcoe using the simple_lcoe function.

"""

from .functions import present_value, item_total_cost

def get_discounted_cost(bill_of_materials, discount_rate):

    """
    Function to calculate LCOE from pandas tables
    Assumes that bill_of_materials is a table containing the fields: 
         item, unitary_cost, quantity, project_year
         for later iterations of the tool more fields may be required, such as
             workpackage, cost_scale_fuction_type,
             cost_scale_fuction_coeficient
    Assumes that energy_output is a table containing the fields:
         project_year, energy_output
    Discount_Rate is a float type input
    """
    
    bill_of_materials['cost'] = present_value(
                        item_total_cost(bill_of_materials['quantity'],
                                        bill_of_materials['unitary_cost']),
                        bill_of_materials['project_year'],
                        discount_rate)
                        
    discounted_cost = bill_of_materials['cost'].sum(axis=0)
    
    return discounted_cost
    
def get_discounted_energy(energy_output, discount_rate):

    """
    Function to calculate LCOE from pandas tables
    Assumes that bill_of_materials is a table containing the fields: 
         item, unitary_cost, quantity, project_year
         for later iterations of the tool more fields may be required, such as
             workpackage, cost_scale_fuction_type,
             cost_scale_fuction_coeficient
    Assumes that energy_output is a table containing the fields:
         project_year, energy_output
    Discount_Rate is a float type input
    """

    energy_output['discounted_energy'] = present_value(
                                            energy_output['energy'],
                                            energy_output['project_year'],
                                            discount_rate)
                                            
    discounted_energy = energy_output['discounted_energy'].sum(axis=0)
        
    return discounted_energy
    
def lcoe(discounted_cost, discounted_energy):
    
    """
    Function to calculate LCOE
    The sum of cost should be the sum of all costs after the previous fuction 
      has been applied
    the sum of energy is the sum of energy output after the previous function 
      has been applied
    """
    
    lcoe = discounted_cost / discounted_energy
    
    return lcoe
