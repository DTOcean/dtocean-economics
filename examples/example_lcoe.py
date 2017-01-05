# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 14:34:10 2015
testing module to run lcoe

@author: msilva
"""

from make_BOM_input import make_BOM_df
from make_energy_input import make_energy_df
from dtocean_economics import lcoe

def test():
    
    BOM = make_BOM_df()
    energy = make_energy_df()
    cost = lcoe(BOM, energy, 0.08)
    
    return cost
    
if __name__ == '__main__':
    
    cost = test()

    print 'LCOE is {}'.format(cost)
