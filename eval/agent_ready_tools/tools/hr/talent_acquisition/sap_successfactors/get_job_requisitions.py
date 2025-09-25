from http import HTTPStatus
import re
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_schemas import (
    JobRequisitionSystemStatus,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


def get_external_code(results: Optional[list]) -> Optional[str]:
    """
    Extracts the externalCode value from the first item in a list of dictionaries.

    Args:
        results: A list of dictionaries, typically from an SAP SuccessFactors nested response.

    Returns:
        The 'externalCode' value from the first dictionary, or None if not found or list is empty.
    """
    if results and isinstance(results, list) and len(results) > 0:
        return results[0].get("externalCode")
    return None


def get_full_name(results: Optional[list]) -> Optional[str]:
    """
    Returns the full name by combining firstName and lastName from the first item.

    Args:
        results: A list of dictionaries, typically containing user profile information like firstName and lastName.

    Returns:
        A concatenation of first and last name if available, else None.
    """
    if results and isinstance(results, list) and len(results) > 0:
        first = results[0].get("firstName", "")
        last = results[0].get("lastName", "")
        return f"{first} {last}".strip() if first or last else None
    return None


@dataclass
class JobRequisition:
    """Represents the details of a single job requisition in SAP SuccessFactors."""

    job_req_id: str
    job_title: Optional[str]
    status: Optional[str]
    workflow_status: Optional[str]
    job_code: Optional[str]
    posting_country: Optional[str]
    job_country_code: Optional[str]
    job_grade: Optional[str]
    job_start_date: Optional[str]
    number_of_openings: Optional[str]
    business_unit: Optional[str]
    department: Optional[str]
    division: Optional[str]
    job_skill: Optional[str]
    employment_type: Optional[str]
    hiring_manager: Optional[str]
    second_recruiter: Optional[str]
    recruiter: Optional[str]
    job_function: Optional[str]
    location: Optional[str]


@dataclass
class JobRequisitionsResponse:
    """A list of job requisitions in SAP SuccessFactors."""

    job_requisitions: list[JobRequisition]
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_job_requisitions(
    job_req_id: Optional[str] = None,
    workflow_status: Optional[JobRequisitionSystemStatus] = None,
    status_id: Optional[str] = None,
    hiring_manager_user_id: Optional[str] = None,
    recruiter_user_id: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> JobRequisitionsResponse:
    """
    Get all job requisitions from SAP SuccessFactors.

    Args:
        job_req_id: Specific job requisition ID to retrieve.
        workflow_status: The workflow status of job requisition. Accepted values are APPROVED, PRE_APPROVED, CLOSED.
        status_id: The picklist option ID of the status matching one of the cases returned
            by the `get_job_requisition_statuses_sap` tool.
        hiring_manager_user_id: The user's user_id uniquely identifying them within the SuccessFactors API, returned by the `get_user_successfactors_ids` tool.
        recruiter_user_id: The user's user_id uniquely identifying them within the SuccessFactors API, returned by the `get_user_successfactors_ids` tool.
        limit: The maximum number of job requisition records to retrieve.
        skip: The number of job requisition records to skip.

    Returns:
        A structured list of job requisitions.
    """
    try:

        client = get_sap_successfactors_client()
        filters = []
        if job_req_id:
            filters.append(f"jobReqId eq '{job_req_id}'")
        if workflow_status:
            try:
                status_enum = JobRequisitionSystemStatus[workflow_status.upper()]
                filters.append(f"internalStatus eq '{status_enum.value}'")
            except KeyError:
                valid_statuses = [status.name for status in JobRequisitionSystemStatus]
                return JobRequisitionsResponse(
                    job_requisitions=[],
                    http_code=HTTPStatus.BAD_REQUEST,
                    message=(
                        f"Workflow status '{workflow_status}' is not valid. "
                        f"Accepted values are: {valid_statuses}"
                    ),
                )

        if status_id:
            filters.append(f"status/id eq '{status_id}'")
        if hiring_manager_user_id:
            filters.append(f"hiringManager/usersSysId eq '{hiring_manager_user_id}'")
        if recruiter_user_id:
            filters.append(f"recruiter/usersSysId eq '{recruiter_user_id}'")

        filter_expr = " and ".join(filters) if filters else None

        response = client.get_request(
            entity="JobRequisition",
            filter_expr=filter_expr,
            expand_expr=(
                "status,businessUnit_obj,department_obj,division_obj,"
                "filter1,jobskill,filter2,filter3,hiringManager,"
                "location_obj,secondRecruiter,jobReqLocale,recruiter"
            ),
            params={
                "$orderby": "jobReqId desc",
                "$top": limit,
                "$skip": skip,
            },
        )

        results = response.get("d", {}).get("results", [])
        job_requisitions_list = []

        for result in results:
            job_requisitions_list.append(
                JobRequisition(
                    job_req_id=result.get("jobReqId"),
                    job_title=(result.get("jobReqLocale", {}).get("results", [{}])[0] or {}).get(
                        "jobTitle"
                    ),
                    status=get_external_code(result.get("status", {}).get("results", [])),
                    workflow_status=result.get("internalStatus"),
                    job_code=result.get("jobCode"),
                    posting_country=result.get("country"),
                    job_country_code=get_external_code(
                        result.get("filter1", {}).get("results", [])
                    ),
                    job_grade=result.get("jobGrade"),
                    job_start_date=(
                        sap_date_to_iso_8601(
                            re.sub(r"([+-]\d+)?(?=\)/)", "", result["jobStartDate"])
                        )
                        if result.get("jobStartDate")
                        else None
                    ),
                    number_of_openings=result.get("numberOpenings"),
                    business_unit=(result.get("businessUnit_obj") or {}).get("name"),
                    department=(result.get("department_obj") or {}).get("name"),
                    division=(result.get("division_obj") or {}).get("name"),
                    job_skill=get_external_code(result.get("jobskill", {}).get("results", [])),
                    employment_type=get_external_code(result.get("filter3", {}).get("results", [])),
                    hiring_manager=get_full_name(
                        result.get("hiringManager", {}).get("results", [])
                    ),
                    second_recruiter=get_full_name(
                        result.get("secondRecruiter", {}).get("results", [])
                    ),
                    recruiter=get_full_name(result.get("recruiter", {}).get("results", [])),
                    job_function=next(
                        (
                            item.get("mdfExternalCode")
                            for item in result.get("filter2", {}).get("results", [])
                        ),
                        None,
                    ),
                    location=next(
                        (
                            item.get("name")
                            for item in result.get("location_obj", {}).get("results", [])
                        ),
                        None,
                    ),
                )
            )
        return JobRequisitionsResponse(job_requisitions=job_requisitions_list)
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return JobRequisitionsResponse(
            job_requisitions=[],
            http_code=(
                e.response.status_code
                if e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
