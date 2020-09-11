#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:59:50 2020

@author: zoakes
"""

#WTF?

#from ETFOpt.Segments import Segments
#from Users.zoakes.Documents.Spyder_Docs.QC.ETFOpt.Segments import Segments
#from ETFOptTests import Segments_test
#from ETFOpt import Segments

if __name__ == '__main__':
    
    print('Test Init, Assignment, Properties...')
    s = Segments() #Was using etfs (DF) as arg -- etfs
    print(s.USFi)
    print(s.G)
    s.SD['G'] #Alt way of calling... (w STRINGS!)
    print('Test Optimal Dict:')
    s.create_optimal_dct(top = 5)