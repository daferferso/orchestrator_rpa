from django.urls import path
from robots.views import RobotAPIView
from tasks.views import TaskAPIView
from items.views import ItemAPIView

app_name = 'api'

urlpatterns = [
    path(r'robots', RobotAPIView.as_view(), name='robot'),
    path(r'tasks', TaskAPIView.as_view(), name='task'),
    path(r'items', ItemAPIView.as_view(), name='item'),
]
