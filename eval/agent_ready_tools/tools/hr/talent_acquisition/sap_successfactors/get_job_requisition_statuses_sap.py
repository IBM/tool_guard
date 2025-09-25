from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class ReqStatus:
    """A job requisition status configured for a SuccessFactors deployment."""

    status_id: str
    label: str


@dataclass
class ReqStatusesResponse:
    """A list of job requisition statuses configured for a SuccessFactors deployment."""

    requisition_statuses: list[ReqStatus]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_job_requisition_statuses_sap() -> ReqStatusesResponse:
    """
    Gets a list of job requisition statuses configured for this SuccessFactors deployment.

    Returns:
        A list of job requisition statuses with the first available English label.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field="reqStatus")

    requisition_statuses = [
        ReqStatus(
            status_id=option.get("id"),
            label=get_first_en_label(labels=option.get("picklistLabels", {}).get("results", [])),
        )
        for option in response.get("d", {}).get("picklistOptions", {}).get("results", [])
    ]

    return ReqStatusesResponse(requisition_statuses=requisition_statuses)
