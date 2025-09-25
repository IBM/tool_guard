from dataclasses import field
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class CandidateDetails:
    """Represents the candidate details."""

    candidate_id: str
    country: str
    first_name: str
    last_name: str
    contact_email: str
    city: str
    address: Optional[str] = None
    cell_phone: Optional[str] = None
    zip_code: Optional[str] = None


@dataclass
class GetAllCandidatesResponse:
    """Represents a list of candidate details."""

    candidates: List[CandidateDetails] = field(default_factory=list)
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_all_candidates(
    city: Optional[str] = None,
    top: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> GetAllCandidatesResponse:
    """
    Retrieves the candidates in SAP SuccessFactors.

    Args:
        city: The name of the city to use when searching for candidates.
        top: The maximum number of job requisition records to retrieve.
        skip: The number of job requisition records to skip.

    Returns:
        A list of candidates.
    """

    try:
        client = get_sap_successfactors_client()

        params = {"$top": top, "$skip": skip}
        filters = []
        if city:
            filters.append(f"city eq '{city}'")

        filter_expr = " and ".join(filters) if filters else None

        response = client.get_request(
            entity="Candidate",
            filter_expr=filter_expr,
            select_expr="candidateId,country,zip,firstName,lastName,education,address,contactEmail,cellPhone,city",
            params=params,
        )
        results = response.get("d", {}).get("results", [])
        candidates_list = [
            CandidateDetails(
                candidate_id=location.get("candidateId"),
                country=location.get("country"),
                first_name=location.get("firstName"),
                last_name=location.get("lastName"),
                address=location.get("address"),
                contact_email=location.get("contactEmail"),
                city=location.get("city"),
                cell_phone=location.get("cellPhone"),
                zip_code=location.get("zip"),
            )
            for location in results
        ]

        return GetAllCandidatesResponse(
            candidates=candidates_list,
        )

    except HTTPError as e:
        message = f"An unexpected error occurred: {e}"

        return GetAllCandidatesResponse(
            http_code=e.response.status_code,
            message=message,
        )
