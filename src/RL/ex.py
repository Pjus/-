# import gym
# env = gym.make('CartPole-v0')
# env.reset()
# for _ in range(1000):
#     env.render()
#     env.step(env.action_space.sample()) # take a random action
# env.close()

import gym
env = gym.make('CartPole-v0')
for i_epoisode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finised after {}timesteps".format(t+1))
            break
env.close()

# import gym
# env = gym.make('CartPole-v0')
# print(env.action_space)
# print(env.observation_space)

# from gym import spaces
# space = spaces.Discrete(2)
# x = space.sample()

# # 가정 함수 assert 
# assert space.contains(x)
# assert space.n == 2, '크기가 다름'