#!/usr/bin/env python
# coding: utf-8

# In[5]:
import random as rd


#create the class Agent for model
class Agent():
    '''
    Python class of Agent

    attributes :
    - coordinates x and y

    methods :
    - __init__: initialise coordinates to random integers in [0,100[
    - move(): move agent to neighboring cell with uniform random process in tore-like grid(queen neighborhood)
    '''

    #initialise the agent by giving it attributes : here random x and y
    def __init__(self, environment,others):#the self variable tells the agent how to call himself
        '''
        initialise random coordinates, agent food storage and agent environment.
        '''
        self.bound_y=len(environment)
        self.bound_x=len(environment[0])
        self._y = rd.randint(0,self.bound_y)
        self._x = rd.randint(0,self.bound_x)
        self.environment=environment
        self.store=0
        self.others=others
        self.neighbors=[]
        self.neighbor_dist=[]
        #def randomise(self):
            #self._x=random.randint(0,bound_x)
            #self._y=random.randint(0,bound_y)
        #randomise(self)
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
            self.y = (self.y + 1) % self.bound_y
        else:
            self.y = (self.y - 1) % self.bound_Y

        if rd.random()<0.5:
            self.x = (self.x + 1) % self.bound_x
        else:
            self.x = (self.x - 1) % self.bound_x

    def eat(self):
        '''Agent eat method: check food in environment and eat 10 or what is left if less.'''
        food_left=self.environment[self.y][self.x]
        self.environment[self.y][self.x] -= min(10,food_left)#an agent can on;y eat how much food is actually there
        self.store += min(10,food_left)

    def give_it_up(self):
        '''Agent delesting method: under conditions can store in the environment all of its internal storage.'''
        self.environment[self.y][self.x]+=self.store
        self.store=0

    def distance_between(self,other_agent):
        '''Return distance between self and other agent.'''
        dist=((self.x-other_agent.x)**2+(self.y-other_agent.y)**2)**0.5
        return(dist)

    def share_with_neighbors(self,neighborhood):
        '''
        Agent sharing method: can share food with other agents if closer than given threshold.
        Two agents share by averaging their storage.
        Neighboring agents are added to the list of neighbors.
        '''
        neighbors=[]
        neighbor_dist=[]
        for other_agent in self.others:
            dist=self.distance_between(other_agent)
            if dist<=neighborhood:
                sum_store=self.store + other_agent.store
                average_storage= sum_store/2
                self.store=average_storage
                other_agent.store=average_storage
                neighbors.append(other_agent)
                neighbor_dist.append(dist)
        #note self is included in neighbors. This is not a big problem here as averaging out won't change store value.
        self.neighbors=neighbors
        self.neighbor_dist=neighbor_dist

    def __str__(self):
        '''return the values of attributes if printed.'''
        return 'y:'+str(self.y)+'\nx:'+str(self.x)+'\nstore:'+str(self.store)+'\n'+str(len(self.others))+' other agents share the same environment'+'\nneighbors: '+str(len(self.neighbors))
