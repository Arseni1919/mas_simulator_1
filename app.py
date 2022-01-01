import random

from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel


def main():
    print('Hellow World!')
    observations = env.reset()
    for step in range(MAX_CYCLES):
        # actions_dict = {agent: policy(observations[agent], agent) for agent in parallel_env.agents}
        actions_dict = {agent: random.choice(agent.actions) for agent in env.agents}
        observations, rewards, dones, infos = env.step(actions_dict)


if __name__ == '__main__':
    env = MSASimulatorParallel(num_agents=10)
    MAX_CYCLES = 500
    main()























