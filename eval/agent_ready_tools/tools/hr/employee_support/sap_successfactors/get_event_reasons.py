from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class EventReason:
    """Represents an FOEventReason in SAP SuccessFactors."""

    description: str
    external_code: str


@dataclass
class EventReasonsResponse:
    """Respresents the list of FOEventReasons configured in SAP SuccessFactors."""

    event_reasons: list[EventReason]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_event_reasons() -> EventReasonsResponse:
    """
    Get the collection of FOEventReason objects.

    Returns:
        A collection of FOEventReason object
    """
    client = get_sap_successfactors_client()

    filter_expr = "eventNav/externalCode eq '26' and status eq 'A'"

    response = client.get_request(entity="FOEventReason", filter_expr=filter_expr)

    event_reasons = [
        EventReason(description=e["description"], external_code=e["externalCode"])
        for e in response["d"]["results"]
    ]

    return EventReasonsResponse(event_reasons)
