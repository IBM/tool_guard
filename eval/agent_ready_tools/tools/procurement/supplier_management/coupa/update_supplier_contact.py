from typing import Dict, Iterable, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    ContactPurposeType,
    CoupaSupplierDetails,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_supplier_contact(
    supplier_id: int,
    contact_id: int,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    country_code: Optional[str] = None,
    area_code: Optional[str] = None,
    phone_number: Optional[str] = None,
    purpose_name: Optional[Union[Iterable[ContactPurposeType] | ContactPurposeType]] = None,
) -> ToolResponse[CoupaSupplierDetails]:
    """
    Update a supplier contact details in Coupa.

    Args:
        supplier_id: The unique identifier of the supplier in Coupa, returned by the
            `get_all_suppliers` tool.
        contact_id: The unique identifier of the supplier contact in Coupa, returned by the
            `get_supplier_by_id` tool.
        email: The email of the supplier contact in Coupa.
        first_name: The contact's first name
        last_name: The contact's last name.
        country_code: The country code of the phone number of the supplier in Coupa.
        area_code: The area code of the supplier in Coupa.
        phone_number: The phone number of the supplier in Coupa.
        purpose_name: The purpose of the supplier contact in Coupa.

    Returns:
        Result from updating supplier contact
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    if purpose_name is None:
        purposes: List[ContactPurposeType] = []
    else:
        purposes = list([purpose_name] if isinstance(purpose_name, str) else purpose_name)

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
                "id": contact_id,
                "email": email,
                "name-given": first_name,
                "name-family": last_name,
                "phone-work": phone_work,
                "purposes": purposes_list,
            }
        ]
    }
    payload = {
        key: [{key: value for key, value in item.items() if value} for item in value]
        for key, value in payload.items()
        if value
    }

    response = client.put_request(
        resource_name=f"suppliers/{supplier_id}",
        payload=payload,
        params={"fields": '["id","number","status","name",{"primary_contact":["email"]}]'},
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier contact updated",
        content=CoupaSupplierDetails(
            id=response.get("id", ""),
            number=response.get("number", ""),
            status=response.get("status", ""),
            name=response.get("name", ""),
            contact_email=response.get("primary-contact", {}).get("email", ""),
        ),
    )
