from GLOBALS import *
from functions import distance_points
from algorithms.alg_meta import AlgMeta


class AlgSimpleCover(AlgMeta):
    def __init__(self):
        super().__init__(name='SIMPLE_COVER')
        self.agents_list = None
        self.er_hat = None
        self.er_hat_dict = None
        self.target_list = None
        self.alpha = 0.777

    def reset(self, agents_list, field_list, *args, **kwargs):
        self.agents_list = agents_list
        self.er_hat = copy.deepcopy(field_list)
        self.er_hat_dict = {(pos.x, pos.y): pos for pos in self.er_hat}
        self.target_list = copy.deepcopy(kwargs['targets'])

    def iteration_calc(self, observations, env, *args, **kwargs):
        # GET REMAINED COVERAGE MAP
        # TODO

        # UPDATE THE RF
        # TODO

        # CHOOSE THE NEXT ACTION ACCORDING TO THE MAP AND THE RF
        # TODO

        actions_dict = {agent.name: random.choice(agent.actions) for agent in self.agents_list}
        return actions_dict
