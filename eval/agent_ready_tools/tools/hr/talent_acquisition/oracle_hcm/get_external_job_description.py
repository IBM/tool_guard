import http
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
import requests

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleGetExternalJobDescription:
    """Represents the response from getting a external job requisition description in Oracle HCM."""

    description: Optional[str]
    message: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_external_job_description(
    requisition_number: str,
) -> OracleGetExternalJobDescription:
    """
    Gets an external job requisition description from Oracle HCM.

    Args:
        requisition_number: The requisition_number is the unique identifier for a job requisition in Oracle HCM
            returned by the `get_job_requisitions` tool.

    Returns:
        The description of the external job requisition.
    """
    client = get_oracle_hcm_client()
    try:
        response = client.get_response_text(
            entity=f"recruitingJobRequisitions/{requisition_number}/enclosure/ExternalDescription",
        )
        return OracleGetExternalJobDescription(description=response, message=None)
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == http.HTTPStatus.NOT_FOUND:
            error_detail = err.response
            message = f"No external job description found with job requisition number: {requisition_number}, {error_detail}"
            return OracleGetExternalJobDescription(description=None, message=message)

        else:
            return OracleGetExternalJobDescription(description=None, message=f"Unexpected error")
