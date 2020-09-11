#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 06:57:50 2020

@author: zoakes
"""


#Should I make these frozen dataclass objects?
'''THIS might be better as GLOBALS (for editing) -- but kinda think I want this frozen'''

class ModelPFS:

    
    def __init__(self):
        #self.model_pfs = {}
        self.list_of_pfs = [self.PF1,self.PF2,self.PF20]
        self.model_pfs = {
            1: self.PF1,
            2: self.PF2,
            20: self.PF20
            }

        
    @property
    def PF1(self):
        PF1 =  {
            'USEq':.4,
            'IntEq':.25,
            'EMEq':.25,
            'EMFi':.03,
            'USFi':.07
            }
        return PF1
    
    @property 
    def PF2(self):
        PF2 = {
            'USEq':.3,
            'IntEq':.2,
            'EMEq':.2,
            'EMFi':.07,
            'USFi':.23
            }
        return PF2

    @property
    def PF20(self):
        PF20 = {
            'USEq':.15,
            'IntEq':.05,
            'EMEq':.05,
            'EMFi':.03,
            'MFi':.25,
            'TIPS':.06,
            'STUST':.15,
            'USFi':.25
            
           }
        return PF20
    
    
if __name__ == '__main__':
    mpf = ModelPFS()
    print(mpf.model_pfs)
    

        