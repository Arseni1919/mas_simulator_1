from GLOBALS import *
from simulator.msa_simulator import Agent, Position
from functions import distance_points
from algorithms.alg_meta import AlgMeta


class AlgDSA(AlgMeta):
    def __init__(self):
        super().__init__()
        self.agents_list = None
        self.er_hat = None
        self.er_hat_dict = None
        self.search_map = None
        self.search_map_dict = None
        self.prev_er_hat_dict = None
        self.name = 'DSA_MST'

    def reset(self, agents_list, field_list):
        self.agents_list = agents_list
        self.er_hat = field_list
        self.er_hat_dict = {(pos.x, pos.y): pos for pos in self.er_hat}
        self.search_map = copy.deepcopy(self.er_hat)
        self.search_map_dict = {(pos.x, pos.y): pos for pos in self.search_map}
        self.prev_er_hat_dict = copy.deepcopy(self.er_hat_dict)

    def iteration_calc(self, observations, env):
        actions_dict = {}
        prev_er_hat_dict = self.prev_er_hat_dict
        visited_pos_dict = {}
        for agent in self.agents_list:
            obs = observations[agent.name]
            for pos_tuple in obs:
                xy_tuple = (pos_tuple[0], pos_tuple[1])
                # SM
                self.search_map_dict[xy_tuple].req = max(0, prev_er_hat_dict[xy_tuple].req - agent.cred)
                visited_pos_dict[xy_tuple] = self.search_map_dict[xy_tuple].req
                # ER
                self.er_hat_dict[xy_tuple].req = pos_tuple[2]

        # get next action
        for agent in self.agents_list:
            next_action = self.get_best_next_action(agent, env)
            if random.random() < 0.7:
                actions_dict[agent.name] = next_action
            else:
                actions_dict[agent.name] = random.choice(agent.actions)

        # update unvisited pos
        # z = 0.01
        # for pos in self.search_map:
        #     if (pos.x, pos.y) not in visited_pos_dict:
        #         pos.req = min(pos.req + z, prev_er_hat_dict[(pos.x, pos.y)].req)
        # actions_dict = {agent.name: random.choice(agent.actions) for agent in self.agents_list}
        return actions_dict

    def get_best_next_action(self, agent, env):
        max_val = 0
        next_action = 0
        for action in agent.actions:
            next_x, next_y = env.get_next_pos(agent, action)
            xy_sum = 0
            # for pos in self.er_hat:
            for pos in self.search_map:
                if distance_points(next_x, next_y, pos.x, pos.y) <= agent.sr:
                    xy_sum += pos.req
            if xy_sum > max_val:
                max_val = xy_sum
                next_action = action
        return next_action

