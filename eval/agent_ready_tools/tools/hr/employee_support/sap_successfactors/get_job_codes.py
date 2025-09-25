from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class JobCode:
    """
    Represents a single job code record in SAP SuccessFactors.

    Job Codes are used to define unique job functions or roles within an organization. They can be
    assigned to worker records to group people with similar skills.
    """

    code: str
    "external code."
    name: str


@dataclass
class JobCodeResponse:
    """Represents all job code records in SAP SuccessFactors."""

    job_codes: List[JobCode]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_job_codes() -> JobCodeResponse:
    """
    Gets the list of job codes configured for this SAP SuccessFactors deployment.

    Returns:
        The list of job codes.
    """

    client = get_sap_successfactors_client()
    response = client.get_request(entity="FOJobCode", select_expr="externalCode,name")
    results = response["d"]["results"]

    job_codes = [
        JobCode(
            code=record.get("externalCode"),
            name=record.get("name"),
        )
        for record in results
    ]

    return JobCodeResponse(job_codes=job_codes)
