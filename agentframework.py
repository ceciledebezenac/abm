# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 09:43:44 2019

@author: gycdb

agentframework for model
"""
import random
class Agent():
    def __init__(self,environment):
        self._y = None
        self._x = None
        self.environment=environment
        self.store=0
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
        self.environment[self.y][self.x] -= min(10,food_left)
        self.store += min(10,food_left)
    def __str__(self):
        return 'y:'+str(self.y)+'\nx:'+str(self.x)+'\nstore:'+str(self.store)
    
    