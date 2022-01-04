from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel
from algorithms.alg_dsa import AlgDSA


def main():
    for problem in range(PROBLEMS):

        for i_alg, algorithm in enumerate(algorithms_list):

            observations = env.reset()
            algorithm.reset(env.agents_list, env.get_field())

            for step in range(MAX_STEPS):
                # actions_dict = {agent: policy(observations[agent], agent) for agent in parallel_env.agents}
                # actions_dict = {agent.name: random.choice(agent.actions) for agent in env.agents_list}
                actions_dict = algorithm.iteration_calc(observations, env)
                new_observations, rewards, dones, infos = env.step(actions_dict)

                observations = new_observations

                # PLOT + RENDER
                env.render(er_hat=algorithm.search_map)
                print(f'\r~[INFO] problem: {problem + 1}/{PROBLEMS}, alg:{i_alg + 1}/{len(algorithms_list)}, '
                      f'step: {step + 1}/{MAX_STEPS}', end='')


if __name__ == '__main__':
    PROBLEMS = 10
    MAX_STEPS = 300
    N_AGENTS = 10
    algorithms_list = [AlgDSA()]
    env = MSASimulatorParallel(num_agents=N_AGENTS, to_render=True)
    main()























