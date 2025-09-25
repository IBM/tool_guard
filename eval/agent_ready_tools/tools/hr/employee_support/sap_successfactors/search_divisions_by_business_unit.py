from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class Division:
    """Represents a division in SAP SuccessFactors."""

    division_external_code: str
    division_name: str


@dataclass
class DivisionResponse:
    """Represents the response of the list of divisions in SAP SuccessFactors."""

    divisions: List[Division]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_divisions_by_business_unit(business_unit_name: str) -> DivisionResponse:
    """
    Gets list of divisions in SAP SuccessFactors.

    Args:
        business_unit_name: The business_unit_name will be returned by the `get_business_units_sap`
            tool.

    Returns:
        The division external code and division name.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        "FODivision",
        filter_expr=f"cust_toBusinessUnit/name eq '{business_unit_name}'",
        select_expr=f"name,externalCode",
        expand_expr=f"cust_toBusinessUnit",
    )

    divisions: list[Division] = []
    for result in response["d"]["results"]:
        divisions.append(
            Division(
                division_external_code=result.get("externalCode"),
                division_name=result.get("name"),
            )
        )
    return DivisionResponse(divisions=divisions)
