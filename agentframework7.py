# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 09:43:44 2019

@author: gycdb

agentframework for model
"""
import random
class Agent():
    def __init__(self,environment,others):
        self._y = None
        self._x = None
        self.environment=environment
        self.others=others
        self.neighbors=None
        self.store=0
        self.hunger=random.random()#this is a hunger parameter that tells the agent how much it will want to eat. This also helps test our sharing method
        bound_y=len(environment)
        bound_x=len(environment[0])
        def randomise(self):
            self._x=random.randint(0,bound_x)
            self._y=random.randint(0,bound_y)
        randomise(self)
    def gety(self):
        return self._y
    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def sety(self, value):
        self._y = value
    x=property(getx,setx)
    y=property(gety,sety)
    
    def move(self):
        bound_y=len(self.environment)
        bound_x=len(self.environment[0])
        if random.random() < 0.5:
            self.x = (self.x + 1) % bound_x
        else:
            self.x = (self.x - 1) % bound_x

        if random.random() < 0.5:
            self.y = (self.y + 1) % bound_y
        else:
            self.y = (self.y - 1) % bound_y
    
    def eat(self): # can you make it eat what is left?
        food_left=self.environment[self.y][self.x]
        self.environment[self.y][self.x] -= min(10*self.hunger,food_left)#an agent can on;y eat how much food is actually there
        self.store += min(10*self.hunger,food_left)
    
    def distance_between(self,other_agent):
        dist=((self.x-other_agent.x)**2+(self.y-other_agent.y)**2)**0.5
        return(dist)
    
    def share_with_neighborhood(self,neighborhood):
        neighbors=[]
        for other_agents in self.others:
            dist=self.distance_between(other_agents)
            if dist<=neighborhood:
                sum_store=self.store + other_agents.store
                average_storage= sum_store/2
                self.store=average_storage
                other_agents.store=average_storage
                neighbors.append(other_agents)
        self.neighbors=neighbors
        print('I have shared with '+str(len(neighbors)-1)+' neighbor(s)')
        #the agent shares with one agent at a time. sharing is a bilateral relation, 
        #and an agent will share more with the agents that come up first. unfortunately,
        #it is not necessarily the closest that come up first.
    
    def __str__(self):
        return 'y:'+str(self.y)+'\nx:'+str(self.x)+'\nstore:'+str(self.store)
    
    
 