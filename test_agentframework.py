# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:40:31 2019

@author: gycdb
"""
import pytest
import agentframework_tryout as ag
import csv
import matplotlib.pyplot



class TestAgents:
    ENVIRONMENT=[[20,10],[10,20]]
    #matplotlib.pyplot.imshow(environment_simple)

    AGENTS=[]
    for i in range(2):
        AGENTS.append(ag.Agent(self.ENVIRONMENT,self.AGENTS))
    AGENT1=AGENTS[0]
    AGENT2=AGENTS[1]
    def test_position(self):
        assert self.AGENT1.x in [0,1]
    def test_agent_eat(self):
        self.AGENT1.eat()
        assert self.AGENT1.store>0 
        