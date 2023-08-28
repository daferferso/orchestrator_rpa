from django.test import TestCase
from .models import Task
from .views import TaskAPIView
from utils.choices import Status
from api.tests import setUp_Test_Case

# Create your tests here.


class TaskAPIViewTestCase(TestCase):
    """
    Test case for the TaskAPIView view.
    """

    def setUp(self):
        """
        Set up test data and environment.
        """
        setUp_Test_Case(self)

    def test_get_all_tasks_filter_by_robot_id(self):
        """
        Test retrieving all tasks filtered by robot_id.
        """
        url = '/tasks/'
        data = {'robot_id': self.robot.id}
        request = self.factory.get(url, data)
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = TaskAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_task(self):
        """
        Test editing a task's status.
        """
        url = '/tasks/'
        data = {
            'robot_id': self.robot.id,
            'task_id': self.task.id,
            'status': Status.COMPLETED
        }
        query_params = '?' + \
            '&'.join(f'{key}={value}' for key, value in data.items())
        request = self.factory.patch(url + query_params)
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = TaskAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(
            id=self.task.id).status, Status.COMPLETED)
