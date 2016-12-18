import os
import sys
import unittest2
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join("../src", testdir)))

from src import environment as env



class TestCode(unittest2.TestCase):
    def test_squares_positive_numbers_correctly(self):
        self.assertEqual(2+2, 4)

    def test_initial_state(self):
        state = env.create_initial_state()
        self.assertEquals(state['turn'], 'Player')
        self.assertEquals(state['terminal'],False)
        self.assertLessEqual(state['Player'], 10)
        self.assertGreaterEqual(state['Player'], 1)
        self.assertLessEqual(state['Dealer'], 10)
        self.assertGreaterEqual(state['Dealer'], 1)

    def test_update_state(self):

        state = env.create_initial_state()

