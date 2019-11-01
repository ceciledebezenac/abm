import agentframework
import unittest


#create data for test : 4x4 environment and 3 agents. neighborhood that includes all agents.
env_data = [[20,20,20,20],[20,20,20,20],[20,20,20,20],[20,20,20,20]]
agent_data=[]
agent_data.append(agentframework.Agent(env_data,agent_data,0,0))
agent_data.append(agentframework.Agent(env_data,agent_data,0,2))
agent_data.append(agentframework.Agent(env_data,agent_data,0,1))
neighborhood=10
baby_energy=20


class TestAgent(unittest.TestCase):
    """
    def __init__(self):

        '''Create data for tests.'''

        self.env_data = [[20,20,20,20],[20,20,20,20],[20,20,20,20],[20,20,20,20]]
        self.agent_data = [agentframework.Agent(self.env_data,self.agent_data,0,0),agentframework.Agent(self.env_data,self.agent_data,0,2),agentframework.Agent(self.env_data,self.agent_data,0,1)]
        self.neighborhood=10
    """

    def test_attributes(self):
        '''
        Test existance and relevance of attributes
        '''
        self.assertEqual(agent_data[0].x,0)
        self.assertEqual(agent_data[0].y,0)
        self.assertEqual(agent_data[0].environment,env_data)
        self.assertEqual(agent_data[0].others,agent_data)
        self.assertEqual(agent_data[0].store,0)
        self.assertTrue(agent_data[0].hunger<=1)
        self.assertTrue(agent_data[0].share_will<=0.5)



    def test_move(self):
        '''
        Test agent has effectively moved according to given rules.
        '''
        agent_data[0].move()
        self.assertTrue(agent_data[0].x==1 or agent_data[0].x==3 )

    def test_eat(self):
        '''
        Test if agent has effectively eaten.
        '''
        agent_data[0].eat(quantity=5)
        self.assertEqual(agent_data[0].store,agent_data[0].hunger*5)
        self.assertEqual(env_data[agent_data[0].y][agent_data[0].x],20-agent_data[0].store)


    def test_distance(self):
        '''
        Test the distance_between() method.
        '''
        #test distance with agents that have not moved yet.
        self.assertEqual(agent_data[1].distance_between(agent_data[2]),1)


    def test_share(self):
        '''
        Test sharing method.
        '''
        agent_data[0].share_with_neighbors(neighborhood)
        self.assertEqual(len(agent_data[0].neighbors),len(agent_data))
        self.assertTrue((agent_data[1].store > 0) & (agent_data[2].store > 0))

    def test_reproduce(self):
        '''
        Test reproduce() method.
        '''
        agent_data[0].store=50
        agent_data[0].reproduce(20)
        self.assertEqual(agent_data[0].store,30)
        self.assertEqual(len(agent_data),4)
        self.assertEqual(agent_data[3].x,agent_data[0].x)
        self.assertEqual(agent_data[3].y,agent_data[0].y)


    def test_print(self):
        self.assertEqual(agent_data[0].__str__(),'y:'+str(agent_data[0].y)+'\nx:'+str(agent_data[0].x)+'\nstore:'+str(agent_data[0].store)+'\n'+str(len(agent_data[0].others))+' other agents share the same environment'+'\nneighbors: '+str(len(agent_data[0].neighbors)))

if __name__ == '__main__':
    unittest.main()
