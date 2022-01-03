import math
import random

import numpy as np

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

    def __init__(self, num_agents, to_render=True, num_points_of_interest=10):
        self.agents = None
        self.num_agents = num_agents
        self.possible_agents = self.agents
        self.max_num_agents = num_agents
        self.observation_spaces = None
        self.action_spaces = None

        self.field = None
        self.num_points_of_interest = num_points_of_interest
        self.width = 50

        # RENDER
        self.to_render = to_render
        self.agent_size = self.width / 50
        if self.to_render:

            # self.fig, self.ax = plt.subplots(figsize=[6.5, 6.5])

            self.fig, self.ax_list = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
            self.ax = self.ax_list[0]
            self.ax2 = self.ax_list[1]

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
        # CLEAR
        self.field = []
        self.agents = []

        # CREATE FIELD
        for i_x in range(self.width):
            for i_y in range(self.width):
                pos = Position(pos_id=f'{i_x}{i_y}', x=i_x, y=i_y)
                self.field.append(pos)

        # CREATE AGENTS
        positions_for_agents = random.sample(self.field, self.num_agents)
        self.agents = [Agent(i, pos.x, pos.y) for i, pos in enumerate(positions_for_agents)]

        # CREATE POINTS OF INTEREST
        points_of_interest = random.sample(self.field, self.num_points_of_interest)
        for target in points_of_interest:
            for pos in self.field:
                dist = math.sqrt((target.x - pos.x) ** 2 + (target.y - pos.y) ** 2)
                if dist <= 1.0:
                    new_req = 1.0
                elif 1.0 < dist <= 10.0:
                    new_req = min(1.0, ((1 / dist) + pos.req))
                else:
                    new_req = pos.req
                pos.req = new_req

        observations = {}
        return observations

    def random_demo(self, render=True, episodes=1):
        pass

    def render(self):
        if self.to_render:
            # self.fig.cla()

            self.ax.clear()
            padding = 4
            self.ax.set_xlim([0 - padding, self.width + padding])
            self.ax.set_ylim([0 - padding, self.width + padding])

            # titles
            self.ax.set_title('MAS Simulation')
            # ax.set_title( f'Problem:({problem + 1}/{B_NUMBER_OF_PROBLEMS})   Iteration: ({big_iteration + 1}/{
            # B_ITERATIONS_IN_BIG_LOOPS})' f'\n{alg_name} ({alg_num + 1}/{len(ALGORITHMS_TO_CHECK)}) ' )
            # ax.set_xlabel(f'\nTime of the run: {time.strftime("%H:%M:%S", time.gmtime(time.time() - start))}')

            # POSITIONS
            self.ax.scatter(
                [pos_node.x for pos_node in self.field],
                [pos_node.y for pos_node in self.field],
                alpha=[pos_node.req for pos_node in self.field],
                color='g', marker="s", s=2
            )

            # POSITION ANNOTATIONS
            # for pos_node in self.field:
            #     self.ax.annotate(pos_node.name, (pos_node.x, pos_node.y), fontsize=5)

            # EDGES: edge lines on the graph
            # for pos_node in graph:
            #     x_edges_list, y_edges_list = [], []
            #     for nearby_node_name, nearby_node in pos_node.nearby_position_nodes.items():
            #         x_edges_list.extend([pos_node.pos[0], nearby_node.pos[0]])
            #         y_edges_list.extend([pos_node.pos[1], nearby_node.pos[1]])
            #     plt.plot(x_edges_list, y_edges_list, color='g', alpha=0.3)

            # ROBOTS
            for robot in self.agents:
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

            # TARGETS
            # for target in targets:
            #     rect = plt.Rectangle(target.pos_node.pos - (B_SIZE_TARGET_NODE / 2, B_SIZE_TARGET_NODE / 2),
            #                          B_SIZE_TARGET_NODE,
            #                          B_SIZE_TARGET_NODE, color='r', alpha=0.3)
            #     ax.add_patch(rect)
            #     ax.annotate(target.name, target.pos_node.pos, fontsize=5)

            # light up nodes upon the changes
            # if LIGHT_UP_THE_CHANGES:
            #     pass

            plt.pause(0.05)


class Agent:
    def __init__(self, agent_id, x=-1, y=-1):
        self.id = agent_id
        self.x, self.y = x, y
        self.name = f'agent_{agent_id}'
        self.actions = [0, 1, 2, 3, 4]
        self.sr = 2
        self.mr = 3


class Position:
    def __init__(self, pos_id, x, y, req=0):
        self.id = pos_id
        self.name = f'pos_{pos_id}'
        self.x, self.y = x, y
        self.req = req
