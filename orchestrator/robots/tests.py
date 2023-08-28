from django.test import TestCase
from .models import Robot
from .views import RobotAPIView
from utils.choices import StatusRobot
from api.tests import setUp_Test_Case

# Create your tests here.


class RobotAPIViewTestCase(TestCase):
    """
    Test case for the RobotAPIView.

    This test case includes tests for getting and patching robot information.

    Inherits from:
        TestCase
    """

    def setUp(self):
        """
        Set up the test environment.

        This method is executed before each test.
        """
        setUp_Test_Case(self)

    def test_get_robot(self):
        """
        Test getting robot information.

        It sends a GET request with a valid robot_id and asserts
        the response status code and data.
        """
        url = '/robots/'
        data = {'robot_id': self.robot.id}
        request = self.factory.get(url, data)
        request.user = self.user
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = RobotAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['ip_address'], '0.0.0.0')

    def test_get_robot_invalid_id(self):
        """
        Test getting robot information with an invalid robot_id.

        It sends a GET request with an invalid robot_id and asserts
        the response status code.
        """
        url = '/robots/'
        data = {'robot_id': 999}  # ID no existente
        request = self.factory.get(url, data)
        request.user = self.user
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = RobotAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_get_robot_bad_request(self):
        """
        Test getting robot information with bad request data.

        It sends a GET request with missing or invalid data
        and asserts the response status code.
        """
        url = '/robots/'
        data = {'robot_id': ''}  # ID inválido
        request = self.factory.get(url, data)
        request.user = self.user
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = RobotAPIView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_patch_robot(self):
        """
        Test patching robot status.

        It sends a PATCH request to update the robot's status
        and asserts the response status code and updated status.
        """
        url = '/robots/'
        data = {
            'robot_id': self.robot.id,
            'status': StatusRobot.INACTIVE
        }
        query_params = '?' + \
            '&'.join(f'{key}={value}' for key, value in data.items())
        request = self.factory.patch(url + query_params)
        request.user = self.user
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = RobotAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Robot.objects.get(
            id=self.robot.id).status, StatusRobot.INACTIVE)
