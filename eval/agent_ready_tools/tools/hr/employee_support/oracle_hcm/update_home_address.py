from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UpdateHomeAddressResult:
    """Represents the result of home address update operation in Oracle HCM."""

    address_line_1: str
    city: str
    postal_code: Optional[str] = None


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_home_address_oracle(
    worker_id: str,
    address_uniq_id: str,
    address_line_1: str,
    city: str,
    postal_code: str,
    state_province_or_region: str,
    address_line_2: Optional[str] = None,
    county: Optional[str] = None,
    is_primary_address: Optional[str] = None,
) -> UpdateHomeAddressResult:
    """
    Updates the worker's home address in Oracle HCM.

    Args:
        worker_id: The worker's worker_id uniquely identifies them within the Oracle HCM API.
        address_uniq_id: The unique ID of the address to update, as specified by the `get_address`
            tool.
        address_line_1: The first line of the address.
        city: The city or town associated with the address.
        postal_code: The postal code associated with the address. The postal code MUST match the
            format relevant to the country returned by the get_address tool.
        state_province_or_region: The state, province, or region associated with the address, in two
            letter ISO format.
        address_line_2: The second line of the address.
        county: The county associated with the address.
        is_primary_address: Indicates whether this is the primary address for the worker.

    Returns:
        An instance of UpdateHomeAddressResult containing the updated
        address details.
    """

    client = get_oracle_hcm_client()
    payload = {
        "AddressLine1": address_line_1,
        "AddressLine2": address_line_2,
        "PostalCode": postal_code,
        "TownOrCity": city,
        "Region1": county,
        "Region2": state_province_or_region,
        "PrimaryFlag": is_primary_address,
    }

    payload = {key: value for key, value in payload.items() if value}
    entity = f"workers/{worker_id}/child/addresses/{address_uniq_id}"
    response = client.update_request(payload=payload, entity=entity)

    return UpdateHomeAddressResult(
        address_line_1=response.get("AddressLine1", ""),
        city=response.get("TownOrCity", ""),
        postal_code=response.get("PostalCode", ""),
    )
