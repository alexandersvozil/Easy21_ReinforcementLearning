import os
import sys
import unittest2

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join("../src", testdir)))

from src import environment as env



class TestCode(unittest2.TestCase):
    TOOMUCH = 500

    def test_squares_positive_numbers_correctly(self):
        self.assertEqual(2+2, 4)

    def test_initial_state(self):
        test_env = env.Environment()

        state = test_env._current_state

        self.assertEquals(state['turn'], 'player')
        self.assertEquals(state['terminal'],False)
        self.assertLessEqual(state['player'], 10)
        self.assertGreaterEqual(state['player'], 1)
        self.assertLessEqual(state['dealer'], 10)
        self.assertGreaterEqual(state['dealer'], 1)

    def test_update_state_terminal(self):
        test_env = env.Environment()

        test_env._current_state['player'] = self.TOOMUCH
        reward = test_env._updateEnvironment()

        self.assertEquals(test_env._current_state['terminal'], True)

    def test_step_terminal(self):
        test_env = env.Environment()

        test_env._current_state['dealer'] = self.TOOMUCH
        test_env._current_state['turn'] = 'player'
        reward,state = test_env.step('stick')

        self.assertEquals(state['terminal'], True)

    def test_step_player_wins(self):
        test_env = env.Environment()

        test_env._current_state['dealer'] = self.TOOMUCH
        test_env._current_state['turn'] = 'player'
        reward,state = test_env.step('stick')

        self.assertEquals(reward, 1)


    def test_step_dealer_wins(self):
        test_env = env.Environment()

        test_env._current_state['player'] = self.TOOMUCH
        test_env._current_state['turn'] = 'player'
        reward,state = test_env.step('hit')

        self.assertEquals(state['terminal'], True)
        self.assertEquals(reward, -1)

    def test_step_reward_zero_notTerminal(self):
        test_env = env.Environment()

        test_env._current_state['player'] = 11
        test_env._current_state['turn'] = 'player'
        reward,state = test_env.step('hit')

        self.assertEquals(state['terminal'], False)
        self.assertEquals(reward, 0)

    def test_dealer_strategy_hit(self):
        test_env = env.Environment()

        test_env._current_state['turn'] = 'dealer'
        test_env._current_state['dealer'] = 1

        action = test_env._dealer_logic_simple()

        self.assertEquals(action, 'hit')

    def test_dealer_strategy_stick(self):
        test_env = env.Environment()

        test_env._current_state['dealer'] = 17

        action = test_env._dealer_logic_simple()

        self.assertEquals(action, 'stick')

    def test_current_state(self):
        test_env = env.Environment()

        reward,new_state = test_env.step('hit')

        self.assertDictEqual(new_state, test_env._current_state)

