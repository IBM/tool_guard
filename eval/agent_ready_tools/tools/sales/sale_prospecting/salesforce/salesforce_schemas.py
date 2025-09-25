import enum
from typing import Any, Dict, List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class Asset:
    """Represents a single asset in Salesforce."""

    asset_id: str
    asset_name: str


@dataclass
class AssetStatus:
    """Represents the result of a asset status in Salesforce."""

    asset_status: str


@dataclass
class Campaign:
    """Represent the Campaign object in Salesforce."""

    campaign_id: str
    campaign_name: Optional[str] = None
    campaign_status: Optional[str] = None
    campaign_type: Optional[str] = None
    campaign_created_date: Optional[str] = None
    campaign_start_date: Optional[str] = None
    campaign_end_date: Optional[str] = None
    campaign_description: Optional[str] = None


@dataclass
class CampaignStatus:
    """Represents the Campaign status in Salesforce."""

    campaign_status: str


@dataclass
class CampaignType:
    """Represents the Campaign type in Salesforce."""

    campaign_type: str


@dataclass
class Contract:
    """Represents the Contract in Salesforce."""

    contract_id: str
    account_id: str
    start_date: str
    contract_number: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    contract_term: Optional[int] = None


@dataclass
class ErrorResponse:
    """Represent the Error Response in Salesforce."""

    message: Any
    payload: Any
    status_code: int


@dataclass
class Lead:
    """Represents Lead in Salesforce."""

    id: str  # Unique identifier of the Lead
    first_name: str  # First name of the Lead
    last_name: str  # Last name of the Lead
    email: str  # Contact email associated with the Lead
    company: str  # Company that the Lead works for
    description: str  # Contextual background or notes about the Lead
    title: Optional[str]  # Job title of the Lead ("CFO", "CEO", "Program Manager")
    industry: Optional[str]  # Industry the Lead works in (e.g., "Hospitality", "Energy", "Finance")
    annual_revenue: Optional[float]  # Revenue associated with the company the lead works for
    number_of_employees: Optional[float]  # Number of employees at lead's company
    city: Optional[str]  # City of the lead's business location
    state: Optional[str]  # State of the lead's business location
    country: Optional[str]  # Country of the lead's business location
    zip_code: Optional[str]  # Postal of the lead's business location
    rating: Optional[str]  # Likelihood of lead converting(e.g., "Hot", "Warm", "Cold")
    status: Optional[str]  # Stage in pipeline (e.g., "Open-Not Contacted", "Working-Contacted")
    additional_data: Optional[Dict[str, Any]] = None  # Optional columns passed to query


@dataclass
class LeadIndustry:
    """Represents the Lead industry in Salesforce."""

    lead_industry: str


@dataclass
class LeadStatus:
    """Represents the Lead status in Salesforce."""

    lead_status: str


@dataclass
class Opportunity:
    """Represents Opportunity in Salesforce."""

    id: Optional[str] = None  # Unique identifier of the Opportunity.
    account_id: Optional[str] = (
        None  # Unique Salesforce Account ID the Opportunity is associated with
    )
    name: Optional[str] = None  # Name of the Opportunity
    amount: Optional[float] = None  # Expected revenue if the Opportunity is won
    close_date: Optional[str] = None  # Expected or actual close date of the Opportunity
    stage_name: Optional[str] = (
        None  # The current phase of the Opportunity in the sales process (e.g. "Prospecting", "Closed Won")
    )
    probability: Optional[float] = None  # Likelihood that the Opportunity will close successfully
    description: Optional[str] = None  # Contextual background or notes about the Opportunity
    opportunity_type: Optional[str] = (
        None  # The type of Opportunity (e.g., "New Business", "Renewal")
    )
    lead_source: Optional[str] = None  # Source of the Opportunity (e.g., "Web", "Referral")
    age_in_days: Optional[int] = None  # Number of days since the Opportunity was created
    additional_data: Optional[Dict[str, Any]] = None  # Optional columns passed to query


@dataclass
class OrderItem:
    """Represents OrderItem in Salesforce."""

    id: str
    pricebook_entry_id: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    """Represents Order in Salesforce."""

    id: str
    status: str
    effective_date: str
    account_id: str
    contract_id: str
    order_number: Optional[str] = None
    order_amount: Optional[float] = None
    items: Optional[List[OrderItem]] = None


@dataclass
class OwnerExpirationNotice:
    """Represents Owner Expiration Notice in Salesforce."""

    value: str
    label: str
    active: bool


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
class Pricebook:
    """Represents Pricebook in Salesforce."""

    id: str
    name: str
    is_standard: Optional[bool] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class Pricebook2:
    """Represents a single price book from Salesforce."""

    id: str
    name: str
    is_active: Optional[bool] = None
    description: Optional[str] = None


@dataclass
class PricebookEntry:
    """Represents an available product and price in a specific Pricebook."""

    id: str
    product_id: str
    product_name: str
    unit_price: float


@dataclass
class PriceBookEntry:
    """Represents an available product and price in a specific PriceBook."""

    id: str
    product_id: str
    product_name: str
    unit_price: float


@dataclass
class Product2:
    """Represent the Solution object in Salesforce."""

    name: str
    id: str
    description: Optional[str] = None
    product_code: Optional[str] = None


@dataclass
class Status:
    """Represents Status in Salesforce."""

    value: str
    label: str
    active: bool
