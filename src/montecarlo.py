import numpy as np
import environment as easy21
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


class MonteCarlo:
    def __init__(self):
        self._value_action_state = np.zeros(shape=(2, 10, 21))
        self._counter = np.zeros(shape=(2, 10, 21))
        self._discount_factor = 1
        self._exploration_rate = 200

    def monte_carlo_control(self, iterations):
        for x in range(iterations):
            episode_history = self._generate_episode()
            self._update_from_episode(episode_history)

    def _generate_episode(self):
        env = easy21.Environment()
        episode_history = []
        cur_state = (dealer_p, player_p) = env.observe_environment()

        while env.is_terminal() is False:
            action = self._generate_action_on_state(cur_state)
            self._counter[action, dealer_p - 1, player_p - 1] += 1
            cur_reward, next_state = env.step(self._action_string_from_action_num(action))
            episode_history.append((cur_state, action, cur_reward))
            cur_state = (dealer_p, player_p) = next_state
        return episode_history

    def _generate_action_on_state(self, (dealer_points, player_points)):
        value_sum = np.sum(self._counter[:, dealer_points - 1, player_points - 1])
        e = self._exploration_rate / (self._exploration_rate + value_sum)

        if np.random.uniform(0, 1) > e:
            action = np.argmax(self._value_action_state[:, dealer_points - 1, player_points - 1])
        else:
            action = np.random.randint(0, 2)

        return action

    def _update_from_episode(self, episode_history):
        current_return = 0
        for j, ((dealer_p, player_p), action, reward) in enumerate(reversed(episode_history)):
            alpha = 1.0 / self._counter[action, dealer_p - 1, player_p - 1]
            current_return += math.pow(self._discount_factor, j) * reward
            self._value_action_state[action, dealer_p - 1, player_p - 1] += \
                 alpha * (current_return - self._value_action_state[action, dealer_p - 1, player_p - 1])

    @staticmethod
    def _action_num_from_action_string(action):
        action_num = 0 if action == 'hit' else 1
        return action_num

    @staticmethod
    def _action_string_from_action_num(action):
        action_str = 'hit' if action == 0 else 'stick'
        return action_str

    def _generate_greedy_policy(self):
        self._policy = np.zeros(shape=(10, 21), dtype="S5")
        for dealer_p in range(0, 10):
            for player_p in range(0, 21):
                value_hit = self._value_action_state[0, dealer_p, player_p]
                value_stick = self._value_action_state[1, dealer_p, player_p]
                greedy_action = max(value_stick, value_hit)
                if greedy_action is value_hit:
                    action = "hit"
                else:
                    action = "stick"
                self._policy[dealer_p][player_p] = action

    def test_strategy(self, test_iterations):
        played = 0
        won = 0
        self._generate_greedy_policy()
        for x in range(test_iterations):
            played += 1
            env = easy21.Environment()
            (dealer_p, player_p) = env.observe_environment()
            while env.is_terminal() is False:
                action = self._policy[dealer_p - 1, player_p - 1]
                cur_reward, (dealer_p, player_p) = env.step(action)
                if cur_reward is 1:
                    won += 1
        print "games won: ", won
        print "win percentage ", won / float(played)

    def plot_value_function(self):
        Vm = np.amax(self._value_action_state, axis=0)
        x = np.arange(1, 11)
        y = np.arange(1, 22)
        xs, ys = np.meshgrid(x, y)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_wireframe(xs, ys, Vm.T, rstride=1, cstride=1)
        plt.show()


if __name__ == "__main__":
    mc = MonteCarlo()
    mc.monte_carlo_control(50000)
    mc.test_strategy(4000)
    mc.plot_value_function()
