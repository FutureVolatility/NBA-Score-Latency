from py_clob_client.client import ClobClient
import os

# init
host = "https://clob.polymarket.com"
private_key = os.getenv("PRIVATE_KEY")  
chain_id = 137  # Polygon Mainnet
client = ClobClient(host, key=private_key, chain_id=chain_id)

market_id = "example-market"

market_details = client.get_market(market_id)

# get each token id for trading 
tokens = market_details.get('tokens', [])
for token in tokens:
    outcome = token.get('outcome')
    token_id = token.get('token_id')
    print(f"Outcome: {outcome}, Token ID: {token_id}")
