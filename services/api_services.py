import pytz
import requests

from utilities import constant
from dateutil.relativedelta import relativedelta, MO
from datetime import timedelta, datetime, date


def asset_price_coingecko_historical(asset_name, current_day):
    # https://api.coingecko.com/api/v3/coins/bitcoin/history?date=10-07-2023&localization=false
    monday_datetime = str(
        (current_day + relativedelta(weekday=MO(-1))).strftime("%d-%m-%Y")
    )

    url = (
        constant.COINGECKO_HOST
        + f"/coins/{constant.symbol_asset[asset_name]}/history?date={monday_datetime}&localization=false"
    )
    try:
        result = dict(requests.get(url).json())
        asset_price = result["market_data"]["current_price"]["usd"]
        return asset_price
    except Exception as e:
        raise Exception(str(e))


def asset_price(asset_name):
    url = constant.COINBASE_HOST + f"prices/{asset_name}-USD/spot"

    try:
        result = dict(requests.get(url).json())
        asset_price = result["data"]["amount"]
        return asset_price
    except Exception as e:
        raise Exception(str(e))


def asset_price_historic(asset_name, time="09:00", day=None):
    monday = 0
    day_diff = day - monday

    url = constant.COINBASE_HOST + f"prices/{asset_name}-USD/historic?days={day_diff}"
    try:
        result = dict(requests.get(url).json())
        prices = result["data"]["prices"]
        return prices
        # for price in prices:
        #     if time in price['time']:
        #         pass

        return asset_price
    except Exception as e:
        raise Exception(str(e))


if __name__ == "__main__":
    # print(asset_price_historic(asset_name="ETH", day=200))
    # print(binance_get_historical_data(5))
    print(asset_price_coingecko_historical("WBTC", date.today()))
