# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 23:05:51 2018

@author: Guy
"""

#import conversion
#import minisolvers #Written by someone else
import LM

KnowB=["(a)>(b)","(a)&(b)", "(a)|(b)", "(a)>(-c)" , "(a)>(d)"]

#sen1="a&b"
#sen1="b>-c"
#sen1="a|c"
#sen1="-a"
#sen1="c&d"
sen1="a>b>c"

print(KnowB)




if LM.checkConsistency(KnowB):
    print("Knowledge base is satisfiable and the model is below:")
    print(list(LM.getModel()))
else:
    print("Knowledge base is not satisfiable")


   
 
  
#if (LM.checkEntailment(KnowB, sen1)):
 #   print(sen1 + " does entail from the knowledge base")
#else:
 #   print(sen1 + " doesn't entail from the knowledge base")
