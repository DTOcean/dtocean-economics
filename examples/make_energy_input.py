# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 17:00:33 2015
Example energy table
@author: msilva
"""

import pandas as pd
import numpy as np

def make_energy_df():

    unc=np.random.randint(11000,high=11001,size=18)
    s=pd.Series([0,0,5000])
    s=np.append(s,unc)
    
    energydb = {'project_year' : pd.Series([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,
                                            15,16,17,18,19,20]),
                'unconstrained' :s,
                'availability' : pd.Series ([0,0,0.47,0.76,0.75,0.55,0.75,0.58,
                                             0.78,0.87,0.82,0.92,0.77,0.88,0.89,
                                             0.64,0.77,0.67,0.65,0.47,0.49]),
                }
    
    
    energy = pd.DataFrame (energydb)
    
    energy['energy']=energy['unconstrained']*.98*.95*energy['availability']
    energy = energy[['project_year','energy']]
    
    return energy
