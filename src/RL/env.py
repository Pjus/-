import gym
from gym import spaces
import numpy as np
import random
from visualize import StockTradingGraph

MAX_ACCOUNT_BALANCE = 2147483647
MAX_NUM_SHARES = 2147483647
MAX_SHARE_PRICE = 5000
MAX_OPEN_POSITIONS = 5
MAX_STEPS = 20000

INITIAL_ACCOUNT_BALANCE = 10000

LOOKBACK_WINDOW_SIZE = 40


class MyEnv(gym.Env):
    """custom enviroment that follows gym interface"""
    metadata = {'render.modes' : ['human']}
    visualization = None

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

        self.trades = []

        return self._next_observation()

    
    def _next_observation(self):
        # get data points for the last 5 dats and scale to between 0-1
        frame = np.array([
            self.df.loc[self.current_step: self.current_step + 5, 'open'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'high'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'low'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'close'].values / MAX_SHARE_PRICE,

            self.df.loc[self.current_step: self.current_step + 5, 'volume'].values / MAX_NUM_SHARES,
        ])

        #append additional data and scale each value to between 0-1
        obs = np.append(frame, [[
            self.balance / MAX_ACCOUNT_BALANCE,
            self.max_net_worth / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES,
            self.cost_basis / MAX_SHARE_PRICE,
            self.total_shares_sold / MAX_SHARE_PRICE,
            self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),

        ]], axis=0)

        return obs

    def step(self, action):
        # excute one time step within the environment
        self.__take_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:, 'open'].values) - 6:
            self.current_step = 0

        delay_modifier = (self.current_step / MAX_STEPS)

        reward = self.balance * delay_modifier
        done = self.net_worth <= 0

        obs = self._next_observation()

        return obs, reward, done, {}

    
    def __take_action(self, action):
        # set the current price to a random price within the time step 
        current_price = random.uniform(
            self.df.loc[self.current_step, 'open'],
            self.df.loc[self.current_step, 'close'])

        action_type = action[0]
        amount = action[1]


        if action_type < 1:
            #Buy amount % of balance in shares
            total_possible = self.balance / current_price
            shares_bought = total_possible * amount
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price

            self.balance -= additional_cost
            self.cost_basis = (prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held += shares_bought

            if shares_bought > 0:
                self.trades.append({'step': self.current_step, 'shares': shares_bought, 'total': additional_cost, 'type':'Buy'})

        elif action_type < 2:
            # Sell amount % of shares held 
            shares_sold = self.shares_held * amount
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

            if shares_sold > 0:
                self.trades.append({'step': self.current_step, 'shares': shares_sold, 'total': shares_sold * current_price, 'type': 'Sell'})

        self.net_worth = self.balance + self.shares_held * current_price

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth
        if self.shares_held == 0:
            self.cost_basis = 0
        

    # def render(self, mode='human', close=False):
    #     # Render env to the screen
    #     profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

    #     print(f'Step : {self.current_step}')
    #     print(f'Balance : {self.balance}')
    #     print(f'Shared held: {self.shares_held}(Total sold : {self.total_shares_sold})')
    #     print(f'Avg cost for held shares: {self.cost_basis}(Total sales value: {self.total_sales_value})')
    #     print(f'Net worth: {self.net_worth}(Max net worth: {self.max_net_worth})')
    #     print(f'Profit: {profit}')
    
    
    def _render_to_file(self, filename='render.txt'):
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

        file = open(filename, 'a+')

        file.write(f'Step : {self.current_step}\n')
        file.write(f'Balance : {self.balance}\n')
        file.write(f'Shared held: {self.shares_held}(Total sold : {self.total_shares_sold})\n')
        file.write(f'Avg cost for held shares: {self.cost_basis}(Total sales value: {self.total_sales_value})\n')
        file.write(f'Net worth: {self.net_worth}(Max net worth: {self.max_net_worth})\n')
        file.write(f'Profit: {profit}\n')

        file.close()

    # New render
    def render(self, mode='live', title=None, **kwargs):
        # render the env to the screen

        if mode == 'file':
            self._render_to_file(kwargs.get('filename', 'render.txt'))
        elif mode == 'live':
            if self.visualization == None:
                self.visualization = StockTradingGraph(self.df, title)

            if self.current_step > LOOKBACK_WINDOW_SIZE:
                self.visualization.render(self.current_step, self.net_worth, self.trades, window_size=LOOKBACK_WINDOW_SIZE)
        


    


    