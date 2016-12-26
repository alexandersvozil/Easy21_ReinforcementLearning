import os
import sys
import unittest2
from src import tdlambda

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join("../src", testdir)))

class test_lambda(unittest2.TestCase):

    def test_init(self):
        tdl = tdlambda.td_lambda()
        self.assertEquals(tdl._values_state_action.shape, (10,21,2))

    def learn_sarsa(self):
        tdl = tdlambda.td_lambda()
        tdl.learn_sarsa(5000)

    def test_episode(self):
        tdl = tdlambda.td_lambda()
        tdl._learn_episode()

    def test_greedt(self):
        tdl = tdlambda.td_lambda()

        tdl._epsilon_greedy((9,1))


