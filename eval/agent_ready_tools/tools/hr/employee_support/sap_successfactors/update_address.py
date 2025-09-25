from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdateAddressResult:
    """Represents the result of an address update operation in SAP SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_address(
    person_id_external: str,
    address_type: str,
    city: str,
    start_date: str,
    country: str,
    notes: Optional[str] = None,
    province: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    address_1: Optional[str] = None,
    address_2: Optional[str] = None,
) -> UpdateAddressResult:
    """
    Updates a user's address in SAP SuccessFactors.

    Args:
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API.
        address_type: The address type matching one of the cases returned by the
            `get_address_types_sap` tool.
        city: The picklist option ID of the city associated with the address, as specified by the
            `search_cities_by_country` tool.
        start_date: The start date associated with the address in ISO 8601 format (e.g., YYYY-MM-
        country: The 3-letter ISO code for the country associated with the address.
            DD).
        notes: Optional comments associated with the address.
        province: The picklist option ID of the province associated with the address, as specified
            by the `search_provinces_by_country` tool.
        state: The picklist option ID of the state associated with the address, as specified by the
            `search_states_by_country` tool.
        zip_code: The zip code associated with the address.
        address_1: The first line of the address.
        address_2: The second line of the address.

    Returns:
        The result from performing the update to the user's address.
    """
    client = get_sap_successfactors_client()

    payload = {
        "__metadata": {"uri": "PerAddressDEFLT", "type": "SFOData.PerAddressDEFLT"},
        "address1": address_1,
        "address2": address_2,
        "addressType": address_type,
        "city": city,
        "country": country,
        "notes": notes,
        "personIdExternal": person_id_external,
        "province": province,
        "startDate": iso_8601_to_sap_date(start_date),
        "state": state,
        "zipCode": zip_code,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.upsert_request(payload=payload)
    try:
        http_code = response["d"][0]["httpCode"]
        message = response["d"][0].get("message")
    except AttributeError as e:
        raise ValueError(f"unexpected Output:", e)

    return UpdateAddressResult(http_code=http_code, message=message)
