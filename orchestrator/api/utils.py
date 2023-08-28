from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from utils.choices import Status


def check_if_can_change_status(object) -> None or PermissionDenied:
    """
    Verifies if the object's state is in the list of invalid states.

    Args:
        object (type): The object whose state will be checked.

    Raises:
        PermissionDenied: If the object's state is in the list of invalid
        states.

    Returns:
        None or PermissionDenied: None if the state is valid,
        or a PermissionDenied exception if the state is invalid.
    """
    status = [Status.COMPLETED, Status.ERROR]
    if object.status in status:
        raise PermissionDenied(detail={
            'detail': f"You can't modify the object because is in {status}"
        })


def check_id(*args) -> None or ValidationError:
    """
    Verifies that the query_params are not empty.

    Args:
        *args: Variable arguments to verify.

    Raises:
        ValidationError: If any of the query_params is empty.

    Returns:
        None or ValidationError: None if the query_params are valid,
        or a ValidationError exception if any query_param is empty.
    """
    for id in args:
        if not id:
            raise ValidationError({
                'detail': 'Missing or invalid parameters'
            })


def token_login(function):
    """
    Decorator that updates the last_login field of the user making the request.

    This decorator can be applied to class-based views to automatically update
    the last_login field of the user every time a request is made to the
    decorated view.

    Args:
        function (callable): The view function to decorate.

    Returns:
        callable: A new function that wraps the original view function.
        This new function updates the last_login field of the user and then
        calls the original view function.
    """
    def wrapper(self, request):
        user = request.user
        user.last_login = timezone.now()
        user.save()
        return function(self, request)
    return wrapper
