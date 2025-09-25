from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleBusinessUnit:
    """Represents the details of a single business unit in Oracle HCM."""

    business_unit_name: str


@dataclass
class BusinessUnitsResponse:
    """Represents a list of business units in Oracle HCM."""

    business_units: List[OracleBusinessUnit]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_business_units_oracle(
    business_unit_name: Optional[str] = None, limit: Optional[int] = 20, offset: Optional[int] = 0
) -> BusinessUnitsResponse:
    """
    Gets a list of business units from Oracle HCM, with an optional query parameter to filter by
    name.

    Args:
        business_unit_name: The name of the business unit to filter results.
        limit: The maximum number of business units to retrieve in a single API call. Defaults to
            20. Use this to control the size of the result set.
        offset: The number of business units to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        A BusinessUnitsResponse containing a list of business units.
    """
    client = get_oracle_hcm_client()

    params = {"limit": limit, "offset": offset}
    filter_expr = None
    if business_unit_name:
        filter_expr = f"Name='{business_unit_name}'"
    response = client.get_request(entity="hcmBusinessUnitsLOV", q_expr=filter_expr, params=params)

    business_units = [
        OracleBusinessUnit(business_unit_name=unit.get("Name"))
        for unit in response.get("items", [])
    ]

    return BusinessUnitsResponse(business_units)
