import numpy as np
import environment as easy21
import copy
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


class MonteCarlo:
    def __init__(self):
        self._value_action_state = np.zeros((2,10,21))
        self._counter = np.zeros((2,10,21))
        self._discount_factor = 1
        self._K = 200

    def monte_carlo_control(self):

        for x in range(10000):
            episode_history = self._generate_episode()
            self._update_from_episode(episode_history)

        self._generate_greedy_policy()
        #print self._counter
        #print self._policy
        played = 0
        won = 0
        for x in range(30000):
            played += 1
            env = easy21.Environment()
            cur_state = env.initial_state
            while cur_state['terminal'] is False:
                action =  self._policy[cur_state['dealer']-1,cur_state['player']-1]
                cur_reward, cur_state = env.step(action)
                if(cur_reward is 1):
                    won+=1
        print "games won: ", won
        print "win percentage ", won / float(played)

        Vm = np.amax(self._value_action_state,axis=0)
        x = np.arange(1,11)
        y = np.arange(1,22)
        xs,ys = np.meshgrid(x,y)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_wireframe(xs,ys,Vm.T, rstride=1, cstride=1)
        plt.show()

    def _generate_episode(self):
        env = easy21.Environment()
        episode_history = []
        cur_state = env._current_state
        episode_history.append(copy.deepcopy(cur_state))
        while cur_state['terminal'] is False:
            action = self._generate_action_on_state(cur_state)
            episode_history.append(action)
            action_num = self._action_num_from_action_string(action)
            self._counter[action_num,cur_state['dealer']-1,cur_state['player']-1] += 1

            cur_reward, cur_state = env.step(action)

            episode_history.append(cur_reward)
            episode_history.append(copy.deepcopy(cur_state))
        return episode_history

    def _generate_action_on_state(self, cur_state):
        dealer_points = cur_state['dealer'] - 1
        player_points = cur_state['player'] - 1
        value_sum = np.sum(self._counter[:,dealer_points,player_points])
        e = self._K / (self._K + value_sum)
        if np.random.uniform(0,1) > e:
            action = np.argmax(self._value_action_state[:,dealer_points,player_points])
            #print action, self._value_action_state[0,dealer_points,player_points], self._value_action_state[1,dealer_points,player_points]
        else:
            action = np.random.randint(0,2)
        return self._action_string_from_action_num(action)

    def _update_from_episode(self, episode_history):

        L = episode_history[:-1]
        it = iter(L)
        state_action_rewards = zip(it,it,it)#zip(states[:-1], actions ,rewards)

        Gt = 0
        for j, (state, action,reward) in enumerate(state_action_rewards):
            dealer = state['dealer'] - 1
            player = state['player'] - 1
            action_num = self._action_num_from_action_string(action)
            alpha = 1.0 / self._counter[action_num,dealer,player]
            Gt += math.pow(self._discount_factor,j) * reward
            self._value_action_state[action_num, dealer, player] += alpha * (Gt - self._value_action_state[action_num, dealer, player])

    @staticmethod
    def _action_num_from_action_string(action):
        action_num = 0 if action == 'hit' else 1
        return action_num

    @staticmethod
    def _action_string_from_action_num(action):
        action_str = 'hit' if action == 0 else 'stick'
        return action_str

    @staticmethod
    def check_equal_state_action(state_action_tuple1, state_action_tuple2):
        state1 = state_action_tuple1[0]
        state2 = state_action_tuple2[0]

        dealer_p1 = state1['dealer']
        player_p1 = state1['player']

        dealer_p2 = state2['dealer']
        player_p2 = state2['player']

        if dealer_p1 != dealer_p2:
            return False

        if player_p1 != player_p2:
            return False

        action1 = state_action_tuple1[1]
        action2 = state_action_tuple2[1]

        if action1 != action2:
            return False
        return True

    def _generate_greedy_policy(self):
        self._policy = np.zeros(shape=(10,21), dtype="S5")
        for dealer_p in range(0, 10):
            for player_p in range(0, 21):
                value_hit = self._value_action_state[0,dealer_p,player_p]
                value_stick = self._value_action_state[1,dealer_p,player_p]
                greedy_action = max(value_stick, value_hit)
                if greedy_action is value_hit:
                    action = "hit"
                else:
                    action = "stick"
                self._policy[dealer_p][player_p] = action

if __name__ == "__main__":
    mc = MonteCarlo()
    mc.monte_carlo_control()
