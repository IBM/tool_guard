import enum
from typing import Any, Dict, Optional

from pydantic.dataclasses import dataclass


@dataclass
class Account:
    """Represents Account in Salesforce."""

    id: Optional[str] = None  # Unique Salesforce ID assigned to the account
    name: Optional[str] = (
        None  # The name of the company or organization associated with the account
    )
    industry: Optional[str] = None  # (e.g., "Hospitality", "Energy", "Finance")
    additional_data: Optional[Dict[str, Any]] = None  # Optional columns passed to query


@dataclass
class AccountType:
    """Represents the result of an account type in Salesforce."""

    account_type: str


@dataclass
class Case:
    """Represents a Case in Salesforce."""

    case_id: str
    case_name: str
    case_number: str
    owner_id: str
    account_id: Optional[str] = None
    created_date: Optional[str] = None


@dataclass
class CaseComment:
    """Represents a Case in Salesforce."""

    comment_id: str
    case_id: str
    comment: str
    comment_created_date: str
    published: bool


@dataclass
class CaseOrigin:
    """Represents the result of a case origin in Salesforce."""

    case_origin: str


@dataclass
class CasePriority:
    """Represents the result of a case priority in Salesforce."""

    case_priority: str


@dataclass
class CaseReason:
    """Represents the result of a case reason in Salesforce."""

    case_reason: str


@dataclass
class CaseStatus:
    """Represents a case status values in Salesforce."""

    case_status_id: str
    case_status_name: str
    sort_order: int
    created_date: str


@dataclass
class CaseTeam:
    """Represent the Case Team object in Salesforce."""

    team_template_id: str
    name: str
    created_date: str
    description: Optional[str] = None


@dataclass
class CaseTeamMember:
    """Represents a case team member from Salesforce."""

    case_team_member_id: str
    case_id: str
    member_id: str
    team_role_id: str
    create_date: Optional[str]
    created_by_id: Optional[str]


@dataclass
class CaseTeamRole:
    """Represents the Case team member role in Salesforce."""

    case_team_member_role_id: str
    case_team_member_role_name: str
    access_level: str
    created_date: str


@dataclass
class CaseTeamTemplate:
    """Represent the predefined case team in Salesforce."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@dataclass
class CaseType:
    """Represents the result of a case type in Salesforce."""

    case_type: str


@dataclass
class Contact:
    """Represents Contact in Salesforce."""

    id: Optional[str]  # Unique Salesforce ID assigned to the contact
    account_id: Optional[str] = None  # Unique Salesforce Account ID the contact is associated with
    name: Optional[str] = None  # Name of the contact
    email: Optional[str] = None  # Email address of the contact
    phone: Optional[str] = None  # Phone number of the contact
    title: Optional[str] = None  # Job title of the contact ("CFO", "CEO", "Program Manager")
    mobile_phone: Optional[str] = None  # Cell phone number of the contact
    additional_data: Optional[Dict[str, Any]] = None  # Optional columns passed to query


@dataclass
class Country:
    """Represents the country in Salesforce."""

    country_name: str
    country_code: str


@dataclass
class ErrorResponse:
    """Represent the Error Response in Salesforce."""

    message: Any
    payload: Any
    status_code: int


@dataclass
class FeedComment:
    """Represent the feed comment in Salesforce."""

    feed_comment_id: str
    comment: str
    feed_item_id: str
    parent_id: str
    is_rich_text: bool
    status: str
    created_by_id: str
    created_date: str


@dataclass
class Individual:
    """Represents Individual in Salesforce."""

    id: str
    name: str
    owner_id: Optional[str] = None


@dataclass
class PickListOptionsPair(enum.Enum):
    """Represents the picklist options pair in Salesforce."""

    AccountType = ("Account", "Type")
    LeadStatus = ("Lead", "Status")
    LeadIndustry = ("Lead", "Industry")
    CaseOrigin = ("Case", "Origin")
    CasePriority = ("Case", "Priority")
    CaseReason = ("Case", "Reason")
    CaseType = ("Case", "Type")
    CampaignStatus = ("Campaign", "Status")
    CampaignType = ("Campaign", "Type")
    Contact = ("Contact", "MailingStateCode")
    AssetStatus = ("Asset", "Status")
    Country = ("User", "CountryCode")

    obj_api_name: str
    field_api_name: str

    def __new__(cls, obj_api_name: str, field_api_name: str):
        """
        Creates a new instance of the enum.

        Args:
            obj_api_name: The API name of the object.
            field_api_name: The API name of the field.

        Returns:
            An instance of the enum.
        """
        obj = object.__new__(cls)
        obj._value_ = (obj_api_name, field_api_name)
        obj.obj_api_name = obj_api_name
        obj.field_api_name = field_api_name
        return obj


@dataclass
class PredefinedCaseTeamMember:
    """Represent the Predefined Case Team Member object in Salesforce."""

    id: str
    member_id: str
    created_date: str
    team_template_id: str


@dataclass
class Role:
    """Represents a single user role from Salesforce."""

    role_id: str
    role_name: str
    parent_role_id: Optional[str]
    developer_name: str
    forecast_user_id: Optional[str]


@dataclass
class State:
    """Represents the states associated with countries in Salesforce."""

    state: str
    valid_for: str


@dataclass
class Solution:
    """Represent the Solution object in Salesforce."""

    id: str
    name: str
    status: str
    description: str
    number: Optional[str] = None


@dataclass
class Task:
    """Represents all tasks in Salesforce."""

    task_id: str
    task_subject: Optional[str]
    task_status: Optional[str]
    task_priority: Optional[str]
    task_description: Optional[str]


@dataclass
class TaskPriority:
    """Represents a task priority in Salesforce."""

    task_priority: str


@dataclass
class TaskStatus:
    """Represents a task status in Salesforce."""

    task_status: str


@dataclass
class User:
    """Represents a single user from Salesforce."""

    user_id: str
    name: str
    alias: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    state: Optional[str] = None
