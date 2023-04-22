from django.urls import path

from lge.views import LGE

urlpatterns = [
    path("referral_link/", LGE.as_view({"post": "referral_link"})),
]
