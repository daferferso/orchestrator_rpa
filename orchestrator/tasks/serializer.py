from rest_framework.serializers import ModelSerializer
from .models import Task
from items.serializer import ItemSerializer


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskWithItemsSerializer(ModelSerializer):
    item_set = ItemSerializer(many=True)  # Serializador de Item anidado
    """
    Serializer for tasks with their associated items.

    This serializer is used to represent tasks along with the nested items
    in a specific format.

    The format returned is as follows:
    {
        "id": 1,
        "item_set": [
            {
                "id": 1,
                "value": {
                    "id": 1,
                    "name": "value1",
                    "value_number": "100.00",
                    "value_text": "",
                    "item_id": 1
                },
                "created_at": "2023-08-17T17:47:17.286670-04:00",
                "started_at": null,
                "ended_at": null,
                "observation": null,
                "status": "CREATED",
                "task_id": 1,
                "robot_id": 1
            }
        ],
        "created_at": "2023-08-17T17:00:38.019918-04:00",
        "started_at": null,
        "ended_at": null,
        "status": "CREATED",
        "user_id": 1,
        "process_id": 1,
        "robot_id": 1
    }

    Attributes:
        item_set (ItemSerializer): Serializer for nested items.

    Meta:
        model (Task): The model associated with the serializer.
        fields (tuple): Fields to include in the serialized representation.
    """
    class Meta:
        model = Task
        fields = '__all__'
