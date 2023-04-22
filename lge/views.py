import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from components import FirebaseDataManager
from lge.serilaizer import (
    ReferralLinkRequestSerializer,
)


class LGE(GenericViewSet):
    def referral_link(self, request):
        result = {"message": None, "error": None}
        serializer_class = ReferralLinkRequestSerializer
        request_body = json.loads(request.body)
        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            referral_code = validated_data.get("referral_link").split("referral_code=")[
                1
            ]
            user_addr = validated_data.get("user_addr")
            data = {f"{user_addr}": validated_data}

            firebase_data_manager = FirebaseDataManager()
            collection_name = "lge_referral"
            document = referral_code

            referral_data_exists = firebase_data_manager.document_exists(
                collection_name=collection_name, document=document
            )
            if referral_data_exists is True:
                user_data = firebase_data_manager.fetch_data(
                    collection_name=collection_name, document_name=document
                ).get(user_addr)
                if user_data:
                    deposit_amount = float(user_data["deposit_amount"])
                    data[user_addr]["deposit_amount"] += deposit_amount
                firebase_data_manager.update_data(
                    collection_name=collection_name, document=document, data=data
                )
            else:
                firebase_data_manager.store_data(
                    collection_name=collection_name, document=document, data=data
                )

            result["message"] = "Successfully Stored Referral Information"
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
