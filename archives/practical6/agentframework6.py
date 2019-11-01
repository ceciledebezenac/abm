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
    def __init__(self, environment):#the self variable tells the agent how to call himself
        '''
        initialise random coordinates, agent food storage and agent environment.
        '''
        self._y = rd.randint(0,99)
        self._x = rd.randint(0,99)
        self.environment=environment
        self.store=0
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
            self.y = (self.y + 1) % 100
        else:
            self.y = (self.y - 1) % 100

        if rd.random()<0.5:
            self.x = (self.x + 1) % 100
        else:
            self.x = (self.x - 1) % 100

    def eat(self):
        '''Agent eat method: check food in environment and eat 10 or what is left if less.'''
        food_left=self.environment[self.y][self.x]
        self.environment[self.y][self.x] -= min(10,food_left)#an agent can on;y eat how much food is actually there
        self.store += min(10,food_left)

    def give_it_up(self):
        '''Agent delesting method: under conditions can store in the environment all of its internal storage.'''
        self.environment[self.y][self.x]+=self.store
        self.store=0

    def __str__(self):
        '''return the values of attributes if printed.'''
        return 'y:'+str(self.y)+'\nx:'+str(self.x)+'\nstore:'+str(self.store)
