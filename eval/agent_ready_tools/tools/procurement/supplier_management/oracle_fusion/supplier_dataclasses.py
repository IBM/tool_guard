from enum import StrEnum
from typing import ClassVar, Dict, Optional

from pydantic.dataclasses import dataclass


class OracleFusionBusinessRelationship(StrEnum):
    """The nature of the business relationship in Oracle Fusion."""

    PROSPECTIVE = "Prospective"
    SPEND_AUTHORIZED = "Spend Authorized"


class OracleFusionTaxOrganizationType(StrEnum):
    """The type of Supplier's Tax Organization in Oracle Fusion."""

    CORPORATION = "Corporation"
    FOREIGN_CORPORATION = "Foreign Corporation"
    FOREIGN_GOVERNMENT_AGENCY = "Foreign Government Agency"
    FOREIGN_INDIVIDUAL = "Foreign Individual"
    FOREIGN_PARTNERSHIP = "Foreign Partnership"
    GOVERNMENT_AGENCY = "Government Agency"
    INDIVIDUAL = "Individual"
    PARTNERSHIP = "Partnership"


@dataclass
class OracleFusionSupplierDetails:
    """
    Represents a supplier detail-s in Oracle Fusion:

    ID = SupplierID,
    Name = Supplier,
    Supplier type code = SupplierTypeCode,
    Status = status,
    Creation date = CreationDate.
    """

    supplier_id: int
    supplier_name: Optional[str]
    supplier_type_code: Optional[str]
    supplier_status: Optional[str]
    supplier_creation_date: Optional[str]


@dataclass
class OracleFusionAddressPurposeMap:
    """
    Maps human-readable address purposes to Oracle Fusion field flags.

    Example:
        "ordering"    → "AddressPurposeOrderingFlag"
        "remit_to"    → "AddressPurposeRemitToFlag"
        "rfq_or_bidding" → "AddressPurposeRFQOrBiddingFlag"
        "payment"     → "AddressPurposePaymentFlag"
        "procurement" → "AddressPurposeProcurementFlag"
    """

    PURPOSES = {
        "ordering": "address_purpose_ordering_flag",
        "remit_to": "address_purpose_remit_to_flag",
        "rfq_or_bidding": "address_purpose_rfq_or_bidding_flag",
        "payment": "address_purpose_payment_flag",
        "procurement": "address_purpose_procurement_flag",
    }


@dataclass
class OracleFusionSupplierAddress:
    """
    Represents a supplier address in Oracle Fusion.

    This dataclass captures all necessary fields required to create a supplier address, including
    address details, contact information, and purpose flags. It also includes a static field map
    (`FIELD_NAME_MAP`) for mapping internal field names to Oracle Fusion API's expected field names.
    """

    address_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: Optional[str]
    country_code: str
    country: Optional[str]
    postal_code: str
    email: str

    address_purpose_ordering_flag: Optional[bool] = None
    address_purpose_remit_to_flag: Optional[bool] = None
    address_purpose_rfq_or_bidding_flag: Optional[bool] = None
    address_purpose_payment_flag: Optional[bool] = None
    address_purpose_procurement_flag: Optional[bool] = None

    FIELD_NAME_MAP: ClassVar[Dict[str, str]] = {
        "address_name": "AddressName",
        "address_line1": "AddressLine1",
        "address_line2": "AddressLine2",
        "city": "City",
        "state": "State",
        "country_code": "CountryCode",
        "country": "Country",
        "postal_code": "PostalCode",
        "email": "Email",
        "address_purpose_ordering_flag": "AddressPurposeOrderingFlag",
        "address_purpose_remit_to_flag": "AddressPurposeRemitToFlag",
        "address_purpose_rfq_or_bidding_flag": "AddressPurposeRfqOrBiddingFlag",
        "address_purpose_payment_flag": "AddressPurposePaymentFlag",
        "address_purpose_procurement_flag": "AddressPurposeProcurementFlag",
    }


@dataclass
class OracleFusionCreateSupplierAddressResult:
    """
    Represents the result of a successful supplier address creation in Oracle Fusion.

    Includes the supplier ID, the newly created address ID (if available), and the full raw response
    payload returned by the Oracle Fusion API.
    """

    supplier_id: str
    address_id: Optional[str] = None
    raw_response: Optional[Dict] = None


class OracleFusionAddressPurposeType(StrEnum):
    """Represents the address purpose type in Oracle Fusion."""

    ORDERING = "ordering"
    REMIT_TO = "remit_to"
    RFQ_OR_BIDDING = "rfq_or_bidding"
    PAYMENT = "payment"
    PROCUREMENT = "procurement"


