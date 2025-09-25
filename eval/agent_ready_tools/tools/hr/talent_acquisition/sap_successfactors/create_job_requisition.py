from http import HTTPStatus
import json
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_ta_utility import (
    get_country_code,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class CreateJobRequisitionResponse:
    """Represents the result of create_job_requisition in SAP SuccessFactors."""

    http_code: Optional[int]
    message: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def create_job_requisition(
    template_id: str,
    country: Optional[str] = None,
    posting_country: Optional[str] = None,
    company_code: Optional[str] = None,
    job_start_date: Optional[str] = None,
    number_of_openings: Optional[str] = None,
    employee_type: Optional[str] = None,
    job_function_code: Optional[str] = None,
    state: Optional[str] = None,
    location_code: Optional[str] = None,
    hiring_manager_id: Optional[str] = None,
    recruiter_manager_id: Optional[str] = None,
    internal_job_title: Optional[str] = None,
    external_job_title: Optional[str] = None,
    custom_fields: Optional[Dict[str, Dict[str, Any]]] = None,
) -> CreateJobRequisitionResponse:
    """
    Creates a job requisition in SAP SuccessFactors.

    Args:
        template_id: The template ID returned by `get_template_details` tool.
        country: The full country name as provided by the user (e.g., "United States"). Do not convert to ISO code.
        posting_country: The full posting country name as provided by the user (e.g., "United States"). Do not convert to ISO code.
        company_code: The external code returned by `sap_get_companies` tool.
        job_start_date: The start date in ISO 8601 format (e.g., YYYY-MM-DD).
        number_of_openings: Number of openings for the job requisition.
        employee_type: The picklist ID returned by `search_employee_type` tool.
        job_function_code: The picklist ID returned by `search_job_functions` tool.
        state: The picklist ID returned by `search_states` tool.
        location_code: The location ID returned by `get_location_id` tool.
        hiring_manager_id: Unique identifier of the hiring manager in SuccessFactors.
        recruiter_manager_id: Unique identifier of the recruiter in SuccessFactors.
        internal_job_title: Internal job title of the requisition.
        external_job_title: External job title of the requisition.
        custom_fields: Deployment specific custom fields e.g. secondRecruiter, jobskill, jobGrade provided by the user.

    Returns:
        Result of the job requisition creation.
    """

    # Ensure non-None string is passed to utility functions
    country_code = get_country_code(country=country) if country else None

    client = get_sap_successfactors_client()

    payload: Dict[str, Any] = {
        "__metadata": {
            "uri": "JobRequisition",
            "type": "SFOData.JobRequisition",
        },
        "templateId": template_id,
        "legalEntity_obj": {"externalCode": company_code},
        "country": posting_country,
        "jobStartDate": iso_8601_to_sap_date(job_start_date) if job_start_date else None,
        "numberOpenings": number_of_openings,
        "filter2": {"id": job_function_code},
        "filter1": {"id": country_code},
        "filter3": {"id": employee_type},
        "state": {"id": state},
        "location_obj": {"externalCode": location_code},
        "hiringManager": {"usersSysId": hiring_manager_id},
        "recruiter": {"usersSysId": recruiter_manager_id},
        "jobReqLocale": {"jobTitle": internal_job_title, "externalTitle": external_job_title},
    }

    # Handling custom fields for creating a job requisition.
    if custom_fields and custom_fields is not None:
        custom_fields_dict = (
            json.loads(custom_fields) if isinstance(custom_fields, str) else custom_fields
        )
        for field_name, info in custom_fields_dict.items():
            field_type = info.get("type", "")
            value = info.get("value", "")
            key = info.get("key", field_name)
            payload[field_name] = {key: value} if field_type in ["picklist", "object"] else value

    # Handling payload by removing the none values for creating a job requisition.
    payload = {
        field_name: cleaned_field_value
        for field_name, field_value in payload.items()
        if (
            cleaned_field_value := (
                {
                    param_key: param_value
                    for param_key, param_value in field_value.items()
                    if param_value
                }
                if isinstance(field_value, dict)
                else field_value
            )
        )
    }

    try:
        response = client.upsert_request(payload=payload)

        return CreateJobRequisitionResponse(
            http_code=response.get("d", [])[0].get("httpCode", ""),
            message=response.get("d", [])[0].get("message", ""),
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response else {}
        message = (
            error_response.get("d", [])[0].get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return CreateJobRequisitionResponse(
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
