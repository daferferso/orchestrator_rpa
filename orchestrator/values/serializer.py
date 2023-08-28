from rest_framework.serializers import ModelSerializer
from .models import Value


class ValueSerializer(ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'
