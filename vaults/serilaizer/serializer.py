from rest_framework import serializers


class FetchPriceRangeRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=True)
