from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class Candidate:
    """Represents a job candidate in Oracle HCM."""

    candidate_number: int
    last_name: str
    full_name: str
    first_name: Optional[str]
    candidate_email: Optional[str]
    candidate_type: Optional[str]


@dataclass
class CandidateResponse:
    """Represents the response from retreiving candidates in Oracle HCM."""

    candidates: List[Candidate]
    message: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_candidates(
    last_name: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> CandidateResponse:
    """
    Retrieves job candidates in Oracle HCM.

    Args:
        last_name: The last_name of the candidate in Oracle HCM.
        limit: The maximum number of candidate records to retrieve.
        offset: The number of candidate records to skip.

    Returns:
        A list of candidates.
    """
    try:
        client = get_oracle_hcm_client()

        q_expr = None
        params = {"limit": limit, "offset": offset}

        if last_name:
            q_expr = f"LastName={last_name}"

        response = client.get_request(
            entity="recruitingCandidates",
            q_expr=q_expr,
            params=params,
        )

    except HTTPError as e:
        message = f"An unexpected error occurred: {e}"

        return CandidateResponse(candidates=[], message=message)

    candidates_list: list[Candidate] = []
    items = response.get("items", [])
    if items:
        for result in items:
            candidates_list.append(
                Candidate(
                    candidate_number=result.get("CandidateNumber", ""),
                    first_name=result.get("FirstName", ""),
                    last_name=result.get("LastName", ""),
                    full_name=result.get("FullName", ""),
                    candidate_email=result.get("Email", ""),
                    candidate_type=result.get("CandidateType", ""),
                )
            )
    return CandidateResponse(candidates=candidates_list, message=None)
