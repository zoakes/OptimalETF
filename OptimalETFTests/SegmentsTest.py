#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:59:50 2020

@author: zoakes
"""

#WTF?

'''FUCK this organization bullshit'''

import sys
#sys.path.insert(0, "../ETFOpt") #Maybe?

#or

sys.path.insert(0, '../')           #BINGO !!! NAVIGATE TO THE FUCKING THING MANUALLY


try:
    from Segments import *
except ImportError:
    print('No Import')
    
    
#Alternative...  DOES NOT WORK -- looks like it should though.
#import importlib
    
#importlib.import_module('..ETFOpt', package = 'Segments')
    
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
    
    def __init__(self,log_lvl = 1):
        self.s = Segments()
        self.logging_lvl = log_lvl
        
    def test_init_and_properties(self):
        s = Segments()
        print(s.G)
        s.SD['G'] #Alt way of calling... (w STRINGS!)
    
        assert s.USFi.asset_class.to_list()[0] == 'Fixed Income'
        assert s.USFi.region.to_list()[0] == 'North America'
        print('Properties work (USFi)')
        return 1
        
    
    def test_optimal_dct(self):
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
        return 1
    
    
    def test_exp_ratio(self):
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
        
        print('Create Exp Ratio Dict Works!')
        return 1
            
    
        print('create_exp_ratio_dct works.')
        
    def test_Segment_Dict_and_properties(self):
        s = Segments()
        sd = s.SD
        ct = 0
        for segment_string, seg_property in sd.items():
            if self.logging_lvl > 0: 
                print(segment_string)
                print(seg_property)
                #No real way to test it's returns... at least not YET without FULL data
            else:
                pass
            ct += 1
        if ct != len(sd):
            print('Error.')
            return -1
        print('SD works, properties work (could be tested further with full data)')
        return 1
        
            
        
        


if __name__ == '__main__':
    


    
    test_init_and_properties()
    
    test_optimal_dct()
    
    test_exp_ratio()
    
    st = SegmentsTest()
    
    #Numbered tests...
    
    t1 = st.test_Segment_Dict_and_properties()
    
    t2 = st.test_init_and_properties()
    
    t3 = st.test_exp_ratio()
    
    t4 = st.test_optimal_dct()
    
    #Iterate through tests to find numbered failure 
    
    tests = [t1,t2,t3,t4]
    
    for i, test in enumerate(tests):
        if test != 1:
            print('ERROR -- failing test {i}.')
    
    print('Success!  All tests passed.')

