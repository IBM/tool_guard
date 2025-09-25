from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class CreateHomeAddressResult:
    """Represents the results of home address create operation in Oracle HCM."""

    address_line_1: str
    city: str
    postal_code: str
    state: str
    country: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_home_address(
    worker_id: str,
    address_type: str,
    address_line_1: str,
    city: str,
    state: str,
    postal_code: str,
    country: str,
    address_line_2: Optional[str] = None,
    is_primary_address: Optional[bool] = False,
    county: Optional[str] = None,
    province: Optional[str] = None,
) -> CreateHomeAddressResult:
    """
    Creates worker's home address in Oracle HCM.

    Args:
        worker_id: The worker's worker_id uniquely identifying them within the Oracle HCM API.
        address_type: The address type matching one of the cases returned by the
            `get_address_types_oracle` tool.
        address_line_1: The first line of the address.
        city: The city or town associated with the address.
        state: The state associated with the address.
        postal_code: The postal code associated with the address.
        country: The 2-digit ISO code (ISO 3166-1 alpha-2) for the country associated with the
            address.
        address_line_2: The second line of the address.
        is_primary_address: Indicates whether this is the primary address for the user.
        county: The county associated with the address.
        province: The province associated with the address.

    Returns:
        An instance of CreateHomeAddressResult containing the create
        address details.
    """

    client = get_oracle_hcm_client()

    payload = {
        "AddressType": address_type,
        "AddressLine1": address_line_1,
        "AddressLine2": address_line_2,
        "PostalCode": postal_code,
        "TownOrCity": city,
        "Region1": county,
        "Region2": state,
        "Region3": province,
        "Country": country,
        "PrimaryFlag": is_primary_address,
    }

    payload = {key: value for key, value in payload.items() if value}
    entity = f"workers/{worker_id}/child/addresses"
    response = client.post_request(entity=entity, payload=payload)

    return CreateHomeAddressResult(
        address_line_1=response.get("AddressLine1", ""),
        city=response.get("TownOrCity", ""),
        postal_code=response.get("PostalCode", ""),
        state=response.get("Region2", ""),
        country=response.get("Country", ""),
    )
