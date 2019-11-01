#!/usr/bin/env python
# coding: utf-8

# # Model from agentframework : GUI

# ## Practical 9a : interface creation

# In[1]:


import tkinter
import sys
import random as rd
import numpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation
import agentframework9a as ag
import csv
import subprocess
import requests
import bs4




# #### Global Enivronment

# In[2]:

#read the text file in csv and put it into a list to be able to plot it.
with open('in.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    environment=[]
    for row in csv_reader:
        rowlist=[]
        for value in row:
            rowlist.append(int(value))
        environment.append(rowlist)

#Default variable values:
#number of agents in the model
number_agents=100
#number of times to run the model(methods)
number_iterations=10
#ray for neighborhood
neighborhood=10
#limit for energy to move
hunger_threshold=10
starvation_threshold=10
baby_energy=50


# ### Update input

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

#######################
### MODEL ANIMATION ###
#######################

#Function to let agents die: just to make the update function more explicit.
def die(agent):
    del agent


#inititialise the figure
fig = plt.figure(figsize=(10, 10))
ax = fig.add_axes([0, 0, 1, 1])

#add a variable for a potential stopping condition to control animation
carry_on = True
#a is used to count time outside of the run function
a=0
#keep count of the dead agents
dead=0


#initialise agent list
agents=[]


### Define a step in the model

def update(f):
    '''Update function to reiterate Agent action.
    Argument: f a given iteration function.
    Returns: new image of enivronment and agents after
        - checking store
        - moving
        - eating
        - sharing
        - reproducing
        - dying if starved.
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

    #plot the agents in their environment after action.
    for i in range(number_agents-dead):
        plt.scatter(agents[i].x,agents[i].y)
    plt.imshow(environment)

    #keep count of the time with f refering to the iteration fucntion described below:
    plt.text(270, 270, str(a),fontsize=14)
    plt.text(30,30 , str(dead)+' agents are dead',fontsize=14)
    #shuffle randomly: note that as we have not fixed each agents color, these will randomly change color as the default color allocation is ordered in python.
    rd.shuffle(agents)


def gen_function():
    '''Generating function giving rules of iteration for animation.
    Returns: threshold stopping and carry_on condition.
    '''
    global a
    global carry_on
    while (a < number_iterations) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1


##########################
### INTERFACE COMMANDS ###
##########################

def stop():
    '''Stop or restart animation.
    Global arguments : carry_on.
    Return          : modified value of carry_on to pause the animation.
    '''
    global carry_on #add carry_on as global to change outside the function
    if carry_on==True:
        carry_on=False
    else:
        carry_on=True
    #carry_on with the animation if True
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

def run_to_end():
    '''Animation command : run till manually stopped by stop().
    Global arguments :
        - agents : list of Agents
                   create agents if at the first step of the animation.
        -  a : integers
               time count.
    Returns : animation plot in canvas.
    '''
    global agents
    global a
    a=0
    for i in range(int(number_agents)):
        agents.append(ag.Agent(environment, agents))
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

def run_once():
    '''Animation command : run one step of the animation > one call of update().
    Global arguments :
        - agents : list of Agents
                   create agents if at the first step of the animation.
        -  a : integers
               time count.
    Returns : animation plot in canvas.
    '''
    global agents
    global a
    if a==0:
        for i in range(int(number_agents)):
            agents.append(ag.Agent(environment, agents))
    animation = matplotlib.animation.FuncAnimation(fig, update, 1, repeat=False)
    a=a+1
    canvas.draw()

def change_parameters():
    '''
    Change paramter command : access scale values and update model variables before running.
    Global arguments :
        - number_agents : integer
                          the number of agents that are to be created.
        - number_iterations : integer
                              the number of single runs the run_to_end() should consider.
        - baby_energy : integer
                        food storage needed to reproduce.
    Returns : New manually fixed values for global arguments.
    '''
    global number_agents
    global number_iterations
    global baby_energy
    number_agents=int(box_ag.get())
    number_iterations=int(box_ite.get())
    baby_energy=int(box_rep.get())
    print(box_ite.get())


########################
### INTERFACE DESIGN ###
########################


### MAIN FRAME

#create the main frame root
root = tkinter.Tk()
root.wm_title("Model")

#Create menu bar and menu command : run_to_end
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run_to_end)

### SECONDARY FRAMES

#create the frame for the model animation:
Frame_model = tkinter.Frame(root,borderwidth=2,relief=tkinter.GROOVE)
Frame_model.pack(side=tkinter.LEFT,padx=10,pady=10)
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=Frame_model)
canvas._tkcanvas.pack(side=tkinter.TOP)#, fill=tkinter.BOTH, expand=1)

#create the frame for model adjustment and animation control:
Frame_argument = tkinter.Frame(root,borderwidth=2,relief=tkinter.GROOVE)
Frame_argument.pack(side=tkinter.LEFT,padx=10,pady=10)


### BUTTONS AND SCALE

#number of agents with Scale
box_ag = tkinter.Scale(Frame_argument,from_=0,to=1000,resolution=10,orient=tkinter.HORIZONTAL,\
length=100,width=20,label="agents",tickinterval=500)
box_ag.pack(padx=30,pady=10)

#number of simulations with Scale
num_iterations = tkinter.IntVar()
num_iterations.set(10)
box_ite = tkinter.Scale(Frame_argument,from_=0,to=1000,resolution=10,orient=tkinter.HORIZONTAL,\
length=100,width=20,label="iterations",tickinterval=500)
box_ite.pack(padx=30,pady=10)

# energy needed for reproducing
reproduce_energy = tkinter.IntVar()
reproduce_energy.set(10)
box_rep = tkinter.Scale(Frame_argument,from_=0,to=1000,resolution=10,orient=tkinter.HORIZONTAL,\
length=100,width=20,label="reproduction energy",tickinterval=500)
box_rep.pack(padx=30,pady=10)

#Apply button for these scale buttons
ButtonApply = tkinter.Button(Frame_argument, text ='Apply parameters', command = change_parameters)
ButtonApply.pack()

#button to run once
ButtonRunOnce = tkinter.Button(Frame_argument, text ='Run 1', command = run_once)
ButtonRunOnce.pack(padx=30,pady=10)

#button to run to end
ButtonRun = tkinter.Button(Frame_argument, text ='Run all', command = run_to_end)
ButtonRun.pack(padx=30,pady=10)

#button to pause the animation and restart from where it left off
ButtonStop = tkinter.Button(Frame_argument, text ='Stop', command = stop)
ButtonStop.pack(padx=30,pady=10)

#Quit button
ButtonQuit = tkinter.Button(Frame_argument, text ='Quit', command = root.destroy)
ButtonQuit.pack(side=tkinter.BOTTOM,padx=30,pady=10)


tkinter.mainloop()
