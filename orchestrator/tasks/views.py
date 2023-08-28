# from django.shortcuts import render
from typing import Any, Dict
from django.shortcuts import redirect, get_object_or_404
from django.db.models.query import QuerySet
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas import ManualSchema
from django.contrib.auth.mixins import LoginRequiredMixin
from coreapi import Field
from .utils import read_file
from .serializer import TaskSerializer, TaskWithItemsSerializer
from .models import Task
from robots.models import Robot
from items.models import Item
from processes.models import Process
from api.utils import token_login, check_id, check_if_can_change_status
from utils.choices import Status
# from robots.tasks import periodic_task_check

# Create your views here.


class TaskAPIView(APIView):
    """
    View for retrieving and editing task information.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    schema = ManualSchema(
        fields=[
            Field("robot_id", required=True, location="query",
                  description="ID of the robot."),
            Field("task_id", required=False, location="query",
                  description="ID of the task."),
            Field("status", required=False, location="query",
                  description="New status of the task."),
            Field("started_at", required=False, location="query",
                  description="Start datetime (format: YYYY-MM-DD HH:MM:SS)."),
            Field("ended_at", required=False, location="query",
                  description="End datetime (format: YYYY-MM-DD HH:MM:SS)."),
        ],
        description="Custom schema for TaskAPIView",
        encoding="application/json",
    )

    @token_login
    def get(self, request) -> Response:
        """
        Retrieves all tasks filtered by robot_id.

        Parameters:
        - robot_id (query parameter): ID of the robot.

        Response:
        - 200 OK: List of tasks with associated items.
        - 404 NOT FOUND: If the robot does not exist.

        Authentication:
        - Bearer Token:
            A valid API token should be provided in the 'Authorization' header.
            Example: Authorization: Token XXXX-XXXX-XXXX-XXXX
        """
        id = request.query_params.get('robot_id')
        check_id(id)
        try:
            robot = Robot.objects.get(id=id)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tasks_with_items = Task.objects.filter(
            robot_id=robot.id,
            status__in=[Status.CREATED, Status.STARTED]
        ).prefetch_related('item_set').all()
        serializer = TaskWithItemsSerializer(tasks_with_items,
                                             many=True)
        return Response(data=serializer.data)

    @token_login
    def patch(self, request):
        """
        Edits a task.

        This method requires the following query parameters:
        - robot_id (query parameter): ID of the robot.
        - task_id (query parameter): ID of the task.
        - status (query parameter): New status of the task.

        Responses:
        - 200 OK: The task is successfully edited.
        - 404 NOT FOUND: If the robot or the task does not exist.
        """
        robot_id = request.query_params.get('robot_id')
        task_id = request.query_params.get('task_id')
        check_id(robot_id, task_id)
        try:
            Robot.objects.get(id=robot_id)
            task = Task.objects.get(id=task_id)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        check_if_can_change_status(task)
        serializer = TaskSerializer(instance=task, data=request.query_params,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)


class DashboardListView(LoginRequiredMixin, ListView):
    """
    View for the user's dashboard list.

    This view displays a list of tasks associated with the user,
    along with relevant information about the state of tasks,
    items, and available robots.

    Requires the user to be authenticated.

    Attributes:
    - login_url (str): Redirect URL for login.
    - template_name (str): Name of the HTML template to render.
    - paginate_by (int): Number of tasks per page in pagination.
    """
    login_url = 'login'
    template_name = 'home/tasks.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """
        Gets the set of tasks associated with the user
        and orders them by ID in descending order.

        Returns:
        QuerySet: Set of tasks associated with the user.
        """
        user = self.request.user
        paginate_by = int(self.request.GET.get('paginate_by',
                                               self.paginate_by))
        self.paginate_by = paginate_by
        return Task.objects.filter(user_id=user).order_by("-id")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Gets the context data for the template.

        Returns:
        Dict[str, Any]: Context data for the template.
        """
        total_items = Item.objects.filter(
            task_id__user_id=self.request.user).count()
        available_robots = Robot.objects.filter(status='ACTIVE').count()
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context["available_robots"] = available_robots
        context['segment'] = 'tasks'
        context['processes'] = Process.objects.all()
        context['total_items'] = total_items
        return context

    # def post(self, *args, **kwargs):
    #     """
    #     Processes a POST request to create a new task.

    #     This function handles the upload of a CSV file, creates a new task
    #     associated with the user and the selected process,
    #     and assigns a robot to the task
    #     if possible. If no robots are available, it enables
    #     the task to check robots.

    #     Returns:
    #     HttpResponse: Redirects to the tasks page after processing.
    #     """
    #     if self.request.method == 'POST':
    #         # Implementar el List para seleccionar el proceso #
    #         process_id = self.request.POST['process_id']
    #         process = get_object_or_404(Process, id=process_id)
    #         file = self.request.FILES['formFile']
    #         assigned_robot = read_file(file, self.request.user, process)
    #         if not assigned_robot:
    #             periodic_task_check.enabled = True
    #             periodic_task_check.save()
    #         return redirect('tasks')
