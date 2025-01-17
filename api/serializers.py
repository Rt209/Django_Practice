from rest_framework import  serializers
from .models import Item, Location, Inventory

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('__all__') 

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('__all__')
        # myapp/serializer.py

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory  # 參考新的 Inventory 模型
        fields = '__all__'  # 包含所有字段
