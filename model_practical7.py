# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:08:04 2019

@author: gycdb
"""
import sys
import matplotlib.pyplot
import matplotlib.animation
import agentframework7 as ag
import csv

fig = matplotlib.pyplot.figure(figsize=(10, 10))
ax = fig.add_axes([0, 0, 1, 1])

arguments = len(sys.argv) - 1
if arguments>3:
    # output arguments
    if float(sys.argv[1])>0:
        num_iterations=int(sys.argv[1])
    else :
        print('The iteration argument is not a valid number of iterations')
    
    if float(sys.argv[2])>0:
        num_agents=int(sys.argv[2])
    else :
        print('The agent argument is not a valid number of agents')
    
    if float(sys.argv[3])>0:
        neighborhood=float(sys.argv[3])
    else :
        print('The agent argument is not a valid distance')

else :#defqult vqlues for arguments
    print('default running')
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
        
#generate a nu;ber of agents

agents=[]
for i in range (num_agents):
    others=agents#this list os not full to start with but will change as it goes. this works as we test it on the agent0
    agents.append(ag.Agent(environment,others))

#move all the agents a number of times
for j in range(num_iterations):
    for i in range(num_agents):
        agents[i].move()
        agents[i].eat()
storage=[num_iterations,num_agents,neighborhood]+[agents[i].store for i in range(num_agents)]

#save the amount stored by agents after num_iterations in a file    
with open('store_file.csv', mode='a') as store_file:#the 'a' writing enables us to append to existing file
    storage_writer = csv.writer(store_file, delimiter=',')
    storage_writer.writerow(storage)#we store the data in one row    

#we can now save the new environment into a new csv file        
f2 = open('environment_after_update.csv', 'w', newline='')#the 'w' will overwrite the exiting environment file
writer = csv.writer(f2, delimiter=',')
writer.writerow(['num_iterations','num_agents','neighborhood'])
writer.writerow([num_iterations,num_agents,neighborhood])
for row in environment:
    writer.writerow(row) # List of values.
f2.close()

#Plot the different qgents on a limited grid
#max_x=max(agents,key=operator.itemgetter(1))

matplotlib.pyplot.ylim(0, 300)
matplotlib.pyplot.xlim(0, 300)

for i in range(num_agents):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
                    
#plot the agents in their environment.    
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()


