from datetime import datetime, timedelta

import pytz
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from components import FirebaseDataManager
from services import CruizeVault
from vaults.serilaizer import (
    FetchPriceRangeRequestSerializer,
    ExpirationRequestSerializer,
    AssetTVLRequestSerializer,
)



class Vaults(GenericViewSet):
    def price_range(self, request):
        result = {"message": None, "error": None}
        serializer_class = FetchPriceRangeRequestSerializer
        request_body = request.query_params
        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            firebase_db_manager_obj = FirebaseDataManager()
            price_range = firebase_db_manager_obj.fetch_data(
                collection_name=validated_data.get("vault"),
                document_name=validated_data.get("asset_name"),
            )["price_range"]
            lower_bound = price_range["lower_bound"]
            upper_bound = price_range["upper_bound"]
            result["message"] = {"upper_bound": upper_bound, "lower_bound": lower_bound}

        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(result, status.HTTP_200_OK)

    def expiration(self, request):
        result = {"message": None, "error": None}
        serializer_class = ExpirationRequestSerializer
        request_body = request.query_params
        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        current_datetime = datetime.utcnow()
        today = datetime.today()
        friday = today + timedelta((4 - today.weekday()) % 7)
        if validated_data.get("vault") == "principle_protection":
            friday = today + timedelta((4 - today.weekday()) % 7)
            friday = friday.replace(hour=5, minute=30, second=0, microsecond=0)

        expiration = friday - current_datetime
        time = str(expiration).split(",")[1].split(":")
        hours = time[0]
        minutes = time[1]
        expiration_dict = {
            "days": str(expiration).split(",")[0].split(" ")[0],
            "hours": hours,
            "minutes": minutes,
        }
        result["message"] = expiration_dict
        return Response(result, status=status.HTTP_200_OK)

    # load contract
    #  read values
    def asset_tvl(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = AssetTVLRequestSerializer
        request_body = request.query_params
        serializer = self.serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        cruize_vault_obj = CruizeVault()
        try:
            result["message"] = cruize_vault_obj.asset_tvl(
                validated_data["asset_symbol"]
            )
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def all_asset_tvl(self, request):
        result = {"message": None, "error": None}
        cruize_vault_obj = CruizeVault()
        try:
            result["message"] = cruize_vault_obj.all_assets_tvl()
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

