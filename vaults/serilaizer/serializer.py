from rest_framework import serializers

from utilities.enum import Vaults


class FetchPriceRangeRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=True)
    vault = serializers.CharField(required=True)


class ExpirationRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=False)
    vault = serializers.CharField(required=True)


class AssetTVLRequestSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField(required=True)
    network_id = serializers.CharField(required=True)


class VaultPlotRequestSerializer(serializers.Serializer):
    vault = serializers.ChoiceField(
        required=True, choices=[vault.value for vault in Vaults]
    )


class AssetAPYRequestSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField(required=True)
