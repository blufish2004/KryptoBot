import matplotlib.pyplot as plt
import numpy as np
from catalyst.api import (record, symbol, order_target_percent,)
from catalyst.exchange.utils.stats_utils import extract_transactions
from .base_strategy import BaseStrategy


class SimpleMovingAverage(BaseStrategy):

    def __init__(self, default=None, custom=None):
        super().__init__(default, custom)

    def get_initialize(self):
        def initialize(context):
            context.i = 0
            context.asset = symbol(self.default['pair'])
            context.base_price = None

        return initialize

    def get_handle_data(self):
        def handle_data(context, data):
            short_window = self.custom['long_window']
            long_window = self.custom['short_window']

            # Skip as many bars as long_window to properly compute the average
            context.i += 1
            if context.i < long_window:
                return

            # Compute moving averages calling data.history() for each
            # moving average with the appropriate parameters. We choose to use
            # minute bars for this simulation -> freq="1m"
            # Returns a pandas dataframe.
            short_data = data.history(context.asset,
                                      'price',
                                      bar_count=short_window,
                                      frequency="1T",
                                      )
            short_mavg = short_data.mean()
            long_data = data.history(context.asset,
                                     'price',
                                     bar_count=long_window,
                                     frequency="1T",
                                     )
            long_mavg = long_data.mean()

            # Let's keep the price of our asset in a more handy variable
            price = data.current(context.asset, 'price')

            # If base_price is not set, we use the current value. This is the
            # price at the first bar which we reference to calculate price_change.
            if context.base_price is None:
                context.base_price = price
            price_change = (price - context.base_price) / context.base_price

            # Save values for later inspection
            record(price=price,
                   cash=context.portfolio.cash,
                   price_change=price_change,
                   short_mavg=short_mavg,
                   long_mavg=long_mavg)

            # Since we are using limit orders, some orders may not execute immediately
            # we wait until all orders are executed before considering more trades.
            orders = context.blotter.open_orders
            if len(orders) > 0:
                return

            # Exit if we cannot trade
            if not data.can_trade(context.asset):
                return

            # We check what's our position on our portfolio and trade accordingly
            pos_amount = context.portfolio.positions[context.asset].amount

            # Trading logic
            if short_mavg > long_mavg and pos_amount == 0:
                # we buy 100% of our portfolio for this asset
                order_target_percent(context.asset, 1)
            elif short_mavg < long_mavg and pos_amount > 0:
                # we sell all our positions for this asset
                order_target_percent(context.asset, 0)

        return handle_data

    def get_analyze(self):
        def analyze(context, perf):
            pass

        return analyze
