import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, MarketOrderArgs, OrderType
from dotenv import load_dotenv
from py_clob_client.constants import AMOY
from py_clob_client.order_builder.constants import BUY


load_dotenv()


def main():
    host = "http://localhost:8080"
    key = os.getenv("PK")
    creds = ApiCreds(
        api_key=os.getenv("CLOB_API_KEY"),
        api_secret=os.getenv("CLOB_SECRET"),
        api_passphrase=os.getenv("CLOB_PASS_PHRASE"),
    )
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    # give token-id from clob, amount in $, and side you would like to execute (buy/sell)
    order_args = MarketOrderArgs(
        token_id="example-token-id",
        amount=100,  # $$$
        side=BUY,
    )
    signed_order = client.create_market_order(order_args)
    resp = client.post_order(signed_order, orderType=OrderType.FOK)
    print(resp)
    print("Done!")


main()
