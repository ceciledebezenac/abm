#!/usr/bin/env python
# coding: utf-8

# In[5]:
import random as rd


#create the class Agent for model
class Agent():
    '''
    Python class of Agent

        Attributes :
        - x,y : integer, spatial coordinates.
        - environment (bound_y and bound_x): integer list, food available.
        - store : int, food storage.
        - others : list of Agents, other agents in environment.
        - share_will: float <0.5, propencity to share.
        - neighbors : list of Agents, agents within a range from self.
        - neighbors_dist : list of float, distance between neighbors.
        - fertility:
        - starvation:
        - hunger:

        Methods :
        - __init__: initialise coordinates to x_value and y_value
        - move(): move agent to neighboring cell with uniform random process in tore-like grid(queen neighborhood).
        - gety(): access self._y with self.y.
        - getx(): access self._x with self.x.
        - sety(): modify self._y with self.y.
        - setx(): modify self._x with self.x.
        - eat():  take food from environment and add it to store.
        - give_it_up: drop store in environment when too heavy.
        - distance_between: compute distance from self to other agents.
        - share_with_neighbors: average store value with other agents in given range.
        - reproduce:
        -__str__: print attribute values.

    '''

    #initialise the agent by giving it attributes : here random x and y
    def __init__(self, environment,others, y_value=None, x_value=None):#the self variable tells the agent how to call himself
        '''
        initialise agent with attributes
        Arguments :
            - environment : 2D grid of integers
                            food storage
            - others :      list of Agent instances.
                            the other agents in the environment
            - y_value :     integer
                            y value for attribute _y
            - x_value :     integer
                            x value for attribute
        '''
        #the environment the agent belongs to
        self.environment=environment
        #coordinates
        if y_value==None :
            self._y = rd.randint(0,len(self.environment))
        else :
            self._y = y_value
        if x_value==None :
            self._x = rd.randint(0,len(self.environment[0]))
        else :
            self._x = x_value
        #the food stored up
        self.store=0
        #all the other agents (including themselves)
        self.others=others
        self.starvation=0
        #simple feritlity, 0 and 1
        self.fertility=rd.randint(0,1)
        #propencity to share with others :
        self.share_will=rd.uniform(0,0.5)
        self.hunger=rd.random()
        self.neighbors=[]
        self.neighbor_dist=[]

    def gety(self):
        '''getter property for y coordinate.'''
        return self._y
    def getx(self):
        '''getter property for x coordinate.'''
        return self._x
    def setx(self, value):
        '''setter property for y coordinate.'''
        self._x = value
    def sety(self, value):
        '''setter property for x coordinate.'''
        self._y = value
    x=property(getx,setx)
    y=property(gety,sety)

    #define the method of moving that
    def move(self):
        '''Agent move method: independantly increment by 1 or -1 y and x with probability 0.5.'''
        if rd.random()<0.5:
            self.y = (self.y + 1) % len(self.environment)
        else:
            self.y = (self.y - 1) % len(self.environment)

        if rd.random()<0.5:
            self.x = (self.x + 1) % len(self.environment[0])
        else:
            self.x = (self.x - 1) % len(self.environment[0])

    def eat(self, quantity=10):
        '''Agent eat method: check food in environment and eat 10 or what is left if less.
        Arguments :
            - quantity : integer
                         initial value of food eaten per turn.'''
        food_left=self.environment[self.y][self.x]
        self.environment[self.y][self.x] -= min(self.hunger*quantity,food_left)#an agent can on;y eat how much food is actually there
        self.store += min(self.hunger*quantity,food_left)

    def give_it_up(self):
        '''Agent delesting method: under conditions can store in the environment all of its internal storage.'''
        self.environment[self.y][self.x]+=self.store
        self.store=0

    def distance_between(self,other_agent):
        '''Return distance between self and other agent.
        Arguments :
            - other_agent : instance of class Agent
                            other agent from whom the distance is calculated.
        '''
        dist=((self.x-other_agent.x)**2+(self.y-other_agent.y)**2)**0.5
        return(dist)

    def share_with_neighbors(self,neighborhood):
        '''
        Agent sharing method: can share food with other agents if closer than given threshold.
        Two agents share by averaging their storage.
        Neighboring agents are added to the list of neighbors
        Arguments :
            - neighborhood : float or integer
                             range of neighborhood.
        '''
        neighbors=[]
        neighbor_dist=[]
        for other_agent in self.others:
            dist=self.distance_between(other_agent)
            if dist<=neighborhood:
                #add the condition the other agent has more needs then the agent himself.
                if other_agent.store < self.store:
                    sum_store=self.store + other_agent.store
                    average_storage= sum_store/2
                    self.store=average_storage
                    other_agent.store=average_storage
                neighbors.append(other_agent)
                neighbor_dist.append(dist)
        #note self is included in neighbors. This is not a big problem here as averaging out won't change store value.
        self.neighbors=neighbors
        self.neighbor_dist=neighbor_dist

    def reproduce(self,baby_energy):
        '''Create new agent in same location'''
        self.others.append(Agent(self.environment,self.others,self.y,self.x))
        self.store-=baby_energy


    def __str__(self):
        '''return the values of attributes if printed.'''
        return 'y:'+str(self.y)+'\nx:'+str(self.x)+'\nstore:'+str(self.store)+'\n'+str(len(self.others))+' other agents share the same environment'+'\nneighbors: '+str(len(self.neighbors))
