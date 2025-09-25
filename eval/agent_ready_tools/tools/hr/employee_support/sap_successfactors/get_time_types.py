from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class TimeType:
    """A single time type in SuccessFactors."""

    external_code: str
    workflow_configuration: str
    unit: str
    absence_class: str
    category: str
    external_name: str


@dataclass
class GetTimeTypesResponse:
    """Represents the response from getting a list of time types configured for a SuccessFactors
    deployment."""

    time_types: list[TimeType]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_time_types(country: str) -> GetTimeTypesResponse:
    """
    Gets a list of time types configured for this SuccessFactors deployment.

    Args:
        country: The country to which the user belongs in SAP SuccessFactors, as returned by
            `get_country_of_employment` tool.

    Returns:
        A list of time types.
    """
    client = get_sap_successfactors_client()
    response = client.get_request(
        entity="TimeType",
        params={"$format": "JSON"},
        filter_expr=f"country eq '{country}'",
        select_expr="country,externalCode,workflowConfiguration,unit,absenceClass,category,externalName_en_US",
    )
    response_data = response.get("d", {})
    results = response_data.get("results", [])
    time_types: list[TimeType] = []
    for time_type in results:
        time_types.append(
            TimeType(
                external_code=time_type["externalCode"],
                workflow_configuration=time_type["workflowConfiguration"],
                unit=time_type["unit"],
                absence_class=time_type["absenceClass"],
                category=time_type["category"],
                external_name=time_type["externalName_en_US"],
            ),
        )

    return GetTimeTypesResponse(time_types=time_types)
