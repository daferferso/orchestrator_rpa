"""
WSGI config for orchestrator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from items.tasks import get_items_first_time_run_server

# ###### First-time Execution ####################

"""
This section contains code that is executed when the application
runs for the first time.

It is used to get items unassigned.

This code block is executed only once during the initial launch
of the application.
"""

get_items_first_time_run_server()

# ##################################################


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orchestrator.settings')

application = get_wsgi_application()
