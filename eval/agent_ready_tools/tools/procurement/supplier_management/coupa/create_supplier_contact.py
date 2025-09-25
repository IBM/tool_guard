from typing import Dict, Iterable, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    ContactPurposeType,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaCreateSupplierContactResponse:
    """Represents the result of creating a supplier contact in Coupa."""

    supplier_id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_supplier_contact(
    supplier_id: int,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    country_code: Optional[str] = None,
    area_code: Optional[str] = None,
    phone_number: Optional[str] = None,
    purpose: Optional[Union[Iterable[ContactPurposeType] | ContactPurposeType]] = None,
) -> ToolResponse[CoupaCreateSupplierContactResponse]:
    """
    Creates contact for a supplier in coupa.

    Args:
        supplier_id: The id of the supplier, returned from get_all_suppliers tool.
        email: The contact's email address.
        first_name: The contact's first name
        last_name: The contact's last name.
        country_code: The country code of the phone number.
        area_code: The area code of the phone number.
        phone_number: The phone number of the contact.
        purpose: The purpose of the contact.

    Returns:
        Result from creating a supplier contact.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    if purpose is None:
        purposes: List[ContactPurposeType] = []
    else:
        purposes = list([purpose] if isinstance(purpose, str) else purpose)

    purposes_list: List[Dict[str, str]] = [{"name": name} for name in purposes]

    phone_work = {
        "country-code": country_code,
        "area-code": area_code,
        "number": phone_number,
    }

    phone_work = {key: value for key, value in phone_work.items() if value}

    payload = {
        "contacts": [
            {
                "email": email,
                "name-given": first_name,
                "name-family": last_name,
                "phone-work": phone_work,
                "purposes": purposes_list,
            }
        ]
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.put_request(
        resource_name=f"suppliers/{supplier_id}",
        payload=payload,
        params={"fields": '["id"]'},
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier contact created",
        content=CoupaCreateSupplierContactResponse(supplier_id=response.get("id", "")),
    )
