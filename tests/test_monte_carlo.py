import unittest2
import os
import sys
import numpy as np
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join("../src", testdir)))

from src import montecarlo as mc

class MonteCarloTest(unittest2.TestCase):

    def test_q_init(self):
        monte = mc.MonteCarlo()

        self.assertEquals(np.shape(monte._counter), (2,10,21))
        self.assertEquals(np.shape(monte._value_action_state),(2,10,21))


    def test_generate_episode_List_notEmpty(self):
        monte = mc.MonteCarlo()

        action_list = monte._generate_episode()

        self.assertTrue(action_list)

    def test_generate_episode_checkList(self):
        monte = mc.MonteCarlo()

        action_list = monte._generate_episode()

        state1 = action_list[0]
        self.assertEquals(state1['terminal'], False)

    def test_generate_action_from_policy(self):
        monte = mc.MonteCarlo()
        state = {'player': 10, 'dealer': 10}
        monte._policy = np.zeros(shape=([10,21]), dtype="S5")
        monte._policy[:] = 'hit'

        action = monte._generate_action_on_state(state)



    def test_update_from_episode(self):
        monte = mc.MonteCarlo()

        episode = monte._generate_episode()
        monte._update_from_episode(episode)


    def test_checkEqualsStatesFalse(self):
        monte = mc.MonteCarlo()

        sa_tuple = ({'terminal': False, 'turn': 'player', 'dealer': 8, 'player': 6}, 'hit')
        sa_tuple2 = ({'terminal': False, 'turn': 'player', 'dealer': 8, 'player': 7}, 'hit')

        self.assertFalse(monte.check_equal_state_action(sa_tuple, sa_tuple2))

    def test_checkEqualsStatesTrue(self):
        monte = mc.MonteCarlo()

        sa_tuple = ({'terminal': False, 'turn': 'player', 'dealer': 8, 'player': 6}, 'hit')
        sa_tuple2 = ({'terminal': False, 'turn': 'player', 'dealer': 8, 'player': 6}, 'hit')

        self.assertTrue(monte.check_equal_state_action(sa_tuple, sa_tuple2))


    def test_greedy_policy(self):
        monte = mc.MonteCarlo()


    def test_monteCarlo(self):
        monte = mc.MonteCarlo()
        monte.monte_carlo_control()


