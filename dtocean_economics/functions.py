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

List of functions:
* item_total_cost: calculates the total cost for a item in the context of the 
project. Simple multiplication for now, can later be expanded to take into 
consideration sizing functions

* present_value: calculates the prensent value of a cost or energy output, 
assuming a discount rate and the year the cost (or the production) occurs

* simple_lcoe: calulates the levelized cost of energy assuming the sum of all 
discounted costs and the sum of all discounted energy outputs

"""

def item_total_cost(quantity, unitary_cost):

    """
    Function to calculate cost
    Can be applied to one item only, or to a table containing quantities and 
      unitary costs
    if units and currencies don't match these should be converted before using
      the cost function
      """
    
    cost = quantity * unitary_cost
    
    return cost

def present_value(value, yr, dr):

    """
    Function to calculate present value
    It should be applied to a table with costs and year cost occurs, and to 
      energy output table
    Costs could be calculated with the above function. 
    It can be applied in an item by item basis, or on the sum by year
    """
    
    present_value = (value / ((1 + dr) ** yr))
    
    return present_value


