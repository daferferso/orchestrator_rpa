import csv
from .models import Task
from items.models import Item
from values.models import Value
from robots.utils import get_min_robot


def get_tasks_from_items(items):
    """
    Obtains unique tasks from a list of items.

    Parameters:
    - items (QuerySet): Set of items.

    Returns:
    QuerySet: Set of unique tasks related to the provided items.
    """
    unique_task_ids = items.values_list('task_id', flat=True).distinct()
    unique_tasks = Task.objects.filter(id__in=unique_task_ids)
    return unique_tasks


def read_file(file, user, process):
    """
    Reads a CSV file and creates Item and Value objects in the database.

    Parameters:
    - file (File): The CSV file to be read.
    - user (User): The user associated with the task.
    - process (Process): The process associated with the task.

    Returns:
    bool: True if the operation was successful,
          False if a robot couldn't be assigned.
    """
    robot = get_min_robot()
    task = Task.objects.create(user_id=user, process_id=process,
                               robot_id=robot)
    # Read the CSV file using DictReader
    csv_reader = csv.DictReader(file.read().decode('utf-8').splitlines())

    # List to store Item and Value objects to create
    items_to_create = []
    values_to_create = []

    # Iterate over the rows of the CSV file and add to the list
    for row in csv_reader:
        try:
            item = Item(
                task_id=task,
                robot_id=robot,
                )
            value = Value(
                item_id=item,
                value_number=row.get('linea'),
                value_text=row.get('valor'),
                name=row.get('field'),
            )
        except Exception:
            continue
        else:
            items_to_create.append(item)
            values_to_create.append(value)

    # Insert the objects into the database using bulk_create
    Item.objects.bulk_create(items_to_create)
    Value.objects.bulk_create(values_to_create)
    if not robot:
        return False
    return True
