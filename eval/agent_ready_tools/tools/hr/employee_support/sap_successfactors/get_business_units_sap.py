from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class SAPBusinessUnit:
    """Represents a business unit in SAP SuccessFactors."""

    business_unit_external_code: str
    business_unit_name: str


@dataclass
class BusinessUnitResponse:
    """Represents the response of the list of business units in SAP SuccessFactors."""

    business_units: List[SAPBusinessUnit]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_business_units_sap() -> BusinessUnitResponse:
    """
    Gets list of business units in SAP SuccessFactors.

    Returns:
        The business unit external code and business unit name.
    """
    client = get_sap_successfactors_client()

    response = client.get_request("FOBusinessUnit", select_expr=f"name,externalCode")

    business_units: list[SAPBusinessUnit] = []
    for result in response["d"]["results"]:
        business_units.append(
            SAPBusinessUnit(
                business_unit_external_code=result.get("externalCode"),
                business_unit_name=result.get("name"),
            )
        )
    return BusinessUnitResponse(business_units=business_units)
