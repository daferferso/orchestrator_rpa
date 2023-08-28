from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Robot
from items.utils import get_items_filtereds
from utils.choices import StatusRobot


def get_active_robots():
    """
    Obtains all robots with ACTIVE status.

    Returns:
        QuerySet: Set of robots with ACTIVE status.
    """
    robots = Robot.objects.filter(status=StatusRobot.ACTIVE)
    return robots


def get_min_robot():
    """
    Obtains the robot with the fewest items assigned to it.

    Returns:
        Robot: Robot object with the minimum number of assigned items.
    """
    robots = get_active_robots()
    if not robots:
        return None
    items_count = get_items_filtereds(robots)

    min_items_robot_id = min(items_count, key=lambda x: x['cantidad'])[
        'robot_id']

    robot = Robot.objects.get(id=min_items_robot_id)
    return robot


# UTILS PARA VERIFICAR ESTADO DE ROBOTS DESCONECTADOS Y ASIGNAR TAREAS A OTROS

def check_disconnected_robots():
    """
    Verifies robots that have been disconnected for more than 3 minutes.

    Returns:
        QuerySet: Set of disconnected robots.
    """
    status = StatusRobot.ACTIVE
    three = timezone.now() - timedelta(minutes=3)
    filter = Q(user_id__last_login__lt=three) & Q(status=status)
    robots = Robot.objects.filter(filter).prefetch_related('user_id')
    return robots


def assing_robots(queryset, robot):
    """
    Updates all robot_id values for each object in the queryset.

    Args:
        queryset (QuerySet): Set of objects to update.
        robot (Robot): Robot object to which the items/tasks will be assigned.
    """
    queryset.update(robot_id=robot)


def remove_robots(querysets: list):
    """
    Removes all robot_id assignments from each queryset.

    Args:
        querysets (list): List of object sets from which robot assignments
        will be removed.
    """

    for qs in querysets:
        qs.update(robot_id=None)


def change_status_inactive(robots):
    """
    Changes the status to INACTIVE for all robots.

    Args:
        robots (QuerySet): Set of Robot objects for which the status
        will be changed to INACTIVE.
    """
    robots.update(status=StatusRobot.INACTIVE)
