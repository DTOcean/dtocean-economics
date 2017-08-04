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
Economic functions to be used within DTOcean tool

"""


def get_item_total_cost(quantity, unitary_cost):

    """
    Function to calculate cost
    Can be applied to one item only, or to a table containing quantities and 
      unitary costs
    if units and currencies don't match these should be converted before using
      the cost function
      """
    
    cost = quantity * unitary_cost
    
    return cost


def get_present_value(value, yr, dr):

    """
    Function to calculate present value
    It should be applied to a table with costs and year cost occurs, and to 
      energy output table
    Costs could be calculated with the above function. 
    It can be applied in an item by item basis, or on the sum by year
    """
    
    present_value = (value / ((1 + dr) ** yr))
    
    return present_value


def get_discounted_cost(bill_of_materials, discount_rate):
    
    bill_of_materials['cost'] = get_present_value(
                        get_item_total_cost(bill_of_materials['quantity'],
                                            bill_of_materials['unitary_cost']),
                        bill_of_materials['project_year'],
                        discount_rate)
                        
    discounted_cost = bill_of_materials['cost'].sum(axis=0)
    
    return discounted_cost


def get_discounted_energy(energy_output, discount_rate):

    energy_output['discounted_energy'] = get_present_value(
                                            energy_output['energy'],
                                            energy_output['project_year'],
                                            discount_rate)
                                            
    discounted_energy = energy_output['discounted_energy'].sum(axis=0)
        
    return discounted_energy


def get_lcoe(discounted_cost, discounted_energy):
    
    lcoe = discounted_cost / discounted_energy
    
    return lcoe


