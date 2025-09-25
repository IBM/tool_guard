from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaSupplierAddressDetails,
    CoupaSupplierContactDetails,
    CoupaSupplierDetails,
    CoupaSupplierDetailsResponse,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_supplier_by_id(
    supplier_id: int,
) -> ToolResponse[CoupaSupplierDetailsResponse]:
    """
    Get a supplier by id in Coupa.

    Args:
        supplier_id: Supplier ID

    Returns:
        The supplier with the given ID
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name=f"suppliers/{supplier_id}",
        params={
            "fields": '["id","number","status","name",{"primary_contact":["email"]},{"contacts":["id","email","name_given","name_family","reference_code"]},{"supplier_addresses":["id","name","street1","street2","city","state","postal-code",{"country":["name"]},{"purposes":["name"]}]}]'
        },
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    supplier_details = CoupaSupplierDetails(
        id=response["id"],
        number=response["number"],
        status=response["status"],
        name=response["name"],
        contact_email=response["primary-contact"]["email"],
    )
    contact_details = [
        CoupaSupplierContactDetails(
            contact_id=item.get("id", ""),
            email=item.get("email"),
            reference_code=item.get("reference-code"),
            name_given=item.get("name-given"),
            name_family=item.get("name-family"),
            purpose=", ".join(
                [
                    purpose.get("name", "")
                    for purpose in item.get("purposes", [])
                    if purpose.get("name")
                ]
            ),
        )
        for item in response.get("contacts", [])
    ]

    address_details = [
        CoupaSupplierAddressDetails(
            address_id=item.get("id", ""),
            name=item.get("name", ""),
            street1=item.get("street1", ""),
            street2=item.get("street2", ""),
            city=item.get("city", ""),
            state=item.get("state", ""),
            country=(item["country"]["name"] if isinstance(item.get("country"), dict) else ""),
            postal_code=item.get("postal-code", ""),
            purpose=", ".join(
                [
                    purpose.get("name", "")
                    for purpose in item.get("purposes", [])
                    if purpose.get("name")
                ]
            ),
        )
        for item in response.get("supplier-addresses", [])
        if item["id"] and item["street1"]
    ]

    supplier = CoupaSupplierDetailsResponse(
        supplier_details=supplier_details,
        contact_details=contact_details,
        address_details=address_details,
    )

    return ToolResponse(success=True, message="Get supplier by ID successful", content=supplier)
