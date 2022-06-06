import time

import numpy as np

from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel
from algorithms.alg_dsa import AlgDSA
from algorithms.alg_rand_1 import AlgRand1
from algorithms.alg_simple_cover import AlgSimpleCover
from metrics import Plotter, get_er_loss, get_objective, get_tags, get_collisions


def main():
    for problem in range(PROBLEMS):
        for i_alg, algorithm in enumerate(algorithms_list):
            obj_list = []
            collisions_list = []

            observations = env.reset()
            # algorithm.reset(env.agents_list, field_list=env.get_field())
            algorithm.reset(env.agents_list, field_list=env.field_list, targets=env.poi, target_radius=env.poi_radius,
                            ratio=problem/max(0, PROBLEMS - ALPHA_LAST))

            for step in range(MAX_STEPS):
                # actions_dict = {agent: policy(observations[agent], agent) for agent in parallel_env.agents}
                # actions_dict = {agent.name: random.choice(agent.actions) for agent in env.agents_list}
                actions_dict = algorithm.iteration_calc(observations, env)
                new_observations, rewards, dones, infos = env.step(actions_dict)

                observations = new_observations

                # RENDER
                # if problem > max(0, PROBLEMS - RENDER_LAST):
                #     env.render(second_graph_dict={'name': 'reward_field', 'nodes': algorithm.reward_field_to_plot},
                #                alg_name=algorithm.name)
                env.render(second_graph_dict={'name': 'reward_field', 'nodes': algorithm.reward_field_to_plot},
                           alg_name=algorithm.name)

                # METRICS
                plotter.update_metrics_and_neptune({
                    # 'er_loss': get_er_loss(er_real=env.field_list, er_hat=algorithm.er_hat_list),
                    # 'objective': get_objective(er_real=env.field_list, agents=env.agents_list),
                    # 'collisions': get_collisions(agents=env.agents_list)
                    'rf_dict': len(algorithm.rf_dict),
                    'alpha': algorithm.alpha,
                })
                obj_list.append(get_objective(er_real=env.field_list, agents=env.agents_list))
                collisions_list.append(get_collisions(agents=env.agents_list))

                # PROGRESS
                print(f'\r~[INFO] problem: {problem + 1}/{PROBLEMS}, alg:{i_alg + 1}/{len(algorithms_list)}, '
                      f'step: {step + 1}/{MAX_STEPS}, size of rf_dict: {len(algorithm.rf_dict)}, alpha: {algorithm.alpha} ', end='')

            plotter.update_metrics_and_neptune({
                f'obj_per_problem_{algorithm.name}': np.mean(obj_list),
                f'collisions_per_problem_{algorithm.name}': np.mean(collisions_list),
            })


if __name__ == '__main__':
    # time.sleep(5)

    PROBLEMS = 1000
    ALPHA_LAST = 100
    MAX_STEPS = 40
    N_AGENTS = 4
    SR = 2
    MR = 1
    CRED = 1
    targets = 5
    target_radius = 1
    width = 20
    # --- #
    RENDER_LAST = 1000
    # PLOT_NEPTUNE = True
    PLOT_NEPTUNE = False
    # --- #
    # algorithms_list = [AlgDSA()]
    # algorithms_list = [AlgRand1()]
    algorithms_list = [AlgSimpleCover(target_radius=target_radius)]
    env = MSASimulatorParallel(num_agents=N_AGENTS, to_render=True, width=width,
                               poi=targets, target_radius=target_radius,
                               agent_sr=SR, agent_mr=MR, agent_cred=CRED)
    # env.seed()
    plotter = Plotter(plot_neptune=PLOT_NEPTUNE, tags=get_tags(algorithms_list), name='check')

    main()
