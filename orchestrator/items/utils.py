from django.db.models import Q, Count
from datetime import datetime
from items.models import Item
from utils.choices import Status


def get_items(robots=None):
    """
    Retrieves items from robots in CREATED or STARTED states.

    Args:
        robots (List[Robot], optional): List of Robot objects.
        If provided, items assigned to the specified robots will be filtered.

    Returns:
        QuerySet: List of Item objects that meet the filtering criteria.
    """
    status = [Status.CREATED, Status.STARTED]
    filter_status = Q(status__in=status)
    filter_robots = Q(robot_id__in=robots)
    if robots:
        filter = filter_status & filter_robots
    else:
        filter = filter_status
    items = Item.objects.filter(filter)
    return items


def get_items_filtereds(robots):
    """
    Obtains the count of items assigned to each robot.

    This function returns a list with the count of items assigned
    to each robot for the current day and in the CREATED or STARTED states.

    Args:
        robots (List[Robot]): List of Robot objects for which
        the count will be obtained.

    Returns:
        List[dict]: List of dictionaries with the item count for
        each robot. Each dictionary has keys 'robot_id' and 'cantidad'.
    """
    now = datetime.now().date()
    status = [Status.CREATED, Status.STARTED]

    items_count = Item.objects.filter(
        created_at__date=now,
        status__in=status,
        robot_id__in=robots
    ).values('robot_id').annotate(cantidad=Count('id'))
    robots_with_counts = {
        robot['robot_id']: robot['cantidad'] for robot in items_count
    }

    result = [{'robot_id': robot.id, 'cantidad': robots_with_counts.get(
        robot.id, 0)} for robot in robots]
    return result
