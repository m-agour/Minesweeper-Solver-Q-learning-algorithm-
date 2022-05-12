import json
import sys
import random
from Sweeper import *
from libs.graph import *


def size_of(item):
    print(sys.getsizeof(item) / 1024 / 1024)


W = 3
H = 4
M = 2

LEARNING_RATE = 0.1
DISCOUNT = 0.5
EPISODES = 50_000

epsilon = 0.9999997
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
EPSILON_DECAY_VALUE = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)
AGG_STATS_EVERY = 500
SHOW_EVERY = 1000
# FRAME_TIME = 1.5
FRAME_TIME = 0
SAVE_MODEL_EVERY = 500


class Q:
    def __init__(self):
        self.area = W * H
        self.name = f"{W}x{H}_{M}"
        self.env = Sweeper(W, H, M)

        cell_states = M + 2
        states_no = cell_states ** self.area
        # number of mines + unknown value + empty (no neighbours)
        # try:
        #     with lzma.open(f'data/{self.name}_map_modified.pickle', 'rb') as f:
        #         self.encoded_states = pickle.load(f)
        # except:
        #     print('No encoder snapshot was found!')
        #     states_list = np.array(list(product(cell_states, repeat=self.area)))
        #     encoded_states_list = np.ravel_multi_index(tuple(states_list.T), np.ones(self.area, dtype='uint8') * 9)
        #     self.encoded_states = {s: i for i, s in enumerate(encoded_states_list)}
        #     print('saving')
        #     with lzma.open(f'data/{self.name}_map_modified.pickle', 'wb') as f:
        #         pickle.dump(self.encoded_states, f)

        try:
            self.Q_table = np.load(f'data/{self.name}_Q_table.npz')['q_table']
        except:
            self.Q_table = np.zeros((states_no, self.area), dtype='float16')
            np.savez_compressed(f'data/{self.name}_Q_table', q_table=self.Q_table)

    def train(self):
        global epsilon

        try:
            with open(f'data/{self.name}_stats.json', 'r') as sf:
                stats = json.load(sf)
                current_episode = stats['episode'][-1]
                epsilon = stats['epsilon'][-1]
        except:
            print('init stats!')
            stats = {
                'episode': [],
                'win_rate': [],
                'm_progress': [],
                'm_reward': [],
                'm_moves': [],
                'epsilon': [],
            }
            current_episode = 1
            epsilon = epsilon

        progress_list, ep_rewards, wins_list, ep_moves = [], [], [], []

        for episode in range(current_episode, EPISODES + 1):
            past_n_wins = self.env.wins
            episode_reward = 0

            self.env.reset()
            done = False
            evaluate = False
            if episode % SHOW_EVERY == 0:
                self.env.display(FRAME_TIME, f'ep{episode}_0', episode)
                evaluate = True
                i = 0

            while not done:
                # state = self.get_state_Q_index(self.env.get_state())
                state = self.env.get_encoded_state()

                if random.uniform(0, 1) > epsilon or evaluate:
                    action = np.argmax(self.Q_table[state, :])
                else:
                    action = random.choice(self.env.get_actions())
                new_state, reward, done = self.env.reveal(action)
                episode_reward += reward

                if episode % SHOW_EVERY == 0:
                    i += 1
                    self.env.display(FRAME_TIME, f"ep{episode}_{str(i).zfill(9)}", episode)

                if not done:
                    max_future_q = np.max(self.Q_table[new_state])
                    current_q = self.Q_table[state][action]
                    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                    self.Q_table[state][action] = new_q
                else:
                    self.Q_table[state][action] = reward

            progress_list.append(self.env.progress)
            ep_rewards.append(episode_reward)
            if self.env.wins > past_n_wins:
                wins_list.append(1)
                ep_moves.append(self.env.moves)
            else:
                wins_list.append(0)

            if not episode % AGG_STATS_EVERY:
                med_progress = round(np.median(progress_list), 7)
                win_rate = round(np.sum(wins_list) / AGG_STATS_EVERY, 2)
                med_reward = round(np.median(ep_rewards), 2)
                med_moves = round(np.median(ep_moves), 2)
                progress_list, ep_rewards, wins_list, ep_moves = [], [], [], []

                print(
                    f'Episode: {episode}, Median progress: {med_progress}, Median reward: {med_reward}, Win rate : {win_rate}, Epsilon: {epsilon}')

                stats['episode'].append(episode)
                stats['win_rate'].append(win_rate)
                stats['m_progress'].append(med_progress)
                stats['m_reward'].append(med_reward)
                stats['m_moves'].append(med_moves)
                stats['epsilon'].append(epsilon)

                with open(f'data/{self.name}_stats.json', 'w') as sf:
                    json.dump(stats, sf)

            if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
                epsilon -= EPSILON_DECAY_VALUE

            if not episode % SAVE_MODEL_EVERY:
                np.savez_compressed(f'data/{self.name}_Q_table', q_table=self.Q_table)
                graph_stats(stats, self.name)
                print('saved Q_table!')

    def play(self):
        while 1:
            self.env.reset()
            done = False
            self.env.display(1.5)
            while not done:
                state = self.env.get_encoded_state()
                action = np.argmax(self.Q_table[state, :])
                done = self.env.reveal(action)[-1]
                self.env.display(1.5)


if __name__ == '__main__':
    x = Q()
    x.train()
    # x.play()

# def get_state_Q_index(self, state):
#     return self.encoded_states[np.ravel_multi_index(state, np.ones(self.area, dtype='uint8') * 9)]
