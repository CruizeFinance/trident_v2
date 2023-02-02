from rest_framework import serializers


class FetchPriceRangeRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=True)
    vault = serializers.CharField(required=True)


class ExpirationRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=False)
    vault = serializers.CharField(required=True)


class AssetTVLRequestSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField(required=True)
    network_id = serializers.CharField(required=False, default=5)


class AssetTotalTVLRequestSerializer(serializers.Serializer):
    network_id = serializers.CharField(required=True)
