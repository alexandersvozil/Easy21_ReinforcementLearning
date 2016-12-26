import numpy as np


class Environment:

    def __init__(self):
        self._current_move = 'player'
        self._dealer_points = self._generate_card()
        self._player_points = self._generate_card()
        self._both_stick = False

    def is_terminal(self):
        if self._dealer_points < 1 or self._dealer_points > 21:
            return True
        if self._player_points < 1 or self._player_points > 21:
            return True
        if self._both_stick:
            return True
        return False

    def step(self, action):
            if action != 'stick' and action != 'hit':
                print ('Action must be either "stick" or "hit"')
                return 0, self.observe_environment()

            if action == 'hit':
                reward = self._update_environment()
                return reward, self.observe_environment()

            if action == 'stick':
                if self._current_move == 'player':
                    self._current_move = 'dealer'
                    self._dealer_ai()
                    reward = self._conclude_game()
                    return reward, self.observe_environment()

                if self._current_move == 'dealer':
                    self._both_stick = True
                    return 0, self.observe_environment()

    def observe_environment(self):
        return self._dealer_points, self._player_points

    def _update_environment(self):
        number, color = self._draw()
        self._update_score(number, color)
        reward = self._calculate_reward()
        return reward

    def _draw(self):
        number = self._generate_card()
        color = self._generate_color()
        return number, color

    @staticmethod
    def _generate_card():
        return np.random.random_integers(1, 10)

    @staticmethod
    def _generate_color():
        success_red = np.random.randint(3)
        if success_red <= 0:
            color = "red"
        else:
            color = "black"
        return color

    def _update_score(self, number, color):
        if self._current_move == 'dealer':
            self._dealer_points = self._updated_points(self._dealer_points, number, color)
        else:
            self._player_points = self._updated_points(self._player_points, number, color)

    @staticmethod
    def _updated_points(current_points, number, color):
        if color == 'black':
            current_points += number
        else:
            current_points -= number
        return current_points

    def _calculate_reward(self):
        current_points = self._player_points if self._current_move == 'player' else self._dealer_points
        if current_points < 1 or current_points > 21:
            return -1
        else:
            return 0

    def _dealer_ai(self):
        while self.is_terminal() is False:
            action = self._dealer_logic_simple()
            reward, self._current_state = self.step(action)

    def _dealer_logic_simple(self):
        if self._dealer_points < 17:
            return 'hit'
        else:
            return 'stick'

    def _conclude_game(self):
        if self._dealer_points > 21 or self._dealer_points < 1:
            return 1

        if self._dealer_points > self._player_points:
            return -1
        elif self._dealer_points == self._player_points:
            return 0
        else:
            return 1
