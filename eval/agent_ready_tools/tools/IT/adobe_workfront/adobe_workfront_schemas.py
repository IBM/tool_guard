from enum import StrEnum


class AdobeWorkfrontPriority(StrEnum):
    """Class containing the enumeration attributes in Adobe Workfront."""

    NONE = "0"
    LOW = "1"
    NORMAL = "2"
    HIGH = "3"
    URGENT = "4"


class AdobeWorkfrontProjectStatus(StrEnum):
    """Represent the types of project statuses in Adobe Workfront."""

    PLANNING = "PLN"
    IN_PROGRESS = "CUR"
    ON_HOLD = "ONH"
    COMPLETED = "CPL"
    CANCELLED = "DED"
    QUEUE = "QUE"


class AdobeWorkfrontTaskStatus(StrEnum):
    """Represent the types of task statuses in Adobe Workfront."""

    NEW = "NEW"
    IN_PROGRESS = "INP"
    ON_HOLD = "OHL"
    AWAITING_DEBRIEFING = "ADB"
    CANCELLED = "CAN"


class AdobeWorkfrontIssueStatus(StrEnum):
    """Represent the issue status types in Adobe Workfront."""

    NEW = "NEW"
    UNDER_REVIEW = "INP"
    AWAITING_FEEDBACK = "AWF"
    ON_HOLD = "ONH"
    COMPLETE = "CLS"
    REQUEST_DENIED = "RED"
