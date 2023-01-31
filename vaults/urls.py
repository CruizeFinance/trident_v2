from django.urls import path

from vaults.views import Vaults

urlpatterns = [
    path("price_range", Vaults.as_view({"get": "price_range"})),
    path("expiration", Vaults.as_view({"get": "expiration"})),
    path("asset_tvl", Vaults.as_view({"get": "asset_tvl"})),
    path("total_tvl", Vaults.as_view({"get": "all_asset_tvl"})),

]
