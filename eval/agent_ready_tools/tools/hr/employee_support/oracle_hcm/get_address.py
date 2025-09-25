from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class Address:
    """represents a single address record of a worker in Oracle HCM."""

    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: Optional[str]
    country: str
    postal_code: Optional[str]
    is_primary_address: Optional[bool]
    county: Optional[str]
    province: Optional[str]
    address_uniq_id: str


@dataclass
class GetAddressResponse:
    """Represents all address records of a worker in Oracle HCM."""

    address_details: list[Address]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_address(worker_id: str, address_type: str) -> GetAddressResponse:
    """
    Gets a worker's address in Oracle HCM.

    Args:
        worker_id: The worker's worker_id uniquely identifying them within the Oracle HCM API.
        address_type: "The type of address to retrieve provided by get_address_types_oracle."

    Returns:
        The worker's address.
    """

    client = get_oracle_hcm_client()

    entity = f"workers/{worker_id}/child/addresses"
    response = client.get_request(entity, q_expr=f"AddressType ={address_type}")

    address_details_list: list[Address] = []

    for result in response["items"]:
        address_details_list.append(
            Address(
                address_line_1=result.get("AddressLine1"),
                address_line_2=result.get("AddressLine2"),
                city=result.get("TownOrCity"),
                county=result.get("Region1"),
                state=result.get("Region2"),
                province=result.get("Region3"),
                postal_code=result.get("PostalCode"),
                country=result.get("Country"),
                is_primary_address=result.get("PrimaryFlag"),
                address_uniq_id=get_id_from_links(result.get("links")[0].get("href")),
            )
        )
    return GetAddressResponse(address_details=address_details_list)
