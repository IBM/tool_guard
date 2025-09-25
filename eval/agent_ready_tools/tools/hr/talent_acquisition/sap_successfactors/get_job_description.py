from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class JobDescription:
    """Represents the job description of a job requisition in SAP SuccessFactors."""

    job_requisition_id: Optional[str] = None
    job_title: Optional[str] = None
    internal_job_description: Optional[str] = None
    external_job_description: Optional[str] = None


@dataclass
class GetJobDescriptionResponse:
    """A list of job descriptions."""

    job_descriptions: List[JobDescription]
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_job_description(
    hiring_manager_user_id: Optional[str] = None,
    recruiter_user_id: Optional[str] = None,
    job_requisition_id: Optional[str] = None,
    top: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> GetJobDescriptionResponse:
    """
    Gets the job description(s) of job requisition(s) in SAP SuccessFactors.

    Args:
        hiring_manager_user_id: The hiring manager user id returned by the tool `get_user_successfactors_ids` in SAP Successfactors.
        recruiter_user_id: The recruiter user id returned by the tool `get_user_successfactors_ids` in SAP Successfactors.
        job_requisition_id: The job requisition id is returned by the tool `get_job_requisitions` in SAP Successfactors.
        top: The maximum number of job descriptions to retrieve in a single API call. Defaults to 10. Use this to control the size of the result set.
        skip: The number of job descriptions to skip for pagination purposes. Defaults to 0.

    Returns:
        A list of job descriptions.
    """
    try:
        job_description_list = []
        client = get_sap_successfactors_client()

        params = {"$orderby": "jobReqId desc", "$top": top, "$skip": skip}
        filters = []
        if job_requisition_id:
            filters.append(f"jobReqId eq '{job_requisition_id}'")
        if hiring_manager_user_id:
            filters.append(f"hiringManager/usersSysId eq '{hiring_manager_user_id}'")
        if recruiter_user_id:
            filters.append(f"recruiter/usersSysId eq '{recruiter_user_id}'")

        filter_expr = " and ".join(filters) if filters else None

        response = client.get_request(
            entity="JobRequisitionLocale",
            filter_expr=filter_expr,
            select_expr="externalJobDescription,jobDescription,jobTitle,jobReqId",
            params=params,
        )
        results = response.get("d", {}).get("results", [])

        job_description_list = [
            JobDescription(
                external_job_description=item.get("externalJobDescription", ""),
                internal_job_description=item.get("jobDescription", ""),
                job_title=item.get("jobTitle", ""),
                job_requisition_id=item.get("jobReqId", ""),
            )
            for item in results
        ]
        return GetJobDescriptionResponse(job_descriptions=job_description_list)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return GetJobDescriptionResponse(
            job_descriptions=[],
            http_code=(
                e.response.status_code
                if e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
