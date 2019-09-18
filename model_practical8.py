# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:08:04 2019

@author: gycdb
"""
import sys
import random
import numpy
import matplotlib.pyplot
import matplotlib.animation
import agentframework7 as ag
import csv
import subprocess


#defining arguments from command line:
arguments = len(sys.argv) - 1
if arguments==3:
    # output arguments
    if float(sys.argv[1])>0:
        num_iterations=int(sys.argv[1])
    else :#error ;essage if not
        print('The iteration argument is not a valid number of iterations')
    
    if float(sys.argv[2])>0 :
        num_agents=int(sys.argv[2])
    else :#error ;essage if not
        print('The agent argument is not a valid number of agents')
    
    if float(sys.argv[3])>0 :
        neighborhood=float(sys.argv[3])
    else :#error message if not
        print('The agent argument is not a valid distance')

else :#defqult vqlues for arguments
    print('running with defaults')
    num_iterations=10
    num_agents=100
    neighborhood=50

#reqd the text file in csv qnd put it into q list to be able to plot it.        
with open('in.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    environment=[]
    for row in csv_reader:
        rowlist=[]
        for value in row:
            rowlist.append(int(value))
        environment.append(rowlist)
        
#generate a number of agents

agents=[]
for i in range (num_agents):
    others=agents#this list os not full to start with but will change as it goes. this works as we test it on the agent0
    agents.append(ag.Agent(environment,others))


fig = matplotlib.pyplot.figure(figsize=(10, 10))
ax = fig.add_axes([0, 0, 1, 1])

carry_on = True	
	
def update(f):
    
    fig.clear()   
    global carry_on
    for i in range(num_agents):
        agents[i].move()
        agents[i].eat()
    #other criteriq for stopping, for example a 5% chance of stopping here at every iteration
    #if random.random() < 0.05:
        #carry_on = False
        #print("stopping condition")
    
    for i in range(num_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
    matplotlib.pyplot.imshow(environment)
    #keep count of the time :
    matplotlib.pyplot.text(270, 270, str(f),fontsize=14)
    
      
		
def gen_function():
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (a < num_iterations) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1


#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=10)
animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)

matplotlib.pyplot.show()

#how do you close the plot once it is done?