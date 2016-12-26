import environment as env

game_env = env.Environment()
cur_state = game_env.observe_environment()
end_reward = -1
while not game_env.is_terminal():
    print "Your Points: " + str(cur_state[1]) + "\n Dealer Points " + str(cur_state[0])
    action = raw_input()
    current_reward, cur_state = game_env.step(action)

    if game_env.is_terminal():
        end_reward = current_reward
else:
    if end_reward is 1:
        print "You win!"
    elif end_reward is 0:
        print "Draw!"
    else:
        print "You lost!"
    print "Your Points: " + str(cur_state[1]) + "\nDealer Points " + str(cur_state[0])
