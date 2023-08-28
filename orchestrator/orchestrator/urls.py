"""
URL configuration for orchestrator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from .views import login_view, logout_view
from tasks.views import DashboardListView
from items.views import ItemListView

urlpatterns = [
    path(r'', DashboardListView.as_view(), name='tasks'),
    path(r'login/', login_view, name='login'),
    path(r'logout/', logout_view, name="logout"),
    path(r'admin/', admin.site.urls),
    path(r'tareas/<int:task_id>', ItemListView.as_view(), name='items'),
    path(r'docs', include_docs_urls(title='API Documentation')),
    path(r'api/', include('api.urls')),
]
