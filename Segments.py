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



class Segments:
    SD = {}
    # ADD each TO SD (so can be called) 
    # SD['USFi'] = self.USFi
    
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
        
        self.SD = {
            'USFi':self.USFi,
            'UST':self.UST,
            'USCFi':self.USCFi,
            'EQ':self.Eq,
            'USEq':self.USEq,
            'LC':self.LC,
            'SC':self.SC,
            'EM':self.EM,
            'DM':self.DM,
            'M':self.M,
            'G':self.G
        } 
  
    def create_optimal_dct(self,top = 5):
        segs = list(self.SD)
        OPT_PF = {}
        for seg in segs:
            df = self.SD[seg]
            
            #Add any OTHER filters here... (AUM, etc)

            df.sort_values(by = 'net_expense',inplace=True)
            
            tickers = df.ticker.to_list()[:top]
            ers = df.net_expense.to_list()[:top]
            seg_pairs = [(tickers, ers) for tickers, ers in zip(tickers, ers)]
            OPT_PF[seg] = seg_pairs

        self.optimal_etfs = OPT_PF
        return OPT_PF
    
    def create_exp_ratio_dct(self):
        opt_etfs = self.create_optimal_dct(top = 1)
        #exp_ratios = {ticker:exp for ticker, exp in list(opt_etfs.values())}
        
        exp_ratios = {v[0][0]:v[0][1] for k,v in list(opt_etfs.items())}
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


    '''NEED to add OTHER filters here (when we have FULL dataset -- for TIPS, Munis, STUST's, ETC'''
    