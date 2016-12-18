import numpy as np

class ActionError(Exception):
    pass



class TurnError(Exception):
    pass

def create_initial_state():
    initial_state = {}
    initial_state['turn'] = 'player'
    initial_state['terminal'] = False
    initial_state['player'] = generate_number()
    initial_state['dealer'] = generate_number()
    return initial_state



DEALERREWARD = 0

def step(state, action):

    try:

        if(action != 'stick' and action != 'hit'):
            raise ActionError('Action must be either "stick" or "hit"')

        if(action == 'stick'):
            if(state['turn']=='player'):
                state['turn'] = 'dealer'
                state = start_dealer_ai(state)
                reward = conclude_game(state)
                return reward,state

            elif(state['turn'] == 'dealer'):
                state['terminal'] = True
                return DEALERREWARD,state

            else:
                raise TurnError('Undefined Turn')

        elif(action == 'hit'):
            reward,next_state = updateEnvironment(state)
            return reward,next_state

    except ActionError as detail:
        print 'ActionError:', detail
        return 0,state

def draw():
   number = generate_number()
   color = generate_color()
   return number,color

def generate_number():
    return np.random.random_integers(1,10)

def generate_color():
    success_red  = np.random.binomial(1, float(1)/float(3) )
    if(success_red==1):
        color = "red"
    else:
        color = "black"
    return color


def updateEnvironment(state):
    number,color = draw()
    updated_score_state = update_score(number,color,state)
    reward = calculate_reward(updated_score_state)
    next_state = checkTerminal(reward,updated_score_state)
    return reward,next_state

def update_score(number, color, state):
    turn = state['turn']
    new_state = state
    if (color == 'black'):
        new_state[turn] += number
    else:
        new_state[turn] -= number

    return new_state

def calculate_reward(state):
    turn = state['turn']
    current_points = state[turn]
    if(current_points < 1 or current_points > 21):
        return -1
    else:
        return 0

def checkTerminal(reward, next_state):
    if (reward < 0):
        next_state['terminal'] = True

    return next_state

def start_dealer_ai(state):
    current_state = state
    while(current_state['terminal'] == False):
        if (state['dealer'] < 17):
            reward, current_state = step(state,'hit')
        else:
            step(state,'stick')
    return current_state


def conclude_game(state):
    if state['dealer'] > 21 or state['dealer'] < 1:
        return 1

    if state['dealer'] > state['player']:
        return -1
    elif state['dealer'] == state['player']:
        return 0
    else:
        return 1
