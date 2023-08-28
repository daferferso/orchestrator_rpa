from django.db.models.query import QuerySet


class Memory:
    """
    Singleton class representing the system's memory
    to store items and tasks pending for assignment.
    """
    def __init__(self):
        """
        Initializes the memory with empty QuerySet sets for items and tasks.
        """
        self.items = QuerySet().none()
        self.tasks = QuerySet().none()

    def clear(self):
        """
        Clears the memory by emptying the sets of items and tasks.
        """
        self.items = self.items.none()
        self.tasks = self.tasks.none()


# Singleton pattern
memory_instance = Memory()


def get_memory():
    """
    Obtains the unique instance of the system's memory.

    Returns:
    Memory: Unique instance of the Memory class.
    """
    return memory_instance
