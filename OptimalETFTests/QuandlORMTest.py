#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 09:13:43 2020

@author: zoakes
"""

import sys
#sys.path.insert(0, "../ETFOpt") #Maybe?

#or

sys.path.insert(0, '../')           #BINGO !!! NAVIGATE TO THE FUCKING THING MANUALLY


try:
    from QuandlORM import ETFData
except ImportError:
    print('No Import')
    
    
class QuandlORMTest:
    
    def __init__(self):
        self.q = ETFData()
        
    def run_all_tests(self):
        self.test_init()
        self.test_attrs()
        print('Success! All QuandlORM Tests passed.')
        return 1
        
        
    def test_init(self):
        etfd = ETFData()
        #How can I test this?
        
    def test_attrs(self):
        etfd = ETFData()

        assert etfd.def_factors == ['ticker', 'net_expense', 'is_levered',
                                'asset_class', 'category', 'focus', 'region'],\
                                'ERROR -- default factors not present.'
        
if __name__ == '__main__':
    
    q = QuandlORMTest()
    
    q.run_all_tests()
    
    
        
        