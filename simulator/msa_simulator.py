import math
import random

import numpy as np

from GLOBALS import *
from functions import distance_nodes
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

    def __init__(self, num_agents, to_render=True, num_points_of_interest=10):
        self.agents = None
        self.agents_list = None
        self.num_agents = num_agents
        self.possible_agents = self.agents_list
        self.max_num_agents = num_agents
        self.observation_spaces = None
        self.action_spaces = None

        self.field = None
        self.field_list = None
        self.num_points_of_interest = num_points_of_interest
        self.width = 50

        # RENDER
        self.to_render = to_render
        self.agent_size = self.width / 50
        self.rewards_sum_list = None
        if self.to_render:

            # self.fig, self.ax = plt.subplots(figsize=[6.5, 6.5])
            self.fig, (self.ax, self.ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
            # self.fig, (self.ax, self.ax2, self.ax3) = plt.subplots(nrows=1, ncols=3, figsize=(9, 3))

    def seed(self):
        SEED = 123
        # torch.manual_seed(SEED)
        np.random.seed(SEED)
        random.seed(SEED)
        # env.seed(SEED)

    def observation_space(self, agent):
        return

    def action_space(self, agent):
        return self.agents[agent].actions

    def get_next_pos(self, agent, action):
        new_pos_x, new_pos_y = agent.x, agent.y
        # if action == 1:  # UP
        #     new_pos_y = agent.y + 1
        # if action == 2:  # DOWN
        #     new_pos_y = agent.y - 1
        # if action == 3:  # LEFT
        #     new_pos_x = agent.x - 1
        # if action == 4:  # RIGHT
        #     new_pos_x = agent.x + 1
        if action == 1:  # UP
            new_pos_y = agent.y + 1
        if action == 2:  # RIGHT
            new_pos_x = agent.x + 1
            new_pos_y = agent.y + 1
        if action == 3:  # RIGHT
            new_pos_x = agent.x + 1
        if action == 4:  # RIGHT
            new_pos_x = agent.x + 1
            new_pos_y = agent.y - 1
        if action == 5:  # DOWN
            new_pos_y = agent.y - 1
        if action == 6:  # RIGHT
            new_pos_y = agent.y - 1
            new_pos_x = agent.x - 1
        if action == 7:  # LEFT
            new_pos_x = agent.x - 1
        if action == 8:  # RIGHT
            new_pos_x = agent.x - 1
            new_pos_y = agent.y + 1

        new_pos_x = min(self.width - 1, max(0, new_pos_x))
        new_pos_y = min(self.width - 1, max(0, new_pos_y))

        return new_pos_x, new_pos_y

    def step(self, actions: dict):
        for agent_name, action in actions.items():
            agent = self.agents[agent_name]
            new_pos_x, new_pos_y = self.get_next_pos(agent, action)
            agent.x = new_pos_x
            agent.y = new_pos_y

        observations = self._get_observations()
        rewards = self._get_rewards(observations)
        self.rewards_sum_list.append(sum(rewards.values()))
        dones, infos = {}, {}
        return observations, rewards, dones, infos

    def reset(self):
        # CLEAR
        self.field_list, self.agents_list = [], []
        self.field, self.agents = {}, {}
        self.rewards_sum_list = []

        # CREATE FIELD
        for i_x in range(self.width):
            for i_y in range(self.width):
                pos = Position(pos_id=f'{i_x}{i_y}', x=i_x, y=i_y)
                self.field_list.append(pos)
        self.field = {pos.name: pos for pos in self.field_list}

        # CREATE AGENTS
        positions_for_agents = random.sample(self.field_list, self.num_agents)
        self.agents_list = [Agent(i, pos.x, pos.y) for i, pos in enumerate(positions_for_agents)]
        self.agents = {agent.name: agent for agent in self.agents_list}

        # CREATE POINTS OF INTEREST
        points_of_interest = random.sample(self.field_list, self.num_points_of_interest)
        for target in points_of_interest:
            for pos in self.field_list:
                dist = distance_nodes(target, pos)
                if dist <= 1.0:
                    new_req = 1.0
                elif 1.0 < dist <= 10.0:
                    new_req = min(1.0, ((1 / dist) + pos.req))
                else:
                    new_req = pos.req
                pos.req = new_req

        # BUILD FIRST OBSERVATIONS
        return self._get_observations()

    def _get_observations(self):
        observations = {}
        for agent in self.agents_list:
            observations[agent.name] = []
            for pos in self.field_list:
                if distance_nodes(agent, pos) <= agent.sr:
                    observations[agent.name].append((pos.x, pos.y, pos.req))
        return observations

    @staticmethod
    def _get_rewards(observations):
        rewards = {}
        for agent_name, positions in observations.items():
            rewards[agent_name] = 0
            for pos in positions:
                rewards[agent_name] += pos[2]
        return rewards

    def random_demo(self, render=True, episodes=1):
        pass

    def render(self, er_hat=None):
        if self.to_render:
            # self.fig.cla()

            self.ax.clear()
            padding = 4
            self.ax.set_xlim([0 - padding, self.width + padding])
            self.ax.set_ylim([0 - padding, self.width + padding])

            # titles
            self.ax.set_title('MAS Simulation')

            # POSITIONS
            self.ax.scatter(
                [pos_node.x for pos_node in self.field_list],
                [pos_node.y for pos_node in self.field_list],
                alpha=[pos_node.req for pos_node in self.field_list],
                color='g', marker="s", s=2
            )

            # ROBOTS
            for robot in self.agents_list:
                # robot
                circle1 = plt.Circle((robot.x, robot.y), self.agent_size, color='b', alpha=0.3)
                self.ax.add_patch(circle1)
                self.ax.annotate(robot.name, (robot.x, robot.y), fontsize=5)

                # range of sr
                circle_sr = plt.Circle((robot.x, robot.y), robot.sr, color='y', alpha=0.15)
                self.ax.add_patch(circle_sr)

                # range of mr
                circle_mr = plt.Circle((robot.x, robot.y), robot.mr, color='tab:purple', alpha=0.15)
                self.ax.add_patch(circle_mr)

            if er_hat:
                self.ax2.clear()
                self.ax2.set_title('er_hat')
                self.ax2.scatter(
                    [pos_node.x for pos_node in er_hat],
                    [pos_node.y for pos_node in er_hat],
                    alpha=[pos_node.req for pos_node in er_hat],
                    color='darkred', marker="o", s=5
                )

            plt.pause(0.05)

    def get_field(self):
        field = []
        for pos in self.field_list:
            field.append(Position(pos.id, pos.x, pos.y, req=1))
        return field


class Agent:
    def __init__(self, agent_id, x=-1, y=-1, sr=5, mr=2, cred=0.5):
        self.id = agent_id
        self.x, self.y = x, y
        self.sr = sr
        self.mr = mr
        self.cred = cred
        self.name = f'agent_{agent_id}'
        # self.actions = [0, 1, 2, 3, 4]
        self.actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]


class Position:
    def __init__(self, pos_id, x, y, req=0):
        self.id = pos_id
        self.name = f'pos_{pos_id}'
        self.x, self.y = x, y
        self.req = req
