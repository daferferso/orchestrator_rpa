from django.db.models import TextChoices


class Status(TextChoices):
    """
    Definition of status options for tasks.
    """
    CREATED = 'CREATED'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'


class StatusRobot(TextChoices):
    """
    Definition of status options for robots.
    """
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class Platform(TextChoices):
    """
    Definition of platform options for automation.
    """
    UIPATH = 'UIPATH'
    AUTOMATION_ANYWHERE = 'AUTOMATION_ANYWHERE'
    BLUEPRISM = 'BLUEPRISM'
    POWER_AUTOMATE = 'POWER_AUTOMATE'
    PYTHON = 'PYTHON'
    OTHER = 'OTHER'
