from enum import StrEnum

from pydantic.dataclasses import dataclass


@dataclass
class TicketPriority(StrEnum):
    """Respresents the list of values for ticket priorities in Zendesk."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class TicketType(StrEnum):
    """Respresents the list of values for ticket types in Zendesk."""

    QUESTION = "Question"
    INCIDENT = "Incident"
    PROBLEM = "Problem"
    TASK = "Task"


@dataclass
class TicketComponent(StrEnum):
    """Respresents the list of values for ticket priorities in Zendesk."""

    CORE_ITEM = "Core Item"
    ACCESSORIES = "Accessories"
    WARRANTIES = "Warranties"


class ZendeskModules(StrEnum):
    """The name of the module in Zendesk."""

    USERS = "users"
    TICKETS = "tickets"
    ORGANIZATIONS = "organizations"


class CustomObjectDefaultFields:
    """Class containing the constant attributes in Zendesk."""

    NAME = "name"
    EXTERNAL_ID = "external_id"
    CUSTOM_OBJECT_RECORD = "custom_object_record"
    CUSTOM_OBJECT_FIELDS = "custom_object_fields"


@dataclass
class ZendeskRole(StrEnum):
    """Respresents the list of values for user roles in Zendesk."""

    ADMIN = "admin"
    ADVISOR = "advisor"
    AGENT = "agent"
    CONTRIBUTOR = "contributor"
    END_USER = "end-user"
    LIGHT_AGENT = "light agent"
