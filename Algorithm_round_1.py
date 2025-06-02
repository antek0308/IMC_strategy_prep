from datamodel import OrderDepth, TradingState, Order
from typing import List

# prosperity2bt algorithm4.py 1 

class Trader:

    def run(self, state: TradingState):
        result = {}

        # Parameters
        pos_limit = 20
        base_order_size = 10
        spread_threshold = 0
        tick_improvement = 1

        for product in state.order_depths:
            depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            pos = state.position.get(product, 0)

            bid_prices = sorted(depth.buy_orders.keys(), reverse=True)
            ask_prices = sorted(depth.sell_orders.keys())

            if bid_prices:
                if len(bid_prices) >= 2:
                    bid_avg = (bid_prices[0] + bid_prices[1]) / 2
                else:
                    bid_avg = bid_prices[0]
            else:
                bid_avg = None

            if ask_prices:
                if len(ask_prices) >= 2:
                    ask_avg = (ask_prices[0] + ask_prices[1]) / 2
                else:
                    ask_avg = ask_prices[0]
            else:
                ask_avg = None

            if bid_avg is not None and ask_avg is not None:
                fair_value = (bid_avg + ask_avg) / 2
            elif bid_avg is not None:
                fair_value = bid_avg
            elif ask_avg is not None:
                fair_value = ask_avg
            else:
                fair_value = 10000 # fallback

            if bid_prices:
                best_bid = bid_prices[0]
                if best_bid >= fair_value + spread_threshold:
                    orders.append(Order(product, best_bid, -base_order_size))
                elif best_bid == fair_value and pos > 0:
                    orders.append(Order(product, best_bid, -pos))

            if ask_prices:
                best_ask = ask_prices[0]
                if best_ask <= fair_value - spread_threshold:
                    orders.append(Order(product, best_ask, base_order_size))
                elif best_ask == fair_value and pos < 0:
                    orders.append(Order(product, best_ask, -pos))

            risk_multiplier = max(0, (pos_limit - abs(pos)) / pos_limit)
            adjusted_size = int(base_order_size * risk_multiplier)
            if adjusted_size > 0:
                buy_price = int(fair_value) - tick_improvement
                orders.append(Order(product, buy_price, adjusted_size))
                
                sell_price = int(fair_value) + tick_improvement
                orders.append(Order(product, sell_price, -adjusted_size))

            result[product] = orders

        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData