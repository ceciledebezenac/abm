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
import agentframework9 as ag
import csv
import subprocess
import requests
import bs4


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

#get access to the x and y data:


r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
print(td_ys)
print(td_xs)

#check if there is enough data for all the agents, if not limit the simulation to the data:
if num_agents > len(td_xs):
    num_agents=len(td_xs)
    print('The number of agents has been limited to '+str(len(td_xs))+' agents because of limited data')

#get the agents to the right spot based on the data    
agents=[]
for i in range(num_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(ag.Agent(environment, agents, y, x))


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

def stop():
    global carry_on 
    carry_on=False



def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.show()

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

#number of agents with Spinbox
number_agents = tkinter.StringVar()
number_agents.set(100)
box_ag = tkinter.Scale(Frame_argument,from_=0,to=1000,resolution=10,orient=tkinter.HORIZONTAL,\
length=100,width=20,label="agents",tickinterval=500,variable=number_agents)
box_ag.pack(padx=30,pady=10)

#number of simulations with Spinbox
number_iterations = tkinter.StringVar()
number_iterations.set(10)
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