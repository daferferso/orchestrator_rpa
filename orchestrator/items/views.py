from typing import Any, Dict
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from robots.models import Robot
from items.models import Item
from tasks.models import Task
from .serializer import ItemSerializer
from api.utils import token_login, check_id, check_if_can_change_status
from rest_framework.schemas import ManualSchema
from coreapi import Field

# Create your views here.


class ItemAPIView(APIView):
    """
    View to edit the state of an item.

    This view allows editing the state of an item using the 'robot_id'
    and 'item_id' parameters.

    Attributes:
        authentication_classes (list): List of authentication classes
        applied to the view.
        permission_classes (list): List of permission classes applied
        to the view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    schema = ManualSchema(
        fields=[
            Field("robot_id", required=True, location="query",
                  description="ID of the robot."),
            Field("status", required=False, location="query",
                  description="New status of the task."),
            Field("item__started_at", required=False, location="query",
                  description="Start datetime (format: YYYY-MM-DD HH:MM:SS)."),
            Field("item__ended_at", required=False, location="query",
                  description="End datetime (format: YYYY-MM-DD HH:MM:SS)."),
            Field("item__observation", required=False, location="query",
                  description="Observation of the item."),
            # Include other fields of Item as needed
        ],
        description="Custom schema for TaskAPIView",
        encoding="application/json",
    )

    @token_login
    def patch(self, request):
        """
        Edits the state of an item using the parameters 'robot_id'
        and 'item_id'.

        Parameters:
        - robot_id (int): ID of the robot associated with the item.
        - item_id (int): ID of the item to be edited.
        - status (str): Status of the item to be edited.

        Returns:
        Response: HTTP response with the result of the operation.

        Authentication:
        - Bearer Token:
            A valid API token should be provided in the 'Authorization' header.
            Example: Authorization: Token XXXX-XXXX-XXXX-XXXX
        """
        robot_id = request.query_params.get('robot_id')
        item_id = request.query_params.get('item_id')
        check_id(robot_id, item_id)
        try:
            Robot.objects.get(id=robot_id)
            item = Item.objects.get(id=item_id)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        check_if_can_change_status(item)
        serializer = ItemSerializer(instance=item, data=request.query_params,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)


class ItemListView(LoginRequiredMixin, ListView):
    """
    View to display the list of items associated with a task.
    """
    login_url = 'login'
    template_name = 'home/items.html'

    def dispatch(self, request, *args: Any, **kwargs: Any):
        """
        Verifies if the user has permissions to access the view.

        Parameters:
        - request (HttpRequest): The incoming HTTP request.
        - args: Positional arguments.
        - kwargs: Keyword arguments.

        Returns:
        HttpResponse: HTTP response that redirects to the tasks page
        or allows access to the view.
        """
        task_id = self.kwargs['task_id']
        self.task = get_object_or_404(Task, id=task_id)
        if request.user != self.task.user_id:
            return redirect(reverse('tasks'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        """
    Obtains the set of items associated with the task.

    Returns:
    QuerySet: Set of items filtered by the task and sorted by ID
    in descending order.
    """
        return Item.objects.filter(task_id=self.task).order_by("-id")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Obtains the context data for the template.

        Returns:
        dict: Dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        context['segment'] = 'items'
        return context
