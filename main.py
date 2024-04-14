from fastapi import FastAPI
from dhanhq import dhanhq
from models import Order, DhanPostback
from services import place_buy_order, place_sell_order, backtest_strategy
from websockets import WebsocketException, connect  
app = FastAPI()
import pandas as pd
from dhanhq import marketfeed
import requests
import matplotlib.pyplot as plt

dhan = dhanhq("client_id", "access_token")

current_price = None


@app.get("/holdings")
async def get_holdings():
    try:
        return dhan.get_holdings()
    except Exception as e:
        return {"error": f"Error fetching holdings: {str(e)}"}


@app.post("/orders/buy", response_model=dict)
async def place_buy_order_api(order_data: Order):
    try:
        response = place_buy_order(dhan, order_data)
        return response
    except Exception as e:
        return {"error": f"Error placing buy order: {str(e)}"}


@app.post("/orders/sell", response_model=dict)
async def place_sell_order_api(order_data: Order):
    try:
        response = place_sell_order(dhan, order_data)
        return response
    except Exception as e:
        return {"error": f"Error placing sell order: {str(e)}"}


def update_price(price):
    global current_price
    current_price = price


async def connect_to_price_feed():
    try:
        async with connect("wss://api-feed.dhan.co") as websocket:
            price_handler = MarketPriceHandler(update_price, websocket)
            await price_handler.handle_messages()
    except WebsocketException as e:
        print(f"Error connecting to price feed: {str(e)}")


task = asyncio.create_task(connect_to_price_feed())


@app.get("/current_price")
async def get_current_price():
    if current_price is None:
        return {"error": "Current price not yet available"}
    return {"current_price": current_price}


@app.post("/dhan/postback")
async def handle_dhan_postback(data: DhanPostback):
    try:
        if isinstance(data, dict):
            order_id = data.get("order_id")
            status = data.get("status")
            print(f"Order {order_id} status update: {status}")
            return {"message": "Postback received successfully"}
        else:
            return {"error": "Invalid postback data format"}
    except Exception as e:
        return {"error": f"Error processing postback: {str(e)}"}


instruments = [(1, "1333"), (0, "13")] # It is for HDFC Bank NSE and BSE
subscription_code = marketfeed.Ticker

crossover_threshold = 10
crossover_price = 0
crosdown_threshold = -10
crosdown_price = 0

async def on_connect(instance):
    print("Connected to websocket")
    await instance.subscribe(subscription_code)

#Tried to implement here trading algorithm for crossover and cross down
async def on_message(instance, message):
    print("Received:", message)
    price = message[13:16]
    if price > crossover_price:
        if price - crossover_price > crossover_threshold:
            dhan.place_order(security_id='1333', exchange_segment=dhan.NSE, transaction_type=dhan.BUY, quantity=10, order_type=dhan.MARKET, product_type=dhan.INTRA, price=0)
            crossover_price = price

    elif price < crosdown_price:
        if crosdown_price - price > crosdown_threshold:
            dhan.place_order(security_id='1333', exchange_segment=dhan.NSE, transaction_type=dhan.SELL, quantity=10, order_type=dhan.MARKET, product_type=dhan.INTRA, price=0)
            crosdown_price = price

feed = marketfeed.DhanFeed(
    client_id,
    access_token,
    instruments,
    subscription_code,
    on_connect=on_connect,
    on_message=on_message
)
feed.run_forever()

#Taking for an example
#here on the basis of past 10 candles average we can predict 11th candle closing price

candles = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
closing_prices = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]

average_price = sum(closing_prices[-10:]) / 10
predicted_price = average_price

plt.plot(candles, closing_prices, label="Closing Prices")
plt.plot([candles[-1], candles[-1]], [average_price, predicted_price], label="Average Price")
plt.plot([candles[-1], candles[-1]], [predicted_price, predicted_price], label="Predicted Price")
plt.xlabel("Candles")
plt.ylabel("Price")
plt.title("Predicting Closing Price for 11th Candle")
plt.legend()
plt.show()
