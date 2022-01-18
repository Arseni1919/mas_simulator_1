from abc import ABC

from GLOBALS import *
from functions import distance_points
from algorithms.alg_meta import AlgMeta


class AlgRand1(AlgMeta, ABC):
    def __init__(self):
        super().__init__()
        self.agents_list = None
        self.er_hat = None
        self.er_hat_dict = None
        self.name = 'Rand_1'

    def reset(self, agents_list, field_list):
        self.agents_list = agents_list
        self.er_hat = field_list
        self.er_hat_dict = {(pos.x, pos.y): pos for pos in self.er_hat}

    def iteration_calc(self, observations, env):
        for agent in self.agents_list:
            obs = observations[agent.name]
            for pos_tuple in obs:
                xy_tuple = (pos_tuple[0], pos_tuple[1])
                # ER
                self.er_hat_dict[xy_tuple].req = pos_tuple[2]

        actions_dict = {agent.name: random.choice(agent.actions) for agent in self.agents_list}
        return actions_dict

