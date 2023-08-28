from items.utils import get_items
from orchestrator.memory_manager import get_memory


def get_items_first_time_run_server():
    """
    Retrieves unassigned items in case of server start or restart.

    This function is used to obtain items that have not been assigned
    to any robot when the server starts or restarts.
    It updates the list of unassigned items in the memory object.

    Returns:
        None
    """
    memory = get_memory()
    memory.items = get_items(robots=None).all()
