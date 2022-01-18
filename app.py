import time

from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel
from algorithms.alg_dsa import AlgDSA
from algorithms.alg_rand_1 import AlgRand1
from algorithms.alg_simple_cover import AlgSimpleCover
from metrics import Plotter, get_er_loss, get_objective, get_tags


def main():
    for problem in range(PROBLEMS):

        for i_alg, algorithm in enumerate(algorithms_list):

            observations = env.reset()
            algorithm.reset(env.agents_list, env.get_field(), targets=env.poi)

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
    SR = 2
    MR = 2
    CRED = 0.5
    targets = 1
    target_radius = 2
    width = 10
    # algorithms_list = [AlgDSA()]
    # algorithms_list = [AlgRand1()]
    algorithms_list = [AlgSimpleCover()]
    env = MSASimulatorParallel(num_agents=N_AGENTS, to_render=True, width=width,
                               poi=targets, target_radius=target_radius,
                               agent_sr=SR, agent_mr=MR, agent_cred=CRED)
    # plotter = Plotter(plot_neptune=True, tags=get_tags(algorithms_list), name='check')
    plotter = Plotter(plot_neptune=False, tags=get_tags(algorithms_list), name='check')
    main()
