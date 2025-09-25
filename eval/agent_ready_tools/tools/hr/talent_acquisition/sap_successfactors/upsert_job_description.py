from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_ta_utility import (
    get_job_requisition,
)
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpsertJobDescriptionResult:
    """Represents the result of performing create or update operation on a job description in SAP
    SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def upsert_job_description(
    job_requisition_id: str, internal_job_description: str, external_job_description: str
) -> UpsertJobDescriptionResult:
    """
    Upserts a job description in SAP SuccessFactors.

    Args:
        job_requisition_id: The ID of the job requisition, returned by the `get_job_requisitions` tool.
        internal_job_description: The internal job description of the job requisition.
        external_job_description: The external job description of the job requisition.

    Returns:
        The result of creating or updating the job description.
    """
    try:
        job_requisition_response = get_job_requisition(job_requisition_id=job_requisition_id)

        client = get_sap_successfactors_client()

        payload = {
            "__metadata": {
                "uri": "JobRequisition",
                "type": "SFOData.JobRequisition",
            },
            "jobReqId": job_requisition_id,
            "jobReqLocale": {
                "jobDescription": internal_job_description,
                "externalJobDescription": external_job_description,
            },
            "location_obj": {"externalCode": job_requisition_response.location},
            "legalEntity_obj": {"externalCode": job_requisition_response.company},
        }

        response = client.upsert_request(payload=payload)
        response_data = response.get("d", [])

        message = next(
            (res.get("message") for res in response_data if res.get("message")),
            None,
        )

        return UpsertJobDescriptionResult(
            http_code=response_data[0].get("httpCode"), message=message
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response else None
        message = (
            error_response.get("d", [])[0].get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return UpsertJobDescriptionResult(
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
