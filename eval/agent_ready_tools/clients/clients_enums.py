from enum import StrEnum


# TODO: deprecate: https://github.ibm.com/WatsonOrchestrate/wxo-domains/issues/3982
class AccessLevel(StrEnum):
    """Enum specifying the access/token type for the client."""

    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"


class AribaApplications(StrEnum):
    """
    Enum specifying the Ariba application (eg.

    Buyer, Invoice, Contract, etc).
    """

    BUYER = "BUYER"
    CONTRACT = "CONTRACT"
    INVOICE = "INVOICE"
    SUPPLIER = "SUPPLIER"


class DNBEntitlements(StrEnum):
    """Enum specifying the D&B entitlement."""

    SALES = "SALES"
    PROCUREMENT = "PROCUREMENT"
