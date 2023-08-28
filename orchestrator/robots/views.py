from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import RobotSerializer
from .models import Robot
from api.utils import token_login, check_id
from rest_framework.schemas import ManualSchema
from coreapi import Field

# Create your views here.


class RobotAPIView(APIView):
    """
    View to retrieve and edit information about robots.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    schema = ManualSchema(
        fields=[
            Field("robot_id", required=True, location="query",
                  description="ID of the robot."),
            Field("status", required=False, location="query",
                  description="Status of the robot."),
        ],
        description="Custom schema for TaskAPIView",
        encoding="application/json",
    )

    @token_login
    def get(self, request) -> Response:
        """
        Obtains information about a robot by its ID.

        Parameters:
        - request (HttpRequest): The incoming HTTP request.

        Returns:
        Response: HTTP response with the robot details.

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
        # validate_user(request.user, robot)
        serializer = RobotSerializer(instance=robot)
        return Response(data=serializer.data)

    @token_login
    def patch(self, request) -> Response:
        """
        Edits the state of a robot by its ID.

        Parameters:
        - request (HttpRequest): The incoming HTTP request.

        Returns:
        Response: HTTP response with the result of the editing operation.

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
        # validate_user(request.user, robot)
        serializer = RobotSerializer(instance=robot,
                                     data=request.query_params,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
