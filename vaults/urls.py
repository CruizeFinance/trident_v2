from django.urls import path

from vaults.views import Vaults

urlpatterns = [
    path("price_range", Vaults.as_view({"get": "price_range"})),
    path("expiration", Vaults.as_view({"get": "expiration"})),
]
