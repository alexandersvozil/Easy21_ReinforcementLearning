import os
import sys
import unittest2

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join("../src", testdir)))

from src import environment as env



class TestCode(unittest2.TestCase):
    TOOMUCH = 500

    def test_initial_state(self):
        test_env = env.Environment()

        self.assertEquals(test_env._current_move, 'player')
        self.assertEquals(test_env.is_terminal(), False)
        self.assertLessEqual(test_env._player_points, 10)
        self.assertGreaterEqual(test_env._player_points, 1)
        self.assertLessEqual(test_env._dealer_points, 10)
        self.assertGreaterEqual(test_env._dealer_points, 1)

    def test_observeEnvironment(self):
        test_env = env.Environment()
        test_env._dealer_points = 20
        test_env._player_points = 10

        (dealer,player) = test_env.observe_environment()

        self.assertEquals(dealer,20)
        self.assertEquals(player,10)

    def test_isTerminal(self):
        test_env = env.Environment()

        isTerminal = test_env.is_terminal

        self.assertTrue(isTerminal is False)

    def test_isTerminal(self):
        test_env = env.Environment()
        test_env._dealer_points = 22
        test_env._player_points = 10

        isTerminal  = test_env.is_terminal()

        self.assertTrue(isTerminal is True)

    def test_step_terminal(self):
        test_env = env.Environment()

        test_env._dealer_points = self.TOOMUCH
        test_env._current_move = 'player'
        test_env.step('stick')

        self.assertEquals(test_env.is_terminal(), True)

    def test_step_player_wins(self):
        test_env = env.Environment()

        test_env._dealer_points = self.TOOMUCH
        test_env._current_move = 'player'
        reward,state = test_env.step('stick')

        self.assertEquals(reward, 1)


    def test_step_dealer_wins(self):
        test_env = env.Environment()

        test_env._player_points = self.TOOMUCH
        test_env._current_move = 'player'
        reward,state = test_env.step('hit')

        self.assertEquals(test_env.is_terminal(), True)
        self.assertEquals(reward, -1)

    def test_step_reward_zero_notTerminal(self):
        test_env = env.Environment()

        test_env._player_points = 11
        test_env._current_move = 'player'
        reward,state = test_env.step('hit')

        self.assertEquals(test_env.is_terminal(), False)
        self.assertEquals(reward, 0)

    def test_dealer_strategy_hit(self):
        test_env = env.Environment()

        test_env._dealer_points = 1

        action = test_env._dealer_logic_simple()

        self.assertEquals(action, 'hit')

    def test_dealer_strategy_stick(self):
        test_env = env.Environment()

        test_env._dealer_points = 17

        action = test_env._dealer_logic_simple()

        self.assertEquals(action, 'stick')

    def test_current_state(self):
        test_env = env.Environment()

        reward,new_state = test_env.step('hit')

        self.assertEqual(new_state, test_env.observe_environment())

    def test_actionexception(self):

        test_env = env.Environment()

        state_before_invalid_action = test_env.observe_environment()
        test_env.step('INVALID_ACTION')
        state_after_invalid_action = test_env.observe_environment()

        self.assertEquals(state_before_invalid_action,state_after_invalid_action )
