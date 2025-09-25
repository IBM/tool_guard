from typing import Any, List

from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client


@dataclass
class JobRequisitionResponse:
    """Represents the response from creating a time off request in SAP SuccessFactors."""

    location: str
    company: str


def get_job_requisition(job_requisition_id: str) -> JobRequisitionResponse:
    """
    Gets the job description of a job requisition in SAP SuccessFactors.

    Args:
        job_requisition_id: The job requisition id returned by `list_job_requisitions` in SAP SuccessFactors.
    Returns:
        It retrieves the job requisition description.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        entity="JobRequisition",
        filter_expr=f"jobReqId eq '{job_requisition_id}'",
        expand_expr="location_obj,legalEntity_obj",
    )

    requistion_details: List[Any] = []

    results = response.get("d", {}).get("results", [])
    for details in results:
        location_obj = details.get("location_obj", {}).get("results", [])[0].get("externalCode", "")
        requistion_details.append(location_obj)
        legal_entity_obj = details.get("legalEntity_obj", {}).get("externalCode", "")
        requistion_details.append(legal_entity_obj)

    return JobRequisitionResponse(location=location_obj, company=legal_entity_obj)


def get_country_code(country: str) -> str:
    """
    Retrieves country code specific to SuccessFactors.

    Args:
        country: The name of the country for which the corresponding country code will be retrieved.
    Returns:
        The country code of the country specific to SuccessFactors.
    """

    client = get_sap_successfactors_client()

    response = client.get_request(
        entity="PicklistLabel",
        filter_expr=f"picklistOption/picklist/picklistId eq 'country' and locale eq 'en_US' and label eq '{country}'",
        expand_expr="picklistOption/picklist",
        select_expr="label,picklistOption/id,picklistOption/externalCode",
    )

    result = response.get("d", {}).get("results", [])[0].get("picklistOption", {}).get("id", "")

    return result
