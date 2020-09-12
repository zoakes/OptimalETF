#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:20:55 2020

@author: zoakes
"""

#from ETFOptTests.Segments_test import create_instance #FUCK this...

from Segments import Segments

def test_init_and_properties():
    s = Segments()
    print(s.G)
    s.SD['G'] #Alt way of calling... (w STRINGS!)

    assert s.USFi.asset_class.to_list()[0] == 'Fixed Income'
    assert s.USFi.region.to_list()[0] == 'North America'
    print('Properties work (USFi)')
    return s

def test_optimal_dct():
    s = Segments()
    top5 = s.create_optimal_dct(top = 5)
    #assert max(len(top5.values())) > 1, 'Error -- check top'

    assert len(top5['EM']) > 1, 'Make sure top argument is working in create_optimal_dct'
    
    
    top1 = s.create_optimal_dct(top = 1)
    print('TOP1 \n',top1)
    for k, v in top1.items():
        assert len(v) == 1, 'Top1 returning more than 1' 
        
    assert top1['TIPS'] == [('TIP',.19)], 'Make sure defaults are working...'
    print('Optimal dict works.')


def test_exp_ratio():
    s = Segments()
    er = s.create_exp_ratio_dct()
    top1 = s.create_optimal_dct(1)
    print(er)

    #Test Class Attributes being assigned properly
    assert er == s.exp_ratios, 'Check class attr exp_ratios is saving properly'
    
    #All ETFs in OPTIMAL dict... make sure they are all in the ER dict...
    top = [v[0][0] for k, v in top1.items()]
    for top_etf in top:
        assert top_etf in er, 'Check create_exp_ratio_dct'
        
    #Make sure proper values (Exp_ratios) are present
    top_ers = [v[0][1] for k, v in top1.items()]
    print(top_ers)
    for top_er in top_ers:
        assert top_er in list(er.values()), "Check er values in expense ratio"
        
    #Compare Keys and Values -- make sure they match.
    for k, v in top1.items():
        assert er[v[0][0]] == v[0][1]
        

    print('create_exp_ratio_dct works.')
            



class SegmentsTest:
    
    def __init__(self):
        self.s = Segments()
        
        


if __name__ == '__main__':
    


    
    test_init_and_properties()
    
    test_optimal_dct()
    
    test_exp_ratio()



