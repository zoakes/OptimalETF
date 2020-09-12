#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:36:18 2020

@author: zoakes
"""
from QuandlORM import ETFData as ETFs
import pandas as pd


'''
NEED to add OTHER filters here 
(when we have FULL dataset)
TIPS, Munis, STUST's, ETC 

(Some of the MORE CONSERVATIVE model PF holdings)

'''

'''
#Going to use as DEFAULTS -- class var
SF_Default_ETFs = {
    "TIPS":[('TIP',.19)], 
    "USFi":[('SPAB',.04)],
    "STUST":[('SPTS',.01)],  
    'EMFi':[('EMB',.39)], 
    'MFi':[('MUB',.07)],
    'IntEq':[('SPGM',.09)], 
    'USEq':[('SPTM',.03)],
    'DM':[('SPDW',.04)],
    'EM':[('SPEM',.11)],
    'RE':[('USRT',.08)]
}
            


'''





class Segments:
    
    SD = {}
    # ADD each TO SD (so can be called) 
    # SD['USFi'] = self.USFi
    
    SF_Default_ETFs = {
        "TIPS":[('TIP',.19)], 
        "USFi":[('SPAB',.04)],
        "STUST":[('SPTS',.01)],  
        'EMFi':[('EMB',.39)], 
        'MFi':[('MUB',.07)],
        'IntEq':[('SPGM',.09)], 
        'USEq':[('SPTM',.03)],
        'DM':[('SPDW',.04)],
        'EM':[('SPEM',.11)],
        'RE':[('USRT',.08)]
    }

    
    #Maybe import ETFData instance?
    def __init__(self, etf_instance = None, df = None):
        pd.set_option('mode.chained_assignment', None)
        
        if etf_instance is None:
            self.etf = ETFs()

        else:
            self.etf = etf_instance
        self.df = self.etf.DF
            
        
        self.optimal_etfs = {}
        self.exp_ratios = {}
        
        '''Why does adding values here break exp_Ratio function ?'''
        self.SD = {
            'USFi':self.USFi,
            'UST':self.UST,
            'TIPS':self.TIPS,
            'STUST':self.STUST,
            'EMFi':self.EMFi,
            'USCFi':self.USCFi,
            'EQ':self.Eq,
            'IntEq':self.IntEq,                                                 
            'USEq':self.USEq,
            'LC':self.LC,
            'SC':self.SC,
            'EM':self.EM,
            'DM':self.DM,
            'RE':self.RE,
            'M':self.M,
            'G':self.G
        } 
  
    def create_optimal_dct(self,top = 5):
        segs = list(self.SD)
        OPT_PF = {}
        for seg in segs:
            df = self.SD[seg]
            
            #Not all in SD HAVE defaults...
            try:
                def_pair = self.SF_Default_ETFs[seg]
                def_er = def_pair[0][1]
                def_etf = def_pair[0][0]
            except:
                continue
            
            #New addition... (Include defaults if no ETFs found)
            if df.shape[0] == 0:
                #If not found in query -- use Default global dict
                OPT_PF[seg] = def_pair
                continue
                
            #Add any OTHER filters here... (AUM, etc)
            
            #Sort queried ETFs
            df.sort_values(by = 'net_expense',inplace=True)
            
            #to list + append in defaults (to compare)
            tickers = df.ticker.to_list()
            tickers += [def_etf]
            
            ers = df.net_expense.to_list()
            ers += [def_er]
            
            seg_pairs = sorted([(tickers, ers) for tickers, ers in zip(tickers, ers)],key = lambda etf_er: etf_er[1])[:top] #Need to sort + take top of
            OPT_PF[seg] = seg_pairs

        self.optimal_etfs = OPT_PF
        return OPT_PF
    
    
    
    def create_exp_ratio_dct(self):
        opt_etfs = self.create_optimal_dct(top = 1)
        #exp_ratios = {ticker:exp for ticker, exp in list(opt_etfs.values())}
        
        exp_ratios = {v[0][0]:v[0][1] for k,v in list(opt_etfs.items())} #THIS line is culprit ...dont know why?
        self.exp_ratios = exp_ratios
        
        return exp_ratios
        

        
    @property
    def USFi(self):
        USFi = self.df.loc[self.df.asset_class == 'Fixed Income'].loc[self.df.region == 'North America']
        USFi.sort_values(by='net_expense',inplace=True)
        return USFi
    
    @property
    def USCFi(self):
        USCFi = self.USFi.loc[self.USFi.category == 'Corporate']
        #USCFi = USFi.loc[etfs.category == 'Corporate']
        USCFi.sort_values(by='net_expense',inplace=True)
        return USCFi


    
    @property
    def UST(self):
        UST = self.df.loc[self.df.focus == 'Treasury']
        UST.sort_values(by='net_expense',inplace=True)
        return UST
    
    @property
    def Eq(self):
        Eq = self.df.loc[self.df.asset_class == 'Equity']
        Eq.sort_values(by='net_expense',inplace=True)
        return Eq
    
    @property
    def USEq(self):
        USEq = self.Eq.loc[self.Eq.region == 'North America']
        USEq.sort_values(by='net_expense',inplace=True)
        return USEq
    
    @property
    def LC(self):
        LC = self.df.loc[self.df.asset_class == 'Equity'].loc[self.df.focus == 'Large Cap']
        LC.sort_values(by='net_expense',inplace=True)
        return LC
    
    @property
    def SC(self):
        SC = self.df.loc[self.df.asset_class == 'Equity'].loc[self.df.focus == 'Small Cap']
        SC.sort_values(by='net_expense',inplace=True)
        return SC
    
    @property
    def EM(self):
        EM = self.df.loc[self.df.region == 'Emerging Markets']
        EM.sort_values(by='net_expense',inplace=True)
        return EM
    
    @property
    def DM(self):
        DM = self.df.loc[self.df.region == 'Developed Markets']
        DM.sort_values(by='net_expense',inplace=True)
        return DM
    
    @property
    def M(self):
        M = self.df.loc[self.df.asset_class == 'Commodities'].loc[self.df.category == 'Precious Metals']
        M.sort_values(by='net_expense',inplace=True)
        return M
    
    @property
    def G(self):
        G = self.M.loc[self.M.focus == 'Gold']
        G.sort_values(by='net_expense',inplace=True)
        return G
    
    @property
    def IntEq(self):
        #REAL logic -- 
        IntEq = self.Eq.loc[self.Eq.region == 'Global']
        return IntEq

    @property
    def TIPS(self):
        TIPS = self.USFi.loc[self.USFi.focus == 'Municipal']                      #NOT sure this is PRESENT?
        if TIPS.shape[0] == 0:
            #logic to simply use TIPS default?
            #print('No TIPS found -- using Default.')
            pass
        return TIPS
    
    @property
    def STUST(self):
        STUST = self.USFi.loc[self.USFi.focus == 'Short Term']
        STUST.sort_values(by='net_expense',inplace=True)
        return STUST
    
    @property
    def EMFi(self):
        EMFi = self.df.loc[self.df.asset_class == 'Fixed Income'].loc[self.df.region == 'Emerging Markets']
        EMFi.sort_values(by='net_expense',inplace=True)
        return EMFi
    

    @property
    def RE(self):
        RE = self.df.loc[self.df.asset_class == "Real Estate"]#.loc[self.df.region == 'North America'] #OR dev mkts?
        RE.sort_values(by = 'net_expense', inplace=True)
        return RE
    



    '''NEED to add OTHER filters here (when we have FULL dataset -- for TIPS, Munis, STUST's, ETC'''
    
if __name__ == '__main__':
    s = Segments()
    opt_dct = s.create_optimal_dct(1)
    print(opt_dct)
    s.create_exp_ratio_dct()
    print('testing...')
