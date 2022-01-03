from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel
from algorithms.alg_dsa import Alg_DSA


def main():
    print('Hellow World!')
    for problem in range(PROBLEMS):

        for i_alg, algorithm in enumerate(algorithms_list):

            observations = env.reset()

            for step in range(MAX_STEPS):
                # actions_dict = {agent: policy(observations[agent], agent) for agent in parallel_env.agents}
                actions_dict = {agent.name: random.choice(agent.actions) for agent in env.agents_list}
                new_observations, rewards, dones, infos = env.step(actions_dict)

                observations = new_observations

                # PLOT + RENDER
                env.render()
                print(f'\r~[INFO] problem: {problem + 1}/{PROBLEMS}, alg:{i_alg + 1}/{len(algorithms_list)}, '
                      f'step: {step + 1}/{MAX_STEPS}', end='')


if __name__ == '__main__':
    PROBLEMS = 10
    MAX_STEPS = 3
    N_AGENTS = 10
    algorithms_list = [Alg_DSA()]
    env = MSASimulatorParallel(num_agents=N_AGENTS, to_render=True)
    main()























