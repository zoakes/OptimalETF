#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:23:56 2020

@author: zoakes
"""

from Segments import Segments
from ModelPFS import ModelPFS


'''
was named ModelPFS in Jupyter -- 
put ModelPFs into class and renamed this Real
'''

class RealPFS:
    
    def_optimal_etfs = {
    'USEq':['VOO','SPY'],
    'IntEq':['INTNTL'],
    'EMEq':['EEM','EFM'],
    'EMFi':['EVF'],
    'USFi':['BND']
    }
    
    def_exp_ratios = {
        'VOO':.005,
        'SPY':.015,
        'INTNTL':.023,
        'EEM':.035,
        'EFM':.033,
        'EVF':.022,
        'BND':.011
    }
    
    def __init__(self, mpf=None, s=None):
        if s is None:
            self.s = Segments()                                                          
        else:
            self.s = s
            
        if mpf is None:
            self.mpf = ModelPFS()
        else:
            self.mpf = mpf
                                                                    #ModelPFS()
        self.optimal_etfs = self.s.create_optimal_dct()
        
        self.model_pfs = self.mpf.model_pfs 

        
        self.final_PF_wts = {}
        self.eff_exp = 0
        
    
    '''Consider moving these lower level details to ModelPFS?  OR an interface?'''
        
    def modify_model_allocs(self, pf_number, asset_classes, new_allocs):
        '''Ex --- [USEq, IntEq], [.3,.2]'''
        #WILL NEED TO CHANGE 2 at once!
        #self.model_pfs[pf_number][asset_classes][0] = new_allocs[0]
        assert len(asset_classes) == len(new_allocs), 'ERROR -- asset_classes and new_allocs must be equal length'
        diff = 0
        old_vals = []
        for asset, alloc in zip(asset_classes, new_allocs):
            old = self.model_pfs[pf_number][asset]
            old_vals += [old]
            diff += alloc - old
            self.model_pfs[pf_number][asset] = alloc
            
        if diff != 0:
            print('ERROR -- cannot make values > 1.0 total.  Reverting to original')
            for asset, alloc in zip(asset_classes, old_vals):
                self.model_pfs[pf_number][asset] = alloc
            
        return self.model_pfs[pf_number]
    
    def replace_model_pf(self, pf_number, new_pf_dict):
        #pf = self.model_pfs[pf_number]
        total = sum([v for k,v in new_pf_dict.items()])
        assert sum([v for k,v in new_pf_dict.items()]) == 1, 'ERROR -- Allocation of new PF is > 1.0 (100%) total.'
        
        self.model_pfs[pf_number] = new_pf_dict
        return self.model_pfs[pf_number]
    
    def remove_model_pf(self, pf_number):
        #del self.model_pfs[pf_number] -- less safe version...
        self.model_pfs.pop(pf_number, 'No Key found') 
        
    #Look at best way to include exp ratios...
    def optimize_by_exp_ratio(self, pf_number,asset_class):
        pf = self.model_pfs[pf_number]
        seg = pf[asset_class]
        etf_options = self.opt_etfs[asset_class]
        
        sorted_by_exp_ratio = sorted([(etf,exp) for etf, exp in self.exp_ratios.items() if etf in etf_options], key = lambda xy: xy[1])
        print(sorted_by_exp_ratio[0])
        return sorted_by_exp_ratio[0]
    
    def optimize_model_pf(self, pf_number):
        pf = self.model_pfs[pf_number]
        segs = list(pf.keys())
        
        PF = {}
        total_exp = 0
        eff_exp = 0
        for seg in segs:
            holding, exp = self.optimize_by_exp_ratio(pf_number, seg)
            
            wt = pf[seg]
            PF[holding] = pf[seg]
            
            total_exp += exp
            eff_exp += exp * wt
            
        print("Avg Expense Ratio",total_exp / len(segs))
        print(f'Effective Expense Ratio: {eff_exp}')
        self.eff_exp = eff_exp
        self.final_PF_wts = PF
        
        return self.final_PF_wts #, self.eff_exp
        
if __name__ == '__main__':
    rpf = RealPFS()    