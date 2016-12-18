import environment as envi

cur_state = envi.create_initial_state()
end_reward = -1
while (cur_state['terminal'] == False):
    print cur_state
    action = raw_input()
    end_reward,cur_state = envi.step(cur_state,action)


print "REWARD: " + str(end_reward) +  " STATE: "  + str(cur_state)
