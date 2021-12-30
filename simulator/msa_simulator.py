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

    def __init__(self):
        agents = None
        num_agents = None
        possible_agents = None
        max_num_agents = None
        observation_spaces = None
        action_spaces = None

    def seed(self):
        pass

    def observation_space(self, agent):
        pass

    def action_space(self, agent):
        pass

    def step(self, actions):
        pass

    def reset(self):
        pass

    def render(self):
        pass

    def random_demo(self, render=True, episodes=1):
        pass
























