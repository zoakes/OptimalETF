#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:23:56 2020

@author: zoakes
"""

from Segments import Segments
from ModelPFS import ModelPFS

'''
SF_Default_ETFs = {
    "TIPS":('TIP',.19),
    "USFi":('SPAB',.04),
    "STUST":('SPTS',.01),
    'EMFi':('EMB',.39),
    'MFi':('MUB',.07),
    'IntEq':('SPGM',.09), #Not in here -- But added
    'USEq':('SPTM',.03),
    'DM':('SPDW',.04),
    'EM':('SPEM',.11),
    'RE':('USRT',.08)
}
'''


'''
WAS named ModelPFS in Jupyter -- 
put ModelPFs into class and renamed this Real
'''

class OptPFS:
    
    '''Need to build out these defaults to include everything'''
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
        self.exp_ratios = self.s.create_exp_ratio_dct()
        
        self.model_pfs = self.mpf.model_pfs 
        
        self.TGT_PFS = {}
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
     
    '''These 2 optimize models require ALL Model segments to be present in Segments, and Quandl data'''
    #Look at best way to include exp ratios...
    def optimize_by_exp_ratio(self, pf_number,asset_class):
        pf = self.model_pfs[pf_number]
        seg = pf[asset_class]
        etf_options = self.optimal_etfs[asset_class]

        sorted_by_exp_ratio = sorted([(etf,exp) for etf, exp in self.exp_ratios.items() if etf in etf_options], key = lambda xy: xy[1])
        if len(sorted_by_exp_ratio) > 0:
            print(sorted_by_exp_ratio)
        return sorted_by_exp_ratio[0]
    
    def optimize_model_pf(self, pf_number):
        pf = self.model_pfs[pf_number]
        segs = list(pf.keys())
        
        PF = {}
        total_exp = 0
        eff_exp = 0
        for seg in segs:
            print(f'Starting {seg}')
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
    
    
    def get_target_pf(self,pf_number):
        model = self.model_pfs[pf_number]
        top1 = self.s.create_optimal_dct(top = 1)
        
        #etf1, er1, detf, der = None, None, None, None
        tgt_pf = {}
        eff_er = 0
        for seg, wt in model.items():

            #Check to see if PRESENT in query (via Segments -> ORM -> Quandl)
            opt_etf = top1.get(seg,None)
            
            #If present, record etf, and exp ratio 
            if opt_etf is not None:
                etf = opt_etf[0][0]
                er = opt_etf[0][1]
                #etf1, er1 = er, etf

            
            #MAYBE should be comparing er ^^ to er below ? Seeing if queried is possibly higher than default?
            #Default should be included in query, but couldn't hurt to optimize one last time?
            
            #If not present, take DEFAULT 
            if opt_etf is None:
                opt_etf = self.def_optimal_etfs[seg][0]
                etf = opt_etf
                er = opf.def_exp_ratios[etf]
                #detf, der = etf, er
            
            #if er1 and der:
            #    if er1 > der:
            #        etf, er = detf, der 

            
            eff_er += er
            tgt_pf[etf] = self.model_pfs[1][seg]
            print(f'Optimal {seg} ETF:  {etf} -- ER: {er}')
            
        print(f'Optimal ETF for Model {pf_number} -- Eff ER: {eff_er/len(model)}')
        self.TGT_PFS[pf_number] = tgt_pf
        self.tgt_pf = tgt_pf
        return tgt_pf
            
            
    
            
            
        
        
if __name__ == '__main__':
    opf = OptPFS()   
    print(opf.model_pfs)
    print(opf.optimal_etfs)
    models = opf.model_pfs
    opt = opf.optimal_etfs
    
    
    target_pf_1 = opf.get_target_pf(1)
    print(target_pf_1)
    
    '''
    THESE require the data to be COMPLETE (and the properties to include IntEq, TIPS, Etc...)
    Otherwise will throw error! (Maybe best to remove them ?)
    
    opf.optimize_by_exp_ratio(1,'USEq')
    opf.optimize_model_pf(1)

    '''
    

            
            
   
        
    
    
    
    
    