import gym
import json
import datetime as dt

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from env import MyEnv

import pandas as pd
import FundamentalAnalysis as fa

import warnings
warnings.filterwarnings(action='ignore')

ticker = "AAPL"
api_key = "d2b83a9cbe59bd13f8c7615015e41b0e"


df = fa.stock_data(ticker, period="ytd", interval="1d")
df['Date'] = df.index

df.index = range(len(df))

# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: MyEnv(df)])


model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=20000)

obs = env.reset()
for i in range(2000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()