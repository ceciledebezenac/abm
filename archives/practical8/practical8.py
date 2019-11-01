#!/usr/bin/env python
# coding: utf-8

# # Model from agentframework : Animation / Beahviour!

# ## Practical 8 : model animation



import random as rd
import agentframework8 as ag
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys


# #### Global Enivronment

#read the text file in csv and put it into a list to be able to plot it.
with open('in.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    environment=[]
    for row in csv_reader:
        rowlist=[]
        for value in row:
            rowlist.append(int(value))
        environment.append(rowlist)
#print('length of environment is ' + str(len(environment)))

# #### Global variables for model and simulation

#create global variables for the model with default values

#number of agents in the model
number_agents=100
#number of times to run the model(methods)
number_iterations=50
#ray for neighborhood
neighborhood=10
#limit for energy to move
hunger_threshold=10
#time spent with no food
starvation_threshold=10
#energy needs for reproducing
baby_energy=50



#use arguments specified in python command line :
arguments = len(sys.argv) - 1
if arguments>0:
    # output arguments
    if float(sys.argv[1])>0:
        number_iterations=int(sys.argv[1])
    else :
        print('The iteration argument is not a valid number of iterations, default will be used.')

    if float(sys.argv[2])>0:
        number_agents=int(sys.argv[2])
    else :
        print('The agent argument is not a valid number of agents, default will be used.')

    if float(sys.argv[3])>0:
        neighborhood=float(sys.argv[3])
    else :
        print('The agent argument is not a valid distance, default will be used.')
    if arguments >3:
        print('Too many arguments have been given, only the first 3 will be considered.')
else :
    print('default running.')


# #### Agent creation

#create number_agents of agents from agentframework7 class Agent, adding environment to the arguments and the list of agents being created.
#We note this list does not need to be full when added, so we can prograssively fill it up as agents are being created.
agents=[]
for i in range (number_agents):
    agents.append(ag.Agent(environment,agents))


# #### Getting the model to work

#save the amount stored by agents after num_iterations in a file
def add_store_info(list_agents,num_iter,num_agents,file_name='store_file'):
    '''
    Append the values of store for all agents after a number of iterations.
    '''
    #create the storage row
    storage=[num_iter,num_agents]+[list_agents[i].store for i in range(num_agents)]

    #append it to existing doc
    with open(file_name+'.csv', mode='a') as store_file:#the 'a' writing enables appending to existing file
        storage_writer = csv.writer(store_file, delimiter=',')
        storage_writer.writerow(storage)#store the data in one row

#save the new environment into a new csv file
def update_environment(environment,num_iter, num_agents,file_name='environment_after_update'):
    '''
    Update possible existing file with new values for environment.
    '''
    f2 = open(file_name+'.csv', 'w', newline='')#the 'w' will overwrite the exiting environment file
    writer = csv.writer(f2, delimiter=',')
    writer.writerow(['num_iterations','num_agents'])
    writer.writerow([num_iter,num_agents])
    for row in environment:
        writer.writerow(row) # List of values.
    f2.close()

def die(agent):
    del agent


fig = plt.figure(figsize=(10, 10))
ax = fig.add_axes([0, 0, 1, 1])

carry_on = True
dead=0

def update(f):
    '''Update function to reiterate Agent action.
    Argument: f a given iteration function.
    Returns: new image of enivronment and agents.
    '''

    fig.clear()#make sure python is not plotting on top of old data.
    global carry_on#a global vairable that can be accessed out of the function.
    global dead
    #one iteration of action for all agents
    for i in range(number_agents):

        #check energy level
        if agents[i].store > hunger_threshold:
            #update food state : starving or store>hunger_threshold:
            agents[i].starvation=0
        else:
            agents[i].starvation+=1

        #All agents can move to find food
        agents[i].move()
        #agents eat what they can find in their environment.
        agents[i].eat(quantity=10)

        #if agents are willing to share and have a store over the threshold level, they can chare with neighbors.
        if rd.random()<agents[i].share_will:
                agents[i].share_with_neighbors(neighborhood)

        #reproduce if right gender, given a probability of 0.5
        if rd.random()*agents[i].fertility > 0.5 and agents[i].store > baby_energy :
            agents[i].reproduce(baby_energy)

        if agents[i].starvation > starvation_threshold:
            die(agents[i])
            dead+=1
            #add the x and y and the energy store to the agents
        #for a simpler animation we do not include sharing here.

    #criteria for stopping, for example a 5% chance of stopping here at every iteration.
    if rd.random() < 0.05:
        carry_on = False
        print("stopping condition")

    #plot the agents in their environment after action.
    for i in range(number_agents-dead):
        plt.scatter(agents[i].x,agents[i].y)
    plt.imshow(environment)

    #keep count of the time with f refering to the iteration fucntion described below:
    plt.text(270, 270, str(f),fontsize=14)
    plt.text(30,30 , str(dead)+' agents are dead',fontsize=14)
    #shuffle randomly
    rd.shuffle(agents)



def gen_function():
    '''Generating function giving rules of iteration for animation.
    Returns: threshold stopping and carry_on condition.
    '''
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (a < number_iterations) :#& (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1


#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=10)
animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)

plt.show()
