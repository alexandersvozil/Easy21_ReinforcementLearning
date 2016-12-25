import numpy as np



class Environment:

    def __init__(self):
        self.DEALERREWARD = 0
        self._current_state = self._create_initial_state()

    def _create_initial_state(self):
        initial_state = {}
        initial_state['turn'] = 'player'
        initial_state['terminal'] = False
        initial_state['player'] = self._generate_number()
        initial_state['dealer'] = self._generate_number()
        return initial_state

    def step(self, action):
            if(action != 'stick' and action != 'hit'):
                print ('Action must be either "stick" or "hit"')
                return 0,self._current_state

            if(action == 'stick'):
                if(self._current_state['turn']== 'player'):
                    self._current_state['turn'] = 'dealer'
                    self._dealer_ai()
                    reward = self._conclude_game()
                    return reward,self._current_state

                if(self._current_state['turn'] == 'dealer'):
                    self._current_state['terminal'] = True
                    return self.DEALERREWARD,self._current_state

            if(action == 'hit'):
                reward = self._updateEnvironment()
                return reward,self._current_state

    def _draw(self):
       number = self._generate_number()
       color = self._generate_color()
       return number,color

    def _generate_number(self):
        return np.random.random_integers(1,10)

    def _generate_color(self):
        success_red  = np.random.binomial(1, float(1)/float(3) )
        if(success_red==1):
            color = "red"
        else:
            color = "black"
        return color


    def _updateEnvironment(self):

        number,color = self._draw()
        updated_score_state = self._update_score(number,color,self._current_state)
        reward = self._calculate_reward(updated_score_state)
        self._current_state = self._checkTerminal(reward,updated_score_state)
        return reward

    def _update_score(self,number, color, state):
        turn = state['turn']
        new_state = state
        if (color == 'black'):
            new_state[turn] += number
        else:
            new_state[turn] -= number

        return new_state

    def _calculate_reward(self,state):
        turn = state['turn']
        current_points = state[turn]
        if(current_points < 1 or current_points > 21):
            return -1
        else:
            return 0

    def _checkTerminal(self,reward, next_state):
        if (reward < 0):
            next_state['terminal'] = True

        return next_state

    def _dealer_ai(self):
        while(self._current_state['terminal'] == False):
            action = self._dealer_logic_simple()
            reward, self._current_state = self.step(action)

    def _dealer_logic_simple(self):
        if (self._current_state['dealer'] < 17):
            return 'hit'
        else:
            return 'stick'

    def _conclude_game(self):
        if self._current_state['dealer'] > 21 or self._current_state['dealer'] < 1:
            return 1

        if self._current_state['dealer'] > self._current_state['player']:
            return -1
        elif self._current_state['dealer'] == self._current_state['player']:
            return 0
        else:
            return 1
