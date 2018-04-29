# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 17:10:23 2017

@author: acorn
"""

f = open("대화문.txt", 'r')
data2=f.read().splitlines() 
script=[]
for i in range(0,len(data2),2):
    ss=[data2[i],data2[i+1]]
    script.append(ss)


train_data = script
train_data

