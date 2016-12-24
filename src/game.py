import environment as env

game_env = env.Environment()
cur_state = game_env._current_state

end_reward = -1
while (cur_state['terminal'] == False):
    print cur_state
    action = raw_input()
    end_reward,cur_state = game_env.step(action)


print "REWARD: " + str(end_reward) +  " STATE: "  + str(cur_state)
