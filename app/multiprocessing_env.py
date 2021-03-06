# ================================================================
#
#   File name   : multiprocessing_env.py
#   Author      : PyLessons
#   Created date: 2021-02-25
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/RL-Bitcoin-trading-bot
#   Description : functions to train/test multiple custom BTC trading environments
#
# ================================================================
import numpy as np
import json
import time

from config import *
from tensorflow.keras.optimizers import Adam
from multiprocessing import Process, Pipe
from datetime import datetime
from collections import deque


class Environment(Process):
    def __init__(self, env_idx, child_conn, env, training_batch_size, visualize):
        super(Environment, self).__init__()
        self.env = env
        self.env_idx = env_idx
        self.child_conn = child_conn
        self.training_batch_size = training_batch_size
        self.visualize = visualize

    def run(self):
        super(Environment, self).run()
        state = self.env.reset(env_steps_size=self.training_batch_size)
        self.child_conn.send(state)
        while True:
            reset, net_worth, episode_orders = 0, 0, 0
            action = self.child_conn.recv()
            if self.env_idx == 0:
                self.env.render(self.visualize)
            state, reward, done = self.env.step(action)

            if done or self.env.current_step == self.env.end_step:
                net_worth = self.env.net_worth
                episode_orders = self.env.episode_orders
                state = self.env.reset(env_steps_size=self.training_batch_size)
                reset = 1

            self.child_conn.send(
                [state, reward, done, reset, net_worth, episode_orders])


def train_multiprocessing(CustomEnv, agent, train_df, train_df_nomalized, num_worker=4, training_batch_size=500, visualize=False, EPISODES=10000, indicators=""):
    works, parent_conns, child_conns = [], [], []
    episode = 0
    total_average = deque(maxlen=100)  # save recent 100 episodes net worth
    best_average = 0  # used to track best average net worth

    for idx in range(num_worker):
        print("###### Starting Worker #"+str(idx))
        parent_conn, child_conn = Pipe()
        env = CustomEnv(train_df, train_df_nomalized,
                        lookback_window_size=agent.lookback_window_size)
        work = Environment(idx, child_conn, env,
                           training_batch_size, visualize)
        work.start()
        works.append(work)
        parent_conns.append(parent_conn)
        child_conns.append(child_conn)

    # create TensorBoard writer
    agent.create_writer(env.initial_balance,
                        env.normalize_value, EPISODES, training_batch_size, indicators)

    states = [[] for _ in range(num_worker)]
    next_states = [[] for _ in range(num_worker)]
    actions = [[] for _ in range(num_worker)]
    rewards = [[] for _ in range(num_worker)]
    dones = [[] for _ in range(num_worker)]
    predictions = [[] for _ in range(num_worker)]

    state = [0 for _ in range(num_worker)]
    for worker_id, parent_conn in enumerate(parent_conns):
        state[worker_id] = parent_conn.recv()

    starting_time = time.time()
    while episode < EPISODES:
        predictions_list = agent.Actor.actor_predict(
            np.reshape(state, [num_worker]+[_ for _ in state[0].shape]))
        actions_list = [np.random.choice(
            agent.action_space, p=i) for i in predictions_list]

        for worker_id, parent_conn in enumerate(parent_conns):
            parent_conn.send(actions_list[worker_id])
            action_onehot = np.zeros(agent.action_space.shape[0])
            action_onehot[actions_list[worker_id]] = 1
            actions[worker_id].append(action_onehot)
            predictions[worker_id].append(predictions_list[worker_id])

        for worker_id, parent_conn in enumerate(parent_conns):
            next_state, reward, done, reset, net_worth, episode_orders = parent_conn.recv()
            states[worker_id].append(np.expand_dims(state[worker_id], axis=0))
            next_states[worker_id].append(np.expand_dims(next_state, axis=0))
            rewards[worker_id].append(reward)
            dones[worker_id].append(done)
            state[worker_id] = next_state

            if reset:
                episode += 1
                a_loss, c_loss = agent.replay(states[worker_id], actions[worker_id], rewards[worker_id],
                                              predictions[worker_id], dones[worker_id], next_states[worker_id])
                total_average.append(net_worth)
                average = np.average(total_average)

                agent.writer.add_scalar(
                    'Data/average net_worth', average, episode)
                agent.writer.add_scalar(
                    'Data/episode_orders', episode_orders, episode)

                ts = time.gmtime()
                print(time.strftime("%x %X", ts) + " - Episode: {:<5} Worker: {:<2} Net Worth: {:<7.2f} Average: {:<7.2f} N_Orders: {}".format(
                    episode, worker_id, net_worth, average, episode_orders))
                if episode > len(total_average):
                    if best_average < average:
                        best_average = average
                        print("Saving model")
                        agent.save(score="{:.2f}".format(best_average), args=[
                                   episode, average, episode_orders, a_loss, c_loss])
                    agent.save()

                states[worker_id] = []
                next_states[worker_id] = []
                actions[worker_id] = []
                rewards[worker_id] = []
                dones[worker_id] = []
                predictions[worker_id] = []

    # terminating processes after while loop
    with open(agent.log_name+"/Parameters.json", "r") as json_file:
        params = json.load(json_file)
    with open(agent.log_name+"/Parameters.json", "w") as write_file:
        params["duration"] = (time.time() - starting_time)/60
        json.dump(params, write_file, indent=4)

    works.append(work)
    for work in works:
        work.terminate()
        print('TERMINATED:', work)
        work.join()


