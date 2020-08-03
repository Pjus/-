import gym
from gym import spaces
import numpy as np
import random

class MyEnv(gym.Env):
    """custom enviroment that follows gym interface"""
    metadata = {'render.modes' : ['human']}

    def __init__(self, df):
        super(MyEnv, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)

        # actions of the format Buy Sell Hold
        self.action_space = spaces.Box(
            low = np.array([0,0]), high=np.array([3,1]), dtype=np.float16)
        
        #prices contains the OHCL(open high low close) values for the last five prices
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(6,6), dtype=np.float16)

    def reset(self):
        #reset state of the environment to an initial state
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE

        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        # set the current step to a random point within the data frame
        self.current_step = random.randint(0, len(self.df.loc[:,'open'].values) - 6)

        return self._next_observation()

    
    def _next_observation(self):
        # get data points for the last 5 dats and scale to between 0-1
        frame = np.array([
            self.df.loc[self.current_step: self.current_step + 5, 'open'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'high'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'low'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'close'].values / MAX_SHARE_PRICE,

            self.df.loc[self.current_step: self.current_step + 5, 'volumn'].values / MAX_NUM_SHARES,
        ])

        #append additional data and scale each value to between 0-1
        obs = np.append(frame, [[
            self.balance / MAX_ACCOUNT_BALANCE,
            self.max_net_worth / MAX_ACCOUNT_BALANCE,
            
        ]])



            