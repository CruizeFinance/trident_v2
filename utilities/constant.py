CRUIZE_CONTRACT = "0xb41Ca4738D0a491acBb88375C62FCb540410Ac52"
symbol_asset = {
    "WETH": "wrapped ether",
    "WBTC": "bitcoin",
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
