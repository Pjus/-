import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc as candlestick
from matplotlib import style

style.use('dark_background')

VOLUME_CHART_HEIGHT = 0.33

UP_COLOR = '#27A59A'
DOWN_COLOR = '#EF534F'
UP_TEXT_COLOR = '#73D3CC'
DOWN_TEXT_COLOR = '#DC2C27'


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

        # format dates as timestemps mecessary for candlestick graph
        self.price_ax.set_xticklabels(self.df['Date'].values[step_range], rotation=45, horizontalalignment='right')

        # hide duplicate net worth date labels
        plt.setp(self.net_worths_ax.get_xticklabels(), visible=False)

        # necessary to view frames before they are unrendered
        plt.pause(0.001)

    def _render_net_worth(self, current_step, net_worth, step_range, dates):
        # clear the frame rendered last step
        self.net_worths_ax.clear()

        # plot net worths
        self.net_worths_ax.plot_date(dates, self.net_worths[step_range], '-', label='Net Worth')

        # show legend, which uses thw label we defined for the plot avobe
        self.net_worths_ax.legend()
        legend = self.net_worth_ax.legend(loc=2, ncol=2, prop={'size': 8})
        legend.get_frame().set_alpha(0.4)

        last_date = date2num(self.df['Date'].values[current_step])
        last_net_worth = self.net_worths[current_step]

        # annotate the current net worth on the net worth graph
        self.net_worth_ax.annotate('{0:.2f}'.format(net_worth),\
            (last_date, last_net_worth),\
            xytext = (last_date, last_net_worth),\
            bbox = dict(last_date, last_net_worth),\
            color='black',\
            fontsize='small')

        # add space above and below min max net worth
        self.net_worths_ax.set_ylim(
            min(self.net_worths[np.nonzero(self.net_worths)] / 1.25,\
            max(self.net_worths) * 1.25))

    def _render_price(self, current_step, net_worth, dates, step_range):
        self.price_ax.clear()

        #format data for OHCL cnadlestick graph

        candlesticks = zip(dates,\
            self.df['open'].values[step_range],
            self.df['close'].values[step_range],
            self.df['high'].values[step_range],
            self.df['low'].values[step_range],
        )

        #plot price using candlestick graph from mplfinance
        candlestick(self.price_ax, candlesticks, width=1, colorup=UP_COLOR, colordown=DOWN_COLOR)

        last_date = date2num(self.df['Date'].values[current_step])
        last_close = self.df['close'].values[current_step]
        last_high = self.df['high'].values[current_step]


        #print the current price to the price axis
        self.price_ax.annotate('{0:.2f}'.format(last_close),\
            (last_date, last_close),
            xytext=dict(last_date, last_high),
            bbox=dict(boxstyle='round', fc='w', ec='k', lw=1),
            color='black',
            fontsize='small'
        )

        #shift priice axis up to give volume chart space
        ylim = self.price_ax.get_ylim()
        self.price_ax.set_ylim(ylim[0] - (ylim[1] - ylim[0]) * VOLUME_CHART_HEIGHT, ylim[1])

    def _render_volume(self, current_step, net_worth, dates, step_range):
        self.volume_ax.clear()

        volume = np.array(self.df)

        pos = self.df['open'].values[step_range] - \
            self.df['close'].values[step_range] < 0
        
        neg = self.df['open'].values[step_range] - \
            self.df['close'].values[step_range] > 0
        
        # color volume bars based on price direction on that date
        self.volume_ax.bar(dates[pos], volume[pos], color=UP_COLOR, alpha=0.4, width=1, align='center')
        self.volume_ax.bar(dates[neg], volume[neg], color=DOWN_COLOR, alpha=0.4, width=1, align='center')

        #cap volume axis height below price chart and hide ticks
        self.volume_ax.set_ylim(0, max(volume) / VOLUME_CHART_HEIGHT)
        self.volume_ax.yaxis.set_ticks([])

    def _render_trades(self, current_step, trades, step_range):
        for trade in trades:
            if trade['step'] in step_range:
                date = date2num(self.df['Date'].values[trade['step']])
                high = self.df['high'].values[trade['step']]
                low = self.df['low'].values[trade['step']]






