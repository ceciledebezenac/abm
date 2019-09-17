# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:08:04 2019

@author: gycdb
"""
import random
import numpy
import matplotlib.pyplot
import operator
import agentframework as ag
import csv

#define the function of distance
def distance_between(agent1,agent2):
    dist=((agent1.x-agent2.x)**2+(agent1.y-agent2.y)**2)**0.5
    return(dist)


#reqd the text file in csv qnd put it into q list to be able to plot it.        
with open('in.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    environment=[]
    for row in csv_reader:
        rowlist=[]
        for value in row:
            rowlist.append(int(value))
        environment.append(rowlist)
        
#generate a nu;ber of agents
num_iterations=100
num_agents=10
agents=[]
for i in range (num_agents):
    agents.append(ag.Agent(environment))

#move all the agents a number of times

for j in range(num_iterations):
    for i in range(num_agents):
        agents[i].move()
        agents[i].eat()
storage=[agents[i].store for i in range(num_agents)]

#save the amount stored by agents after num_iterations in a file    
with open('store_file.csv', mode='a') as store_file:#the 'a' writing enables us to append to existing file
    storage_writer = csv.writer(store_file, delimiter=',')
    storage_writer.writerow(storage)#we store the data in one row    

#we can now save the new environment into a new csv file        
f2 = open('environment_100.csv', 'w', newline='')#the 'w' will overwrite the exiting environment file
writer = csv.writer(f2, delimiter=',')
for row in environment:
    writer.writerow(row) # List of values.
f2.close()

#Plot the different qgents on a limited grid
#max_x=max(agents,key=operator.itemgetter(1))

matplotlib.pyplot.ylim(0, 100)
matplotlib.pyplot.xlim(0, 100)

for i in range(num_agents):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
#matplotlib.pyplot.scatter(max_x[1],max_x[0],color='red')

#compute the matrix of distances between agents
distance_all=numpy.zeros((num_agents,num_agents))
for i in range(num_agents):
    for j in range(i,num_agents):
        distance_all[i][j]=distance_between(agents[i],agents[j])
        
        


        
#plot the agents in their environment.    
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()
