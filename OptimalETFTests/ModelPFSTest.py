#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 08:32:13 2020

@author: zoakes
"""

import sys
#sys.path.insert(0, "../ETFOpt") #Maybe?

#or

sys.path.insert(0, '../')           #BINGO !!! NAVIGATE TO THE FUCKING THING MANUALLY


try:
    from ModelPFS import ModelPFS
except ImportError:
    print('No Import')
    

class ModelPFSTest:
    
    def __init__(self,log_lvl = 1):
        self.mpf = ModelPFS()
        self.log_lvl = log_lvl
        
    
    def run_all_tests(self):
        self.test_model_pfs_attr()
        self.test_pf1()
        self.test_pf2()
        self.test_pf(1)
        self.test_all_pfs(0)
        print('Success! All ModelPFS Tests passed.')

        return 1
        
        
        
    def test_model_pfs_attr(self):
        m = ModelPFS()
        
        mpfs_dict = m.model_pfs
        ct = 0
        for pf_num, pf_prop in mpfs_dict.items():
            if self.log_lvl > 0:
                print(f'{pf_num} : {pf_prop}')
            ct += 1
        assert ct == len(mpfs_dict), 'Error -- check self.model_pfs in modelPFS'
        return 1
    
    
    def test_pf1(self):
        m = ModelPFS()
        m1 = m.PF1 
        
        PF1 =  {
            'USEq':.4,
            'IntEq':.25,
            'EM':.25,
            'EMFi':.03,
            'USFi':.07
            }
        #assert m1 == PF1, 'Check that dicts match'
        total = 0.0
        for seg, wt in PF1.items():
            assert m1[seg] == wt, 'Dictionaries do not match in PF1 property'
            
            total += wt
        assert total == 1.0, 'Portfolio Weights do not sum to 1.0'
        
        return 1
    
    
    def test_pf2(self):
        m = ModelPFS()
        m2 = m.PF2
        
        PF2 = {
            'USEq':.3,
            'IntEq':.2,
            'EM':.2,
            'EMFi':.07,
            'USFi':.23
            }
        #assert m1 == PF1, 'Check that dicts match'
        total = 0.0
        for seg, wt in PF2.items():
            assert m2[seg] == wt, 'Dictionaries do not match in PF2 property'
            total += wt
        assert total == 1.0, 'Portfolio Weights do not sum to 1.0'
            
        return 1
    
    #More automated, less explicit --- maybe better than repeating 20x of ^^ ?
    def test_pf(self, pf_number):
        assert 0 < pf_number <= 20, 'ArgumentError -- pass a pf_number between 1 and 20' 
        m = ModelPFS()
        md = m.model_pfs

        #pf_n = md[pf_number] #same as self.PF1, or self.PF2
        pf_n = md.get(pf_number,-1)
        assert pf_n != -1, f'ERROR -- PF{pf_number} key not present in ModelPFS -- may not be built yet.'
        
        total = 0.0
        for seg, wt in pf_n.items():
            assert md[pf_number][seg] == wt, f'Check dict / property in PF{pf_number} -- error on key {seg}'
            total += wt
        
        assert total == 1.0, f'PF{pf_number} Portfolio Weights do not sum to 1.0'
        
        print(f'Success -- tested PF{pf_number}')
        return 1
    
    def test_all_pfs(self, all_present_or_all_numbers = 0):
        m = ModelPFS()
        
        #All present
        if all_present_or_all_numbers == 0:
            md = m.model_pfs
            models_to_test = list(md.keys())
            print('testing models:',models_to_test)
        
        #ALL numbered portfolios: (1 - 20)
        else:
            models_to_test = range(1,21)    #20 models initially
            print('testing models:',models_to_test)
        
        for pfn in models_to_test:
            self.test_pf(pfn)
        
        return 1
            
            
        
        
            
        
        
    
if __name__ == '__main__':
    mpft = ModelPFSTest()
    
    mpft.run_all_tests()

    
    # ---- Failing Tests (for pfs not yet defined ------- #

    #mpft.test_pf(150)
    
    #mpft.test_all_pfs(1) #TESTS 1 - 20 exactly...
    
    
    
    
             
            
        
        
        