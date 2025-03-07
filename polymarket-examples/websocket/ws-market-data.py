import websocket
import json

## ws-market-data.py ##
"""
File is example file for getting the asset
bid/ask for X market
"""

WSS_URL = "wss://clob.polymarket.com"

# use actual asset ids
ASSET_IDS = []

subscribe_message = {
    "type": "market",
    "assets_ids": ASSET_IDS
}

# websocket message handlers 
def on_message(ws, message):
    data = json.loads(message)
    
    if data.get("event_type") == "book":
        asset_id = data["asset_id"]
        market_id = data["market"]
        timestamp = data["timestamp"]

        bids = data.get("buys", [])  
        asks = data.get("sells", [])  

        print(f"\nMarket: {market_id} | Asset ID: {asset_id} | Timestamp: {timestamp}")
        print("Bids (Buy Orders):")
        for bid in bids:
            print(f" - Price: {bid['price']}, Size: {bid['size']}")

        print("\nAsks (Sell Orders):")
        for ask in asks:
            print(f" - Price: {ask['price']}, Size: {ask['size']}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    print("WebSocket Connected. Subscribing to market updates...")
    ws.send(json.dumps(subscribe_message))

# start ws
ws = websocket.WebSocketApp(WSS_URL, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open
ws.run_forever()
