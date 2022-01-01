from GLOBALS import *
from simulator.msa_simulator import MSASimulatorParallel


def main():
    print('Hellow World!')
    for problem in range(PROBLEMS):

        observations = env.reset()

        for step in range(MAX_STEPS):
            # actions_dict = {agent: policy(observations[agent], agent) for agent in parallel_env.agents}
            actions_dict = {agent: random.choice(agent.actions) for agent in env.agents}
            observations, rewards, dones, infos = env.step(actions_dict)

            # PLOT + RENDER
            env.render()
            print(f'\r[INFO] problem: {problem}/{PROBLEMS}, step: {step}/{MAX_STEPS}', end='')


if __name__ == '__main__':
    PROBLEMS = 10
    MAX_STEPS = 20
    N_AGENTS = 10
    env = MSASimulatorParallel(num_agents=N_AGENTS, to_render=False)
    main()























