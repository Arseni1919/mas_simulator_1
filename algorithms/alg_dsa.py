from GLOBALS import *
from simulator.msa_simulator import Agent, Position


class AlgDSA:
    def __init__(self):
        self.agents_list = None
        self.er_hat = None
        self.er_hat_dict = None

    def reset(self, agents_list, field_list):
        self.agents_list = agents_list
        self.er_hat = field_list
        self.er_hat_dict = {(pos.x, pos.y): pos for pos in self.er_hat}

    def iteration_calc(self, observations):
        actions_dict = {}
        for agent in self.agents_list:
            obs = observations[agent.name]
            for pos in obs:
                self.er_hat_dict[(pos[0], pos[1])].req = pos[2]

        actions_dict = {agent.name: random.choice(agent.actions) for agent in self.agents_list}
        return actions_dict


