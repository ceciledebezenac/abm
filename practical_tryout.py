# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 09:38:09 2019

@author: gycdb
"""
import tkinter
import sys
import random
import numpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation
import agentframework_tryout as ag
import csv



#reqd the text file in csv qnd put it into q list to be able to plot it.        
with open('in.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    environment=[]
    for row in csv_reader:
        rowlist=[]
        for value in row:
            rowlist.append(int(value))
        environment.append(rowlist)



#agents=[]
#for i in range(int(number_agents.get())):
    #agents.append(ag.Agent(environment, agents))


fig = matplotlib.pyplot.figure(figsize=(10, 10))
ax = fig.add_axes([0, 0, 1, 1])

carry_on = True	
	
def update(f):
    
    fig.clear()   
    global carry_on
    global agents
    global num_agents
    for agent in agents:
        agent.move()
        agent.eat()
    #other criteriq for stopping, for example a 5% chance of stopping here at every iteration
    #if random.random() < 0.05:
        #carry_on = False
        #print("stopping condition")
    
    for agent in agents:
        matplotlib.pyplot.scatter(agent.x,agent.y)
    matplotlib.pyplot.imshow(environment)
    #keep count of the time :
    matplotlib.pyplot.text(270, 270, str(f),fontsize=14)
    
      
		
def gen_function():
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1

def stop():
    global carry_on 
    carry_on=False


def run():
    global agents
    global num_agents
    agents=[]
    for i in range(num_agents):
        agents.append(ag.Agent(environment, agents))
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.show()

def change_agents():
    global num_agents
    num_agents=number_agents.get()

#create the main frame root
root = tkinter.Tk()
root.wm_title("Model")

#create the frame for the model animation:
Frame_model = tkinter.Frame(root,borderwidth=2,relief=tkinter.GROOVE)
Frame_model.pack(side=tkinter.LEFT,padx=10,pady=10)
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=Frame_model)
canvas._tkcanvas.pack(side=tkinter.TOP)#, fill=tkinter.BOTH, expand=1)

#create the frame for model adjustment and animation control:
Frame_argument = tkinter.Frame(root,borderwidth=2,relief=tkinter.GROOVE)
Frame_argument.pack(side=tkinter.LEFT,padx=10,pady=10)

#Quit button
ButtonQuit = tkinter.Button(Frame_argument, text ='Quit', command = root.destroy)
ButtonQuit.pack(side=tkinter.BOTTOM,padx=30,pady=10)

#number of agents with Scale
number_agents = tkinter.IntVar()
number_agents.set(10)
box_ag = tkinter.Scale(Frame_argument,from_=0,to=1000,resolution=10,orient=tkinter.HORIZONTAL,\
length=100,width=20,label="agents",tickinterval=500,variable=number_agents,command=change_agents)
box_ag.pack(padx=30,pady=10)


#number of simulations with Spinbox
number_iterations = tkinter.IntVar()

box_ite = tkinter.Scale(Frame_argument,from_=0,to=1000,resolution=10,orient=tkinter.HORIZONTAL,\
length=100,width=20,label="iterations",tickinterval=500,variable=number_iterations)
box_ite.pack(padx=30,pady=10)

#Stop button
ButtonStop = tkinter.Button(Frame_argument, text ='Stop', command = stop)
ButtonStop.pack(padx=30,pady=10)


#Stop Resume

ButtonRun = tkinter.Button(Frame_argument, text ='Run', command = run)
ButtonRun.pack(padx=30,pady=10)

menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

# Création d'un widget Button (bouton Quitter)


tkinter.mainloop()

 # Wait for interactions.
#how do you close the plot once it is done?


#http://fsincere.free.fr/isn/python/cours_python_tkinter.php