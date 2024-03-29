from datetime import datetime, timedelta, date
import time


from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from components import FirebaseDataManager
from components import VaultStrategyPlot
from services import CruizeContract, api_services
from utilities.constant import UTC

from vaults.serilaizer import (
    FetchPriceRangeRequestSerializer,
    ExpirationRequestSerializer,
    AssetTVLRequestSerializer,
    VaultPlotRequestSerializer,
    AssetAPYRequestSerializer,
    TotalTVLRequestSerializer,
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
            asset_info = firebase_db_manager_obj.fetch_data(
                collection_name=validated_data.get("vault"),
                document_name=validated_data.get("asset_name"),
            )
            price_range = asset_info["price_range"]
            # asset_price_9am_utc = float(asset_info["asset_price_9am_utc"])
            asset_price_monday = float(
                api_services.asset_price_coingecko_historical(
                    asset_name=validated_data.get("asset_name"),
                    current_day=date.today(),
                )
            )

            lower_bound_pcg = int(price_range["lower_bound"])
            upper_bound_pcg = int(price_range["upper_bound"])
            lower_bound = asset_price_monday * (lower_bound_pcg / 100)
            upper_bound = asset_price_monday * (upper_bound_pcg / 100)

            result["message"] = {
                "upper_bound": round(upper_bound, 2),
                "lower_bound": round(lower_bound, 2),
            }
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    def asset_tvl(self, request):
        result = {"message": None, "error": None}
        serializer_class = AssetTVLRequestSerializer
        request_body = request.query_params
        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        cruize_vault_obj = CruizeContract()

        try:
            result["message"] = cruize_vault_obj.asset_tvl(
                validated_data["asset_symbol"],
                validated_data["network_id"],
            )
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def total_tvl(self, request):
        result = {"message": None, "error": None}
        serializer_class = TotalTVLRequestSerializer
        request_body = request.query_params
        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        cruize_contract_obj = CruizeContract()
        try:
            result["message"] = cruize_contract_obj.total_tvl(
                network_env=validated_data["network_env"]
            )
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def strategy_plot_data(self, request):
        result = {"message": None, "error": None}
        data = request.query_params
        serializer_class = VaultPlotRequestSerializer
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            vault_strategy_plot = VaultStrategyPlot(
                vault=validated_data.get("vault"),
                asset_symbol=validated_data.get("asset_symbol"),
            )
            vault_strategy_plot_data = (
                vault_strategy_plot.strategy_plot_data().to_dict()
            )
            result["message"] = vault_strategy_plot_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def asset_apy(self, request):
        result = {"message": {}, "error": None}
        data = request.query_params
        serializer_class = AssetAPYRequestSerializer
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            firebase_db_manager_obj = FirebaseDataManager()
            asset_apy = firebase_db_manager_obj.fetch_data(
                collection_name=validated_data.get("vault"),
                document_name="apy",
            )
            result["message"] = asset_apy
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
