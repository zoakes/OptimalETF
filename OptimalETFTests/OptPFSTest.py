#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:47:45 2020

@author: zoakes
"""



import sys
#sys.path.insert(0, "../ETFOpt") #Maybe?

#or

sys.path.insert(0, '../')           #BINGO


try:
    from OptPFS import OptPFS
    from Segments import Segments
except ImportError:
    print('No Import')
    
    
#Build out a class thats a more organized test module  --- > 

class OptPFSTest:
    
    def __init__(self):
        self.o = OptPFS()
        
    


if __name__ == '__main__':
    opf = OptPFS()   
    print(opf.model_pfs)
    print(opf.optimal_etfs)
    models = opf.model_pfs
    opt = opf.optimal_etfs
    
    #
    '''
    THESE require the data to be COMPLETE (and the properties to include IntEq, TIPS, Etc...)
    Otherwise will throw error! (Maybe best to remove them ?)
    
    opf.optimize_by_exp_ratio(1,'USEq')
    #opf.optimize_model_pf(1)
    
    exp_ratios = opf.exp_ratios
    
    
    pf = opf.model_pfs[1]
    segs = list(pf.keys())
    
    for seg in segs:
        print(f'Starting {seg}')
        holding, exp = opf.optimize_by_exp_ratio(1, seg)
        print(holding, exp)
    '''
    
    #opf.optimize_by_exp_ratio(1,'USEq')
    
    etf_options = opf.optimal_etfs['USEq']
    for etf, exp in opf.exp_ratios.items(): 
        print(etf, exp)
        print(etf_options)
        #if etf in etf_options:
        #    print(etf,exp)
        if etf == 'SPY':
            print('Found')
    
    '''Debugging -- Issue is not all segments present (not all sectors in model PF available in data sample)'''
    s = Segments()     
    top1 = s.create_optimal_dct(top = 1)
    print('TOP1:')
    print(top1)
    model1 = opf.model_pfs[1]
    
    TGT_PF = {}
    total_er = 0
    for seg, wt in opf.model_pfs[1].items():
        print(seg,wt)
        

        opt_etf = top1.get(seg,None)
        print('OPT ETF',opt_etf)
        if opt_etf is not None:
            etf = opt_etf[0][0]
            er = opt_etf[0][1]
            print('1st Block',etf, er)
            
        if opt_etf is None:
            opt_etf = opf.def_optimal_etfs[seg][0]
            etf = opt_etf
            er = opf.def_exp_ratios[etf]
            print('Alt Opt ETF:',opt_etf)
            
            print('ETF - Exp Rate',etf, er)
            print(' -- End Inner Iter -- ')
            
        total_er += er
        TGT_PF[etf] = opf.model_pfs[1][seg]
            
        #opt_etf = top1.get(seg,opf.def_optimal_etfs[seg][0])
        
        print('Optimal: ',seg, opt_etf)

        #sec = top1[seg][0][0]
        #exp = top1[seg][1][1]
        #print(sec, exp, wt)
    print(TGT_PF)
        