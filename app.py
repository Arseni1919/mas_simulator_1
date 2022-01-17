import time

from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel
from algorithms.alg_dsa import AlgDSA
from algorithms.alg_rand_1 import AlgRand1
from metrics import Plotter, get_er_loss, get_objective, get_tags


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

                # RENDER
                env.render(er_hat=algorithm.er_hat, alg_name=algorithm.name)
                # env.render(er_hat=algorithm.search_map)

                # METRICS
                plotter.update_metrics_and_neptune({
                    'er_loss': get_er_loss(er_real=env.field_list, er_hat=algorithm.er_hat),
                    'objective': get_objective(er_real=env.field_list, agents=env.agents_list),
                })

                # PROGRESS
                print(f'\r~[INFO] problem: {problem + 1}/{PROBLEMS}, alg:{i_alg + 1}/{len(algorithms_list)}, '
                      f'step: {step + 1}/{MAX_STEPS} ', end='')


if __name__ == '__main__':
    # time.sleep(5)
    PROBLEMS = 100
    MAX_STEPS = 300
    N_AGENTS = 2
    num_points_of_interest = 1
    width = 30
    # algorithms_list = [AlgDSA()]
    algorithms_list = [AlgRand1()]
    env = MSASimulatorParallel(num_agents=N_AGENTS, to_render=True, poi=num_points_of_interest, width=width)
    # plotter = Plotter(plot_neptune=True, tags=get_tags(algorithms_list), name='check')
    plotter = Plotter(plot_neptune=False, tags=get_tags(algorithms_list), name='check')
    main()























