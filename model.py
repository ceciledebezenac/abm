# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:08:04 2019

@author: gycdb
"""
import random
import numpy
import matplotlib.pyplot
import operator
'''
print('hello')
 
y0=50
x0=50
if random.random()<0.5:
     y0=y0+1
else:
    y0=y0-1
if random.random()<0.5:
     x0=x0+1
else:
    x0=x0-1
print(y0,x0)

y1=50
x1=50
if random.random()<0.5:
     y1+=1
else:
    y1-=1
if random.random()<0.5:
     x1+=1
else:
    x1-=1
print(y1,x1)

dist=((x0-x1)**2+(y0-y1)**2)**0.5
print(dist)

'''
num_iterations=100
num_agents=10
agents=[]
for i in range (num_agents):
    agents.append([random.randint(0,99),random.randint(0,99)])

max_x=max(agents,key=operator.itemgetter(1))

matplotlib.pyplot.ylim(0, 100)
matplotlib.pyplot.xlim(0, 100)

for j in range(num_iterations):
    for i in range(num_agents):
        if random.random()<0.5:
            agents[i][0] = (agents[i][0] + 1) % 100
        else:
            agents[i][0] = (agents[i][0] - 1) % 100
        if random.random()<0.5:
            agents[i][1] = (agents[i][1] + 1) % 100
        else:
            agents[i][1] = (agents[i][1] - 1) % 100

for i in range(num_agents):
  
    matplotlib.pyplot.scatter(agents[i][1],agents[i][0])
matplotlib.pyplot.scatter(max_x[1],max_x[0],color='red')

def distance_between(agent1,agent2):
    dist=((agent1[0]-agent2[0])**2+(agent1[1]-agent2[1])**2)**0.5
    return(dist)
distance_all=numpy.zeros((num_agents,num_agents))
for i in range(num_agents):
    for j in range(i,num_agents):
        distance_all[i][j]=distance_between(agents[i],agents[j])
        
        