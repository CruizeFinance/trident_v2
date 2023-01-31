import requests

from utilities import constant


def asset_price(asset_name):
    url = constant.COINGECKO_HOST + f"/simple/price?ids={asset_name}&vs_currencies=usd"
    try:
        result = dict(requests.get(url).json())
        asset_price = result[asset_name]["usd"]
        return asset_price
    except Exception as e:
        raise Exception(str(e))


if __name__ == "__main__":
    asset_price("ethereum")
