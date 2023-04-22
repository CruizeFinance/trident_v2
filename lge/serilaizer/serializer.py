from rest_framework import serializers


class ReferralLinkRequestSerializer(serializers.Serializer):
    referral_link = serializers.CharField(required=True)
    deposit_amount = serializers.FloatField(required=True)
    user_addr = serializers.CharField(required=True)
