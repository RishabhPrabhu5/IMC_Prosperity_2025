from typing import Dict, List, Tuple
from collections import deque
import jsonpickle
from datamodel import TradingState, Order, OrderDepth


class Trader:
    def __init__(self):
        self.position_limit = {
            'KELP': 100,
            'SQUID_INK': 100,
            'RAINFOREST_RESIN': 100
        }
        self.price_history = {}
        
        # Parameters for Rainforest Resin strategy (stable product)
        self.resin_mean = 10000.00
        self.resin_buy_threshold = 9998.50
        self.resin_sell_threshold = 10001.49
        
    def fair_price(self, product, price):
        if product not in self.price_history:
            self.price_history[product] = deque(maxlen=100)
        self.price_history[product].append(price)
        return sum(self.price_history[product]) / len(self.price_history[product])
        
    def run(self, state: TradingState) -> Tuple[Dict[str, List[Order]], int, str]:
        result = {}
        
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            position = state.position.get(product, 0)
            best_bid = max(order_depth.buy_orders) if order_depth.buy_orders else None
            best_ask = min(order_depth.sell_orders) if order_depth.sell_orders else None
            
            if best_bid is None or best_ask is None:
                continue
                
            mid_price = (best_bid + best_ask) / 2
            
            fair_value = self.fair_price(product, mid_price)
            
            if product == 'RAINFOREST_RESIN':
                orders = self._trade_rainforest_resin(product, order_depth, position)
            else:
                orders = self._trade_default_strategy(product, order_depth, position, best_bid, best_ask, fair_value)
                
            result[product] = orders
            
        traderData = jsonpickle.encode(self.price_history)
        conversions = 0
        return result, conversions, traderData
    
    def _trade_rainforest_resin(self, product, order_depth, position):
        """
        Rainforest Resin strategy: Simple mean reversion around stable price.
        Buy when price is below threshold, sell when above threshold.
        """
        orders = []
        
        # Check if we can buy (price below threshold and position allows)
        if order_depth.sell_orders:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_volume = abs(order_depth.sell_orders[best_ask])
            
            # If price is below buy threshold
            if best_ask < self.resin_buy_threshold:
                # Calculate how much we can buy
                available_position = self.position_limit[product] - position
                buy_volume = min(available_position, best_ask_volume)
                
                if buy_volume > 0:
                    orders.append(Order(product, best_ask, buy_volume))
        
        # Check if we can sell (price above threshold and position allows)
        if order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_volume = order_depth.buy_orders[best_bid]
            
            # If price is above sell threshold
            if best_bid > self.resin_sell_threshold:
                # Calculate how much we can sell
                available_position = position + self.position_limit[product]
                sell_volume = min(available_position, best_bid_volume)
                
                if sell_volume > 0:
                    orders.append(Order(product, best_bid, -sell_volume))
        
        return orders
    
    def _trade_default_strategy(self, product, order_depth, position, best_bid, best_ask, fair_value):
        """
        Default strategy for other products.
        Uses the existing algorithm's approach.
        """
        orders = []
        spread = best_ask - best_bid
        
        buy_price = int(min(best_bid + spread * 0.3, fair_value - 1))
        sell_price = int(max(best_ask - spread * 0.3, fair_value + 1))
        
        for ask_price, ask_amount in sorted(order_depth.sell_orders.items()):
            if ask_price <= buy_price and position < self.position_limit[product]:
                qty_to_buy = min(-ask_amount, self.position_limit[product] - position)
                if qty_to_buy > 0:
                    orders.append(Order(product, ask_price, qty_to_buy))
                    position += qty_to_buy
                    
        for bid_price, bid_amount in sorted(order_depth.buy_orders.items(), reverse=True):
            if bid_price >= sell_price and position > -self.position_limit[product]:
                qty_to_sell = min(bid_amount, self.position_limit[product] + position)
                if qty_to_sell > 0:
                    orders.append(Order(product, bid_price, -qty_to_sell))
                    position -= qty_to_sell
                    
        return orders