@dataclass
class OracleFusionUpdateSupplierAddress:
    """Represents a partial update payload for a supplier address in Oracle Fusion."""

    address_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country_code: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    email: Optional[str] = None
    ordering: Optional[bool] = None
    remit_to: Optional[bool] = None
    # Add other optional purpose flags as needed

    FIELD_NAME_MAP = {
        "address_name": "AddressName",
        "address_line1": "AddressLine1",
        "address_line2": "AddressLine2",
        "city": "City",
        "state": "State",
        "country_code": "CountryCode",
        "country": "Country",
        "postal_code": "PostalCode",
        "email": "Email",
        "address_purpose_ordering_flag": "AddressPurposeOrderingFlag",
        "address_purpose_remit_to_flag": "AddressPurposeRemitToFlag",
        "address_purpose_rfq_or_bidding_flag": "AddressPurposeRfqOrBiddingFlag",
        "address_purpose_payment_flag": "AddressPurposePaymentFlag",
        "address_purpose_procurement_flag": "AddressPurposeProcurementFlag",
    }


@dataclass
class OracleFusionUpdateSupplierAddressResult:
    """Represents the result of updating supplier address details in Oracle Fusion."""

    supplier_id: str
    address_id: str
    raw_response: Dict


@dataclass
class OracleFusionSupplierTaxRegistrations:
    """Represents tax registration data of a supplier in Oracle Fusion."""

    tax_regime_code: Optional[str]
    registration_number: Optional[str]
    tax: Optional[str]
    tax_jurisdiction_code: Optional[str]
    tax_point_basis: Optional[str]
    registration_type: Optional[str]
    status: Optional[str]
    reason: Optional[str]
    effective_from: Optional[str]
    registration_id: Optional[int]


@dataclass
class OracleFusionSupplierContactDetails:
    """Represents the supplier's contacts details from Oracle Fusion."""

    supplier_contact_id: int
    first_name: str
    last_name: str
    phone_country_code: Optional[str]
    phone_area_code: Optional[str]
    phone_number: Optional[str]
    mobile_country_code: Optional[str]
    mobile_area_code: Optional[str]
    mobile_number: Optional[str]
    email: Optional[str]


@dataclass
class OracleFusionSupplierAddressHeader:
    """Represents the list of supplier's address details from Oracle Fusion."""

    address_id: int
    country: str
    address_name: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    county: Optional[str]
    province: Optional[str]


@dataclass
class OracleFusionSupplierIncomeTaxData:
    """Represents a supplier income tax data in Oracle Fusion."""

    supplier: str
    tax_organization_type: Optional[str]
    registry_id: Optional[str]
    tax_registration_country: Optional[str]
    tax_registration_number: Optional[str]
    tax_payer_country: Optional[str]
    tax_payer_id: Optional[str]
    federal_income_tax_type_code: Optional[str]
    federal_income_tax_type: Optional[str]
    tax_reporting_name: Optional[str]
    withholding_tax_group: Optional[str]


@dataclass
class OracleFusionUpdateSupplierResponse:
    """Represents a update supplier response in Oracle Fusion."""

    supplier_name: str


@dataclass
class OracleFusionSupplierSiteHeaders:
    """Represents the list of supplier's sites from Oracle Fusion."""

    site_id: int
    site_name: str
    procurement_business_unit: str
    address_name: str


@dataclass
class OracleFusionUpdateTaxRegistrationResponse:
    """Represents a update supplier tax registration response in Oracle Fusion."""

    tax_point_basis: Optional[str]
    registration_type_code: Optional[str]
    registration_status_code: Optional[str]
    registration_reason_code: Optional[str]
    registration_source_code: Optional[str]
    rounding_rule_code: Optional[str]
    tax_authority_id: Optional[int]
    legal_location_id: Optional[int]


class OracleFusionRegistrationStatus(StrEnum):
    """Represent the registration status in Oracle Fusion."""

    AGENT = "AGENT"
    NOT_REGISTERED = "NOT REGISTERED"
    REDUCED_TDS = "REDUCED TDS"
    REGISTERED = "REGISTERED"
    REGISTERED_IN_EU_NON_UNITED_KINGDOM = "EC_REG(NON GB)"
    REGISTERED_IN_EU_NON_FRANCE = "EC_REG(NON FR)"
    REGISTERED_IN_EU_NON_UK = "A1_ORACLE12.0.0_EC_REG"
    REGISTERED_IN_EU_NON_UK_1 = "A1_EBTAX_EC_REG"


class OracleFusionTaxRegistrationType(StrEnum):
    """Represent the tax registration type in Oracle Fusion."""

    CPF = "CPF"
    CUIL = "CUIL"
    CUIT = "CUIT"
    DNI = "DNI"
    NATIONAL_CODE_FOR_JURIDICAL_PERSON = "CNPJ"
    OTHERS = "OTHERS"
    TAX_IDENTIFICATION_NUMBER = "NIT"
    VAT = "VAT"


@dataclass
class OracleFusionTaxAuthorities:
    """Represents a supplier tax authority details in Oracle Fusion."""

    tax_authority_id: int
    tax_authority_name: str


@dataclass
class OracleFusionLegalLocations:
    """Represents a supplier legal location details in Oracle Fusion."""

    location_id: int
    address: str
