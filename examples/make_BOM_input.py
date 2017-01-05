# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:53:53 2015
Example bill of materials table
@author: msilva
"""

import pandas as pd

def make_BOM_df():

    db = {'item'            : pd.Series(['Device','Electrical cable',
                                         'Mooring Lines','Anchors',
                                         'Mooring Lines','Vessel X','Vessel Y',
                                         'Electrical Cable','Anchors']),
          'unitary_cost'    : pd.Series([2500000,800,60,1400,800,2500,500,300,
                                         1400]),
          'currency'        : pd.Series(['EUR','EUR','EUR','EUR','EUR','EUR',
                                         'EUR','EUR','EUR']),
          'ref_year'        : pd.Series([2012,2014,2014,2010,1999,2007,2009,
                                         2010,2010]),
          'units'           : pd.Series(['devices','metres','metres','units',
                                          'metres','days.vessel','days.vessel',
                                          'meters','units']),
          'quantity'        : pd.Series([5,5000,1500,6,250,10,3,1000,3]),
          'project_year'    : pd.Series([2,1,0,0,5,2,7,15,10]),
          'capex_opex'      : pd.Series(['c','c','c','c','o','c','o','o','o']),
          'workpackage'     : pd.Series(['wp2','wp3','wp4','wp4','wp6','wp5',
                                         'wp5','wp6','wp6'])}
    
    df = pd.DataFrame (db)
    
    df = df[['item','quantity','units','unitary_cost','currency',
             'project_year']]
            
    return df
