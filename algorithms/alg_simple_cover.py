import random

from GLOBALS import *
from functions import distance_points, distance_nodes
from algorithms.alg_meta import AlgMeta
from metrics import get_sum_jc


class AlgSimpleCover(AlgMeta):
    def __init__(self, target_radius):
        super().__init__(name='SIMPLE_COVER')
        self.agents_list = None
        self.er_hat_list = None
        self.er_hat_dict = None
        self.target_list = None
        self.target_radius = target_radius
        self.near_pos_dict = None
        self.reward_field_to_plot = None
        self.rf_dict = {}
        self.alpha = 0.9
        self.ratio = None

    def create_rel_dict(self):
        rel_dict = {}
        for i_x in range(0 - self.target_radius, 0 + self.target_radius + 1):
            for i_y in range(0 - self.target_radius, 0 + self.target_radius + 1):
                rel_dict[(i_x, i_y)] = 0
        return rel_dict

    def reset(self, agents_list, field_list, *args, **kwargs):
        self.agents_list = agents_list
        self.er_hat_list = copy.deepcopy(field_list)
        self.er_hat_dict = {(pos.x, pos.y): pos for pos in self.er_hat_list}
        self.target_list = copy.deepcopy(kwargs['targets'])
        self.ratio = min(0.95, kwargs['ratio'])
        self.alpha = self.ratio
        self.near_pos_dict = {}
        for target in self.target_list:
            near_pos_list = list(filter(lambda pos: (distance_nodes(target, pos) <= self.target_radius), self.er_hat_list))
            self.near_pos_dict[target.name] = near_pos_list

    def iteration_calc(self, observations, env, *args, **kwargs):
        # GET THE REMAINED COVERAGE MAP
        for pos in self.er_hat_list:
            pos.rem_req = max(0, pos.req - get_sum_jc(pos.x, pos.y, self.agents_list))
            pos.cov_req = min(pos.req, get_sum_jc(pos.x, pos.y, self.agents_list))

        # UPDATE THE RF
        for target in self.target_list:
            rel_dict = self.create_rel_dict()
            # rel_map_key = tuple(list(map(self.there_is_agent_method, self.rel_map_dict[target.name])))
            self.set_rel_dict(rel_dict, target, self.agents_list)
            rel_dict_key = self.get_rel_dict_key(rel_dict)
            if rel_dict_key not in self.rf_dict:
                if 2 in rel_dict.values():
                    self.rf_dict[rel_dict_key] = 0
                else:
                    self.rf_dict[rel_dict_key] = sum(list(map(lambda curr_pos: curr_pos.cov_req, self.near_pos_dict[target.name])))

        # CHOOSE THE NEXT ACTION ACCORDING TO THE MAP AND THE RF
        # we want to minimize the remained requirement or to maximize the covered requirement
        actions_dict = {}
        for agent in self.agents_list:
            other_agents = list(filter(lambda a: a.name != agent.name, self.agents_list))
            # - BUILD THE FIELD OF POSSIBLE COVERAGES
            rel_dict = self.create_rel_dict()
            reward_list = env.get_field(req=0)
            reward_dict = {(pos.x, pos.y): pos for pos in reward_list}
            for target in self.target_list:
                self.set_rel_dict(rel_dict, target, other_agents)
                for near_pos in self.near_pos_dict[target.name]:
                    self.update_agent_counter(rel_dict, target, near_pos, add=True)  # ADD AGENT TO CHOSEN POS
                    rel_dict_key = self.get_rel_dict_key(rel_dict)
                    if rel_dict_key in self.rf_dict:
                        reward = self.rf_dict[rel_dict_key]
                        reward_dict[(near_pos.x, near_pos.y)].req += reward
                    self.update_agent_counter(rel_dict, target, near_pos, add=False)  # REMOVE AGENT FROM CHOSEN POS

            # - CHOOSE SUBSET OF MAXIMUM-COVERAGE POSITIONS
            max_reward = max([pos.req for pos in reward_list])
            max_reward_pos_list = list(filter(lambda curr_pos: curr_pos.req == max_reward, reward_list))

            # - PEAK ONE
            pos_dir = random.choice(max_reward_pos_list)

            # - CALCULATE THE DISTANCE FROM EACH ACTION UNTIL THE CHOSEN POSITION
            best_action, best_dist = 0, env.width
            for action in agent.actions:
                new_pos_x, new_pos_y = env.get_next_pos(agent, action)
                dist = distance_points(new_pos_x, new_pos_y, pos_dir.x, pos_dir.y)
                if dist < best_dist:
                    best_action, best_dist = action, dist

            # - CHOOSE THE SHORTEST-DISTANCE ACTION WITH PROBABILITY OF ALPHA
            if random.random() < self.alpha:
                actions_dict[agent.name] = best_action
            else:
                actions_dict[agent.name] = random.choice(agent.actions)

            # FOR PLOT
            if agent.id == 0:

                max_value = max([pos.req for pos in reward_list])
                if max_value != 0:
                    for pos in reward_list:
                        pos.req = pos.req / max_value
                self.reward_field_to_plot = reward_list
        # actions_dict = {agent.name: random.choice(agent.actions) for agent in self.agents_list}
        return actions_dict

    @staticmethod
    def there_is_agent(cur_pos, agents_list):
        # map(self.there_is_agent, self.rel_map_dict[target.name])
        value = 0
        for agent in agents_list:
            if (agent.x, agent.y) == (cur_pos.x, cur_pos.y):
                value += 1
        return value

    def set_rel_dict(self, rel_dict, target, agent_list):
        for agent in agent_list:
            self.update_agent_counter(rel_dict, target, agent)

    @staticmethod
    def update_agent_counter(rel_dict, target, agent, add=True):
        rel_x = agent.x - target.x
        rel_y = agent.y - target.y
        if (rel_x, rel_y) in rel_dict:
            if add:
                rel_dict[(rel_x, rel_y)] += 1
            else:
                rel_dict[(rel_x, rel_y)] -= 1

    def get_rel_dict_key(self, rel_dict):
        rel_2dlist = []
        for indx_x, i_x in enumerate(range(0 - self.target_radius, 0 + self.target_radius + 1)):
            rel_2dlist.append([])
            for indx_y, i_y in enumerate(range(0 - self.target_radius, 0 + self.target_radius + 1)):
                rel_2dlist[indx_x].append(rel_dict[(i_x, i_y)])
        # key = np.array(rel_2dlist).tobytes()
        key = str(np.array(rel_2dlist))
        return key











