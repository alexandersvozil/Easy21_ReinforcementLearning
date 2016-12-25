import numpy as np
import environment as easy21
import copy
import math
import random


class MonteCarlo:
    def __init__(self):
        self._max_dealer_points = 10
        self._max_player_points = 21
        self._num_actions = 2
        self._value_action_state = np.zeros(shape=(self._num_actions, self._max_dealer_points, self._max_player_points))
        self._counter = np.zeros(shape=(self._num_actions, self._max_dealer_points, self._max_player_points))
        self._policy = np.zeros(shape=(self._max_dealer_points, self._max_player_points), dtype="S5")
        self._policy[:] = 'hit'
        self._discount_factor = 1

    def monte_carlo_control(self):
        for x in range(15000):
            episode_history = self._generate_episode()
            self._update_from_episode(episode_history)
            epsilon = 100
            self._create_next_policy(epsilon)
        self._generate_greedy_policy()
        # print self._counter
        print  self._policy
        played = 0;
        won = 0;
        for x in range(1000):
            played += 1
            episode_history = self._generate_episode()
            if episode_history[len(episode_history) - 2] == 1:
                won += 1

        print "games won: ", won
        print "win percentage ", won / float(played)

    def _generate_episode(self):
        env = easy21.Environment()
        episode_history = []
        cur_state = env._current_state
        episode_history.append(copy.deepcopy(cur_state))

        while (cur_state['terminal'] == False):
            action = self._generate_action_on_state(cur_state)
            episode_history.append(action)

            cur_reward, next_state = env.step(action)

            episode_history.append(cur_reward)
            episode_history.append(copy.deepcopy(next_state))
        return episode_history

    def _generate_action_on_state(self, cur_state):
        dealer_points = cur_state['dealer'] - 1
        player_points = cur_state['player'] - 1
        action = self._policy[dealer_points, player_points]
        return action

    def _update_from_episode(self, episode_history):

        states = [x for x in episode_history if isinstance(x, dict)]
        actions = [x for x in episode_history if isinstance(x, str)]
        rewards = [x for x in episode_history if isinstance(x, int)]

        state_action = zip(states[:-1], actions)
        sa_rewards = zip(state_action, rewards)

        for (state, action) in state_action:
            return_x = self._calculate_return((state, action), sa_rewards)
            dealer = state['dealer'] - 1
            player = state['player'] - 1
            action_num = self._action_num_from_action_string(action)
            self._counter[action_num][dealer][player] += 1
            counter_sa = self._counter[action_num][dealer][player]
            self._value_action_state[action_num, dealer, player] += \
                (float(1) / counter_sa) * (return_x - self._value_action_state[action_num, dealer, player])

    def _action_num_from_action_string(self, action):
        action_num = 0 if action == 'hit' else 1
        return action_num

    def _action_string_from_action_num(self, action):
        action_str = 'hit' if action == 0 else 'stick'
        return action_str

    def _calculate_return(self, tuple_state_action, sa_rewards):
        result = 0
        since_first_occurrence_found = -1

        for ((state, action), reward) in sa_rewards:

            if self._checkEqualStateAction((state, action), tuple_state_action) and since_first_occurrence_found == -1:
                since_first_occurrence_found = 0

            if since_first_occurrence_found >= 0:
                result += reward * math.pow(self._discount_factor, since_first_occurrence_found)
                since_first_occurrence_found += 1

        return result

    def _checkEqualStateAction(self, state_action_tuple1, state_action_tuple2):
        state1 = state_action_tuple1[0]
        state2 = state_action_tuple2[0]

        dealer_p1 = state1['dealer']
        player_p1 = state1['player']

        dealer_p2 = state2['dealer']
        player_p2 = state2['player']

        if (dealer_p1 != dealer_p2):
            return False

        if (player_p1 != player_p2):
            return False

        action1 = state_action_tuple1[1]
        action2 = state_action_tuple2[1]

        if (action1 != action2):
            return False
        return True

    def _create_next_policy(self, epsilon_constant):
        self._policy = np.zeros(shape=([self._max_dealer_points, self._max_player_points]), dtype="S5")
        for dealer_p in range(0, 10):
            for player_p in range(0, 21):
                value_hit = self._value_action_state[0][dealer_p][player_p]
                value_stick = self._value_action_state[1][dealer_p][player_p]
                epsilon = float(epsilon_constant) / (
                epsilon_constant + self._counter[0, dealer_p, player_p] + self._counter[1, dealer_p, player_p])
                stick_prob = 1 - epsilon + epsilon / 2 if value_stick > value_hit else epsilon / 2
                # print stick_prob

                randRoll = random.random()

                if randRoll <= stick_prob:
                    action = 'stick'
                else:
                    action = 'hit'

                self._policy[dealer_p][player_p] = action

    def _generate_greedy_policy(self):
        for dealer_p in range(0, 10):
            for player_p in range(0, 21):
                value_hit = self._value_action_state[0][dealer_p][player_p]
                value_stick = self._value_action_state[1][dealer_p][player_p]
                greedy_action = max(value_stick, value_hit)
                if greedy_action == value_hit:
                    action = "hit"
                else:
                    action = "stick"
                self._policy[dealer_p][player_p] = action

if __name__ == "__main__":
    mc = MonteCarlo()
    mc.monte_carlo_control()