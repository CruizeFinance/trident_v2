from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from components import FirebaseDataManager
from vaults.serilaizer import FetchPriceRangeRequestSerializer


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
                collection_name="assets_price_range",
                document_name=validated_data.get("asset_name"),
            )["price_range"]
            lower_bound = price_range["lower_bound"]
            upper_bound = price_range["upper_bound"]
            result["message"] = {"upper_bound": upper_bound, "lower_bound": lower_bound}

        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(result, status.HTTP_200_OK)
