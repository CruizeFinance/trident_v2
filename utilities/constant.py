import pytz

CRUIZE_CONTRACT = "0xb41Ca4738D0a491acBb88375C62FCb540410Ac52"
symbol_asset = {
    "WETH": "ethereum",
    "WBTC": "bitcoin",
    "BTC": "bitcoin",
    "USDC": "usd",
    "ETH": "ethereum",
}
asset_decimals = {"WETH": 1e18, "WBTC": 1e08, "USDC": 1e06, "ETH": 1e18}
# asset_tvl_testnet_v1 = {"WETH": 1614, "WBTC": 212, "USDC": 0, "ETH": 0}

asset_cap_decimal = 1e18
networks = {
    "testnet": {"421613": "arbitrum-goerli"},
    "mainnet": {"42161": "arbitrum"},
}

# TODO:make sure to use the mainnet data here.
COINGECKO_HOST = "https://api.coingecko.com/api/v3"
COINBASE_HOST = "https://api.coinbase.com/v2/"

UTC = pytz.utc

BINANCE_API_KEY = "9zFIgetckRO80d4RciWs8jc4XSwAMEnFIuwVhAoaYIstQ9RWlfqiV6zcAGu0Ta8R"
BINANCE_API_SECRET = "Uu8vtNEmH1PPDPDchX51jivxBENEbNwDmDcQrnhPJBJwFcbqjnvxL2MeQJuTc4Kg"
