# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:11:44 2019

@author: gycdb
"""

import subprocess

agent_numbers = [1, 2, 5, 10, 20, 50, 100]

for an in agent_numbers:
    # Run model for this number of agents
    subprocess.run('python model_practical8.py 10 {0} 10'.format(an))