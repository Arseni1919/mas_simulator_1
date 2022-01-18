from GLOBALS import *
from functions import distance_points, distance_nodes
from algorithms.alg_meta import AlgMeta
from metrics import get_sum_jc


class AlgSimpleCover(AlgMeta):
    def __init__(self):
        super().__init__(name='SIMPLE_COVER')
        self.agents_list = None
        self.er_hat_list = None
        self.er_hat_dict = None
        self.target_list = None
        self.target_radius = None
        self.rel_map_dict = None
        self.rel_map_key_dict = None
        self.rf_dict = {}
        self.alpha = 0.777

    def reset(self, agents_list, field_list, *args, **kwargs):
        self.agents_list = agents_list
        self.er_hat_list = copy.deepcopy(field_list)
        self.er_hat_dict = {(pos.x, pos.y): pos for pos in self.er_hat_list}
        self.target_list = copy.deepcopy(kwargs['targets'])
        self.target_radius = kwargs['target_radius']
        self.rel_map_dict = {}
        self.rel_map_key_dict = {}
        for target in self.target_list:
            rel_map = list(filter(lambda pos: (distance_nodes(target, pos) <= self.target_radius), self.er_hat_list))
            self.rel_map_dict[target.name] = rel_map
            self.rel_map_key_dict[target.name] = []

    def iteration_calc(self, observations, env, *args, **kwargs):
        # GET THE REMAINED COVERAGE MAP
        for pos in self.er_hat_list:
            pos.rem_req = max(0, pos.req - get_sum_jc(pos.x, pos.y, self.agents_list))
            pos.cov_req = min(pos.req, get_sum_jc(pos.x, pos.y, self.agents_list))

        # UPDATE THE RF
        for target in self.target_list:
            rel_map_key = tuple(list(map(self.there_is_agent, self.rel_map_dict[target.name])))
            self.rel_map_key_dict[target.name] = rel_map_key

            if rel_map_key not in self.rf_dict:
                self.rf_dict[rel_map_key] = sum(list(map(lambda curr_pos: curr_pos.cov_req, self.rel_map_dict[target.name])))
                print(f'k: {rel_map_key}, v: {self.rf_dict[rel_map_key]}')  # self.rf_dict[rel_map_key] = sum(list(map(lambda curr_pos: curr_pos.cov_req, self.rel_map_dict[target.name])))

        # CHOOSE THE NEXT ACTION ACCORDING TO THE MAP AND THE RF
        # we want to minimize the remained requirement or to maximize the covered requirement
        actions_dict = {}
        for agent in self.agents_list:

            # - BUILD THE FIELD OF POSSIBLE COVERAGES
            clean_field = env.get_field(req=0)
            for target in self.target_list:
                rel_map_key = self.rel_map_key_dict[target.name]

            # - CHOOSE SUBSET OF MAXIMUM-COVERAGE POSITIONS
            # TODO

            # - PEAK ONE
            # TODO

            # - CALCULATE THE DISTANCE FROM EACH ACTION UNTIL THE CHOSEN POSITION
            # TODO

            # - CHOOSE THE SHORTEST-DISTANCE ACTION WITH PROBABILITY OF ALPHA
            # TODO
            actions_dict[agent.name] = random.choice(agent.actions)

        # actions_dict = {agent.name: random.choice(agent.actions) for agent in self.agents_list}
        return actions_dict

    def there_is_agent(self, cur_pos):
        # map(self.there_is_agent, self.rel_map_dict[target.name])
        value = 0
        for agent in self.agents_list:
            if (agent.x, agent.y) == (cur_pos.x, cur_pos.y):
                value += 1
        return value

