import numpy as np

class ActionError(Exception):
    pass



class TurnError(Exception):
    pass

def create_initial_state():
    initial_state = {}
    initial_state['turn'] = 'Player'
    initial_state['terminal'] = False
    initial_state['Player'] = generate_number()
    initial_state['Dealer'] = generate_number()
    return initial_state



DEALERREWARD = 0

def step(state, action):

    try:

        if(action != 'stick' and action != 'hit'):
            raise ActionError('Action must be either "stick" or "hit"')

        if(action == 'stick'):
            if(state['turn']=='Player'):
                state['turn'] = 'Dealer'
                state = start_dealer_ai(state)
                reward = conclude_game(state)
                return reward,state

            elif(state['turn'] == 'Dealer'):
                state['terminal'] = True
                return DEALERREWARD,state
            else:
                raise TurnError('Undefined Turn')
        elif(action == 'hit'):
            number,color = draw()
            next_state = updateState(number,color,state)
            reward = calculate_reward(next_state)
            next_state = checkTerminal(reward,next_state)

            return reward,next_state
    except ActionError as detail:
        print 'ActionError:', detail

def draw():
   number = generate_number()
   color = generate_color()
   return number,color

def generate_number():
    return np.random.random_integers(1,10)

def generate_color():
    success_red  = np.random.binomial(1,1/3)
    if(success_red):
        color = "red"
    else:
        color = "black"
    return color

def calculate_reward(state):
    current_points = state['Player']

    turn = state['turn']
    if(turn == 'Dealer'):
        current_points = state['Dealer']

    if(current_points < 1 or current_points > 21):
        return -1
    else:
        return 0

def updateState(number, color, state):
    turn = state['turn']
    new_state = state
    if (color == 'black'):
        new_state[turn] += number
    else:
        new_state[turn] -= number
    return new_state

def checkTerminal(reward, next_state):
    if (reward < 0):
        next_state['Terminal'] = True
    return next_state

def start_dealer_ai(state):
    current_state = state
    while(current_state['terminal'] == False):
        if (state['Dealer'] < 17):
            reward, current_state = step(state,'hit')
        else:
            step(state,'stick')
    return current_state


def conclude_game(state):
    if state['Dealer'] > 21 or state['Dealer'] < 1:
        return 1

    if state['Dealer'] > state['Player']:
        return -1
    elif state['Dealer'] == state['Player']:
        return 0
    else:
        return 1
