from datetime import datetime, timedelta

import pandas as pd

def place_sell_order(dhan_client, order_data):
    try:
        response = dhan_client.place_order(
            exchange="NSE", 
            segment="EQ",   
            order_type="SELL", 
            product_type="MIS", 
            symbol=order_data.symbol,
            quantity=order_data.quantity,
            price=order_data.price,
        )
        return response
    except Exception as e:
        return {"error": str(e)}


def place_buy_order(dhan_client, order_data):
    try:
        response = dhan_client.place_order(
            exchange="NSE",  
            segment="EQ",
            order_type="BUY",
            product_type="MIS", 
            symbol=order_data.symbol,
            quantity=order_data.quantity,
            price=order_data.price,
        )
        return response
    except Exception as e:
        return {"error": str(e)}
    



def backtest_strategy(symbol, start_date, end_date, strategy_logic):
    data = get_historical_data(symbol, start_date, end_date)

    portfolio_value = 0
    transaction_history = []

    for index, row in data.iterrows():
        current_price = row["close"]

        signal = strategy_logic(row)

        if signal == "BUY":
            portfolio_value += 0
            transaction_history.append({"timestamp": index, "action": "BUY", "price": current_price})
        elif signal == "SELL":
            portfolio_value -= 0
            transaction_history.append({"timestamp": index, "action": "SELL", "price": current_price})


    return portfolio_value, transaction_history, performance_metrics


