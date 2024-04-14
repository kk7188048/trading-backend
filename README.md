# FastAPI Trading Backend

This project is a backend service built using FastAPI for implementing a basic trading system. It allows users to fetch their holdings, place buy and sell orders, and receive postbacks from the broker. Additionally, it connects to a market feed WebSocket for real-time price updates and implements a basic trading algorithm based on moving average crossover and cross-down strategies.

## Features

- **Holdings**: Fetch current holdings of the user.
- **Place Orders**: Place buy and sell orders through the broker's API.
- **WebSocket Price Feed**: Connects to a WebSocket for real-time price updates.
- **Trading Algorithm**: Implements a basic trading algorithm for moving average crossover and cross-down strategies.
- **Postbacks**: Receives postbacks from the broker regarding order status updates.


## Access the API endpoints:

- **Holdings**: `GET /holdings`
- **Place Buy Order**: `POST /orders/buy`
- **Place Sell Order**: `POST /orders/sell`
- **Current Price**: `GET /current_price`
- **Dhan Postback**: `POST /dhan/postback`

## Connect to the WebSocket for real-time price updates:

- **WebSocket URL**: `wss://api-feed.dhan.co`
