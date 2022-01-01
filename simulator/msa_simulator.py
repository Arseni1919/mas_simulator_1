from GLOBALS import *

"""
Full API:
Attributes: 
    agents, num_agents, possible_agents, max_num_agents, observation_spaces, action_spaces

Methods: 
    render(mode='human'), 
    seed(seed=None), close(), 
    observation_space(agent), 
    action_space(agent)
    
    step(actions): receives a dictionary of actions keyed by the agent name. Returns the observation dictionary, 
                   reward dictionary, done dictionary, and info dictionary, where each dictionary is keyed by the agent.
    
    reset(): resets the environment and returns a dictionary of observations (keyed by the agent name)

Functions:
    random_demo(env, render=True, episodes=1)

"""


class MSASimulatorParallel:

    def __init__(self, num_agents):
        self.agents = [Agent(i) for i in range(num_agents)]
        self.num_agents = num_agents
        self.possible_agents = None
        self.max_num_agents = None
        self.observation_spaces = None
        self.action_spaces = None

    def seed(self):
        pass

    def observation_space(self, agent):
        pass

    def action_space(self, agent):
        pass

    def step(self, actions):
        observations, rewards, dones, infos = {}, {}, {}, {}
        return observations, rewards, dones, infos

    def reset(self):
        pass

    def render(self):
        pass

    def random_demo(self, render=True, episodes=1):
        pass


class Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.name = f'agent_{agent_id}'
        self.actions = [1, 2, 3, 4]
        self.x, self.y = -1, -1
