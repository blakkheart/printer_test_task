from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.IntegerField()


class ItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.IntegerField()


class CheckSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    items = ItemSerializer(many=True)
    address = serializers.CharField()
    client = ClientSerializer()
    point_id = serializers.IntegerField()
