from rest_framework import serializers
from .models import User, TransactionHistory
from decimal import Decimal


class DecimalField(serializers.Field):
    def to_representation(self, value):
        return float(value)  # Convert Decimal to float

    def to_internal_value(self, data):
        return Decimal(str(data))


class UserSerializer(serializers.ModelSerializer):
    balance = DecimalField()

    class Meta:
        model = User
        fields = "__all__"


class SimpleUserSerializer(serializers.ModelSerializer):
    balance = DecimalField()

    class Meta:
        model = User
        fields = ["id", "name", "email", "balance"]


class UserChoiceField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return f"{instance.id} - {instance.name}"


class TransactionHistorySerializer(serializers.ModelSerializer):
    from_user = UserChoiceField(queryset=User.objects.all())
    to_user = UserChoiceField(queryset=User.objects.all())
    amount = DecimalField()

    class Meta:
        model = TransactionHistory
        fields = "__all__"

    def validate(self, attrs):
        if attrs["from_user"] == attrs["to_user"]:
            raise serializers.ValidationError("From user and To user cannot be the same.")
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["from_user"] = UserSerializer(instance.from_user).data
        representation["to_user"] = UserSerializer(instance.to_user).data
        return representation
