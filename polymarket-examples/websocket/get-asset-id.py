import requests

host = "https://clob.polymarket.com"
market_id = "example-market"

# get market details
response = requests.get(f"{host}/markets/{market_id}")
market_data = response.json()

# get each asset ids #
asset_ids = [token['token_id'] for token in market_data.get('tokens', [])]
print("Asset IDs:", asset_ids)
