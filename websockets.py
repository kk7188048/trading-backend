import asyncio
import websockets

from dhanhq import marketfeed

class MarketPriceHandler:
    def __init__(self, on_price_update):
        self.on_price_update = on_price_update

    async def connect(self):
        async with websockets.connect("wss://api-feed.dhan.co") as websocket:
            await self.subscribe(websocket)
            while True:
                message = await websocket.recv()
                data = marketfeed.decode_message(message)
                price = data.get("last_price")  
                await self.on_price_update(price)

    async def subscribe(self, websocket):
        subscription_data = marketfeed.get_subscription_packet(
            "YOUR_CLIENT_ID", "YOUR_ACCESS_TOKEN", [(1, "1234")]  
        )
        await websocket.send(subscription_data)
