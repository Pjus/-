import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def date2num(date):
    converter = mdates.strpdate2num('%Y-%m-%d')
    return converter(date)

class StockTradingGraph:
    """ A stock trading visualization using matplotlib 
        made to render OpenAI gym environments """

    def __init__(self, df, title=None):
        self.df = df
        self.net_worths = np.zeros(len(df['Date']))

        # create figure on screen and set the title
        fig = plt.figure()
        fig.suptitle(title)

        # create top subplot for net worth axis
        self.net_worths_ax = plt.subplot2grid((6, 1), (0, 0), rowspan=2, colspan=1)

        # create bottom subplot for shares price / volume axis
        self.price_ax = plt.subplot2grid((6, 1), (2, 0), rowspan=8, colspan=1, sharex = self.net_worths_ax)

        # create a new axis for volume which shares its x-axis with price
        self.volume_ax = self.price_ax.twinx() # y축이 다를때 .twinx() 사용 

        # add padding to make graph easier to view
        plt.subplots_adjust(left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0)

        # show the graph without blocking the rest of the program
        plt.show(block=False)
    
    def render(self, current_step, net_worth, trades, window_size=40):
        self.net_worths[current_step] = net_worth

        window_start = max(current_step - window_size, 0)
        step_range = range(window_start, current_step + 1)

        



