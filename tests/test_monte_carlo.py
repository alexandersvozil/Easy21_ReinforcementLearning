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

        self.assertEquals(np.shape(monte._counter), (2, 10, 21))
        self.assertEquals(np.shape(monte._value_action_state), (2, 10, 21))

    def test_generate_episode_List_notEmpty(self):
        monte = mc.MonteCarlo()

        action_list = monte._generate_episode()

        self.assertTrue(action_list)

    def test_generate_episode_checkList(self):
        monte = mc.MonteCarlo()

        action_list = monte._generate_episode()

        (state, action, reward) = action_list[0]
        self.assertIn(reward, [-1, 0, 1])
        self.assertGreaterEqual(state[0], 0)
        self.assertGreaterEqual(state[1], 0)
        self.assertTrue(action is 0 or action is 1)

    def test_generate_action_from_policy(self):
        monte = mc.MonteCarlo()

        state = (10, 10)

        action = monte._generate_action_on_state(state)
        self.assertTrue(action is 0 or action is 1)

    def test_update_from_episode(self):
        monte = mc.MonteCarlo()

        episode = monte._generate_episode()
        monte._update_from_episode(episode)

    def test_monteCarloEval(selfs):
        monte = mc.MonteCarlo()
        monte.monte_carlo_control(10000)
        monte.test_strategy(400)
