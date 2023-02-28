from rest_framework import serializers

from utilities.enum import Vaults


class FetchPriceRangeRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=True)
    vault = serializers.ChoiceField(
        required=True, choices=[vault.value for vault in Vaults]
    )


class ExpirationRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=False)
    vault = serializers.ChoiceField(
        required=True, choices=[vault.value for vault in Vaults]
    )


class AssetTVLRequestSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField(required=True)
    network_id = serializers.CharField(required=True)


class TotalTVLRequestSerializer(serializers.Serializer):
    network_env = serializers.CharField(required=False, default="mainnet")


class VaultPlotRequestSerializer(serializers.Serializer):
    vault = serializers.ChoiceField(
        required=True, choices=[vault.value for vault in Vaults]
    )
    asset_symbol = serializers.CharField(required=True)


class AssetAPYRequestSerializer(serializers.Serializer):
    vault = serializers.ChoiceField(
        required=True, choices=[vault.value for vault in Vaults]
    )