def test_multiprocessing(CustomEnv, CustomAgent, test_df, test_df_nomalized, num_worker=4, visualize=False, test_episodes=1000, folder="", name="", comment="", initial_balance=INITIAL_CAPITAL, Show_reward=False, Show_indicators=False):
    with open(folder+"/Parameters.json", "r") as json_file:
        params = json.load(json_file)
    if name != "":
        params["Actor name"] = "models/" + f"{name}_Actor.h5"
        params["Critic name"] = "models/" + f"{name}_Critic.h5"
    name = params["Actor name"][:-9]

    agent = CustomAgent(lookback_window_size=params["lookback window size"],
                        optimizer=Adam, depth=params["depth"], model=params["model"])

    agent.load(folder, name)
    works, parent_conns, child_conns = [], [], []
    average_net_worth = 0
    average_orders = 0
    no_profit_episodes = 0
    episode = 0

    for idx in range(num_worker):
        parent_conn, child_conn = Pipe()
        # env = CustomEnv(test_df, initial_balance=initial_balance, lookback_window_size=agent.lookback_window_size)
        env = CustomEnv(df=test_df, df_normalized=test_df_nomalized,
                        initial_balance=initial_balance, lookback_window_size=agent.lookback_window_size)
        work = Environment(idx, child_conn, env,
                           training_batch_size=0, visualize=visualize)
        work.start()
        works.append(work)
        parent_conns.append(parent_conn)
        child_conns.append(child_conn)

    state = [0 for _ in range(num_worker)]
    for worker_id, parent_conn in enumerate(parent_conns):
        state[worker_id] = parent_conn.recv()

    print("Name: "+name+" starting...")
    while episode < test_episodes:
        predictions_list = agent.Actor.actor_predict(
            np.reshape(state, [num_worker]+[_ for _ in state[0].shape]))
        actions_list = [np.random.choice(
            agent.action_space, p=i) for i in predictions_list]

        for worker_id, parent_conn in enumerate(parent_conns):
            parent_conn.send(actions_list[worker_id])

        for worker_id, parent_conn in enumerate(parent_conns):
            next_state, reward, done, reset, net_worth, episode_orders = parent_conn.recv()
            state[worker_id] = next_state

            if reset:
                episode += 1
                # print(episode, net_worth, episode_orders)
                average_net_worth += net_worth
                average_orders += episode_orders
                if net_worth < initial_balance:
                    # calculate episode count where we had negative profit through episode
                    no_profit_episodes += 1
                print("episode: {:<5} worker: {:<2} net worth: {:<7.2f} average_net_worth: {:<7.2f} orders: {}".format(
                    episode, worker_id, net_worth, average_net_worth/episode, episode_orders))
                if episode == test_episodes:
                    break

    print("No profit episodes: {}".format(no_profit_episodes))
    # save test results to test_results.txt file
    with open(folder+"/test_results.txt", "a+") as results:
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        results.write(f'{current_date}, {name}, {test_episodes}')
        results.write(
            f', {average_net_worth/(episode+1)}, {average_orders/test_episodes}')
        results.write(f', {no_profit_episodes}, {agent.model}, {comment}\n')

    # terminating processes after while loop
    works.append(work)
    for work in works:
        work.terminate()
        print('TERMINATED:', work)
        work.join()
