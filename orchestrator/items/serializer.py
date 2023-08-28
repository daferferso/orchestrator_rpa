from rest_framework.serializers import ModelSerializer
from .models import Item
from values.serializer import ValueSerializer


class ItemSerializer(ModelSerializer):
    value = ValueSerializer()  # Serializador de Value anidado

    class Meta:
        model = Item
        fields = '__all__'
