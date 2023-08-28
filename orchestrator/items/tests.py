from django.test import TestCase
from rest_framework import status
from items.models import Item
from .views import ItemAPIView
from utils.choices import Status
from api.tests import setUp_Test_Case

# Create your tests here.


class ItemAPIViewTestCase(TestCase):
    """
    Test case for the ItemAPIView class-based view.

    This test case checks the behavior of the patch_item_status method
    which updates the status of an item using the ItemAPIView view.

    Attributes:
        See individual test methods for attributes.
    """

    def setUp(self):
        """
        Set up the test case by creating necessary objects and data.
        """
        setUp_Test_Case(self)

    def test_patch_item_status(self):
        """
        Test the patch_item_status method.

        This test sends a PATCH request to the ItemAPIView view
        with updated item status.
        It checks if the status is updated correctly and if the response
        status code is 200 OK.
        """
        url = '/items/'
        data = {
            'robot_id': self.robot.id,
            'item_id': self.item.id,
            'status': 'COMPLETED'
        }
        query_params = '?' + \
            '&'.join(f'{key}={value}' for key, value in data.items())
        request = self.factory.patch(url + query_params)
        # Token Auth para el header
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = ItemAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(
            id=self.item.id).status, Status.COMPLETED)
