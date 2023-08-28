# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from tasks.utils import get_tasks_from_items
# from items.utils import get_items
# from robots.utils import (check_disconnected_robots, change_status_inactive,
#                           assing_robots, get_min_robot, get_active_robots,
#                           remove_robots)
# from orchestrator.celery import app
# from orchestrator.memory_manager import get_memory


# # CREATING THE TASK: handle_disconnected_robots
# # Create or get an interval schedule to run the task every 1 minute
# schedule_handle, created_handle = IntervalSchedule.objects.get_or_create(
#     every=3,
#     period=IntervalSchedule.MINUTES,
# )

# # Try to get an existing periodic task or create a new one
# try:
#     periodic_task_handle = PeriodicTask.objects.get(
#         name='handle_disconnected_robots')
# except PeriodicTask.DoesNotExist:
#     # If the task doesn't exist, create it
#     periodic_task_handle = PeriodicTask.objects.create(
#         interval=schedule_handle,
#         name='handle_disconnected_robots',
#         task='robots.tasks.handle_disconnected_robots',
#         enabled=True,
#     )


# @app.task
# def handle_disconnected_robots():
#     """
#     Celery task to handle disconnected robots.

#     This task is scheduled to run periodically and performs
#     the following actions:
#     1. Searches for disconnected robots.
#     2. Changes the state of disconnected robots to inactive.
#     3. Retrieves items associated with disconnected robots and their
#        corresponding tasks.
#     4. Removes robot assignments from items and tasks.
#     5. Checks if there are active robots. If there are no active robots,
#        enables the periodic task for robot verification.

#     Returns:
#     None
#     """
#     robots_disconnecteds = check_disconnected_robots()

#     if robots_disconnecteds:
#         change_status_inactive(robots_disconnecteds)
#         items = get_items(robots_disconnecteds).all()
#         if items:
#             tasks = get_tasks_from_items(items)
#             remove_robots([items, tasks])
#             items = items.none()
#             tasks = tasks.none()
#     robots_active = get_active_robots()
#     if not robots_active:
#         periodic_task_check.enabled = True
#         periodic_task_check.save()


# # CREATING THE TASK: check_robots_every_minute

# # Define the interval schedule for the periodic task
# schedule_check, created_check = IntervalSchedule.objects.get_or_create(
#     every=1,
#     period=IntervalSchedule.MINUTES,
# )

# # Try to retrieve the existing periodic task or create a new one
# try:
#     periodic_task_check = PeriodicTask.objects.get(
#         name='check_robots_every_minute')
# except PeriodicTask.DoesNotExist:
#     # Create a new periodic task with the defined interval and settings
#     periodic_task_check = PeriodicTask.objects.create(
#         interval=schedule_check,
#         name='check_robots_every_minute',
#         task='robots.tasks.check_robots_every_minute',
#         enabled=False,  # Disable the task initially
#     )


# @app.task
# def check_robots_every_minute():
#     """
#     Celery task to check robots every minute.

#     This task is scheduled to run periodically and performs the following
#     actions:
#     1. If the task to handle disconnected robots is enabled, it disables
#        it and logs a message.
#     2. Searches for active robots.
#     3. If there are active robots, it checks if the memory has unassigned
#        items.
#     4. If the memory has unassigned items, it assigns the items and tasks
#        to a robot and clears the memory.
#     5. Disables the task to check active robots and enables the task to handle
#        disconnected robots.
#     6. If there are no active robots, enables the task to check disconnected
#        robots.

#     Returns:
#     None
#     """
#     if periodic_task_handle.enabled:
#         periodic_task_handle.enabled = False
#         periodic_task_handle.save()
#     memory = get_memory()
#     robots = get_active_robots()
#     if robots:
#         if not memory.items.exists():
#             memory.items = get_items(robots=None).all()
#             if memory.items.exists():
#                 robot = get_min_robot()
#                 memory.task = get_tasks_from_items(memory.items).all()
#                 assing_robots(memory.items, robot)
#                 assing_robots(memory.task, robot)
#                 memory.clear()
#             periodic_task_check.enabled = False
#             periodic_task_handle.enabled = True
#             periodic_task_handle.save()
#             periodic_task_check.enabled = False
#             periodic_task_check.save()
