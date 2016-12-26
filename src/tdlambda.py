import numpy as np
import environment
import montecarlo
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

class td_lambda:
    def __init__(self, episodes, iLambda = 0.4):
        self._values_state_action = np.zeros((10, 21, 2))
        self._discount_factor = 1
        self._counter = np.zeros((10, 21, 2))
        self._exploration_rate = 100
        self._lambda = iLambda
        self._mse = []
        self._episodes = episodes

    def learn_sarsa(self, Q_star = None):
        if Q_star is not None:
            Q_star = np.swapaxes(Q_star,0,1)
            Q_star = np.swapaxes(Q_star,1,2)
        for i in range(self._episodes):
            self._learn_episode()
            if i % 1000 is 0 and Q_star is not None:
                self._mse.append(np.sum(self._values_state_action-Q_star)**2)




    def _learn_episode(self):
        self._eligibility_trace = np.zeros((10, 21, 2))
        env = environment.Environment()
        current_state = env.observe_environment()
        action = self._epsilon_greedy(current_state)
        self._learn_for_each_step(env, current_state, action)


    def _epsilon_greedy(self, (dealer_points, player_points)):

       # print "dealer:  " + str(dealer_points)
       # print "player: " + str(player_points)
        value_sum = np.sum(self._counter[dealer_points - 1, player_points - 1, :])
        e = self._exploration_rate / (self._exploration_rate + value_sum)

        if np.random.uniform(0, 1) > e:
            action = np.argmax(self._values_state_action[dealer_points - 1, player_points - 1, :])
        else:
            action = np.random.randint(0, 2)
        return action

    def _learn_for_each_step(self, env, state, action):
        while not env.is_terminal():
            self._counter[state[0]-1, state[1]-1, action] += 1
            reward, next_state = env.step(env._action_string_from_action_num(action))
            if(env.is_terminal()):
                delta = reward - self._values_state_action[state[0]-1, state[1]-1, action]
                next_action = 0
            else:
                next_action = self._epsilon_greedy(next_state)
                delta = reward + self._discount_factor * self._values_state_action[
                    next_state[0]-1, next_state[1]-1, next_action] \
                        - self._values_state_action[state[0]-1, state[1]-1, action]

            self._eligibility_trace[state[0]-1, state[1]-1, action] += 1
            alpha = 1.0 / self._counter[state[0]-1, state[1]-1, action]
            self._values_state_action += (alpha * delta * self._eligibility_trace)
            self._eligibility_trace = self._discount_factor * self._lambda * self._eligibility_trace
            action = next_action
            state = next_state



    def plot_value_function(self):
        Vm = np.amax(self._values_state_action, axis=2)
        x = np.arange(1, 11)
        y = np.arange(1, 22)
        xs, ys = np.meshgrid(x, y)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_wireframe(xs, ys, Vm.T, rstride=1, cstride=1)
        plt.show()

def plot_MSE(mses,episodes):
    plt.figure()
    plt.xlabel("episode")
    plt.ylabel("MSE")
    plt.title("MSE TDLambda Q*")
    for j,mse in enumerate(mses):
        plt.plot(np.arange(0, episodes, 1000), mse, label = "lambda " + str(j))

    plt.legend(loc=0)
    plt.show()

if __name__ == "__main__":
    tdl = td_lambda(25000)
    tdl.learn_sarsa()
    tdl.plot_value_function()

    try:
        q_star = np.load('q_star.npy')
        print "Loaded q_star locally!"
    except IOError:
        print "need to calculate q_star first"
        q_star = montecarlo.monte_carlo_control(10**6)
        np.save('q_star', q_star)

    mses = []
    episodes = 100000
    for i in (0,1):
        tdl = td_lambda(episodes,iLambda=i)
        tdl.learn_sarsa(q_star)
        mses.append(tdl._mse)

    plot_MSE(mses,episodes)

