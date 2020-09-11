#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:41:42 2020

@author: zoakes
"""
import quandl
quandl.ApiConfig.api_key = 'bNhmL6hk7a3boYd7Rbfz'
import pandas as pd



class ETFData:
    #Parse ETF DF's -> primitive types
    # DIP in practice
    def_factors = ['ticker','net_expense','is_levered','asset_class','category','focus','region']


    
    
    
    def __init__(self,path = None, factors_to_keep=None):
        #Initially, going to be CSV dependent -> eventually may use REST? / Other API stream
        #Dataframe
        if path is None:
            self.DF = quandl.get_table('ETFG/INDP', date='2018-01-02',ticker='SPY,GLD,EEM,EFA,TLT,JNK,IWM')
        else:
            self.DF = pd.read_csv(path) #WILL USE THIS WHEN FULL DATA
        
        #Columns / Factors
        if factors_to_keep is None:
            self.factors = self.def_factors
        else:
            self.factors = factors_to_keep #COL NAMES
            
            
        try:
            self.DF = self.DF.drop(columns = [col for col in self.DF.columns if col not in self.factors])
        
        except:
            try:
                self.DF = self.DF[self.factors]
            except:
                print('ERROR -- confirm factors are in dataframe.')
        
    def filter_by_factors(self, factor, top, asc=True, df_lst = 0, df = None):
        '''Asc and Factor can both be lists for multi sorts...
        NOT persistant -- simply queries a view, doesn't change class attr self.DF
        
        '''
        #if df is None:
        #    df = self.DF
        assert factor in self.factors, 'Choose factor in selected factors -- or re-init'
        if not isinstance(factor,list):
            df = self.DF.sort_values(by=[factor], ascending = asc)
        else:
            df = self.DF.sort_values(by=factor, ascending = True)
        
        df = df.head(top)
        tickers_lst = df.head(top).ticker.to_list()                       #CONFIRM COL NAME IS symbol
        #tickers_dct = df.set_index('ticker',inplace=True).to_dict()
        if df_lst == 0:
            return df
        return tickers_lst #if df_lst == 1 else tickers_dct
    
if __name__ == '__main__':
    print('test')
    
    e = ETFData()
    
    print(e.DF)
    