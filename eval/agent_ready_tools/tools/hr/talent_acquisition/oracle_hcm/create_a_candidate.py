from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class CreateCandidateResponse:
    """Represents the results of candidate create operation in Oracle HCM."""

    http_code: int
    message: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_candidate_oracle(
    last_name: str,
    first_name: str,
    email_address: str,
    middle_name: Optional[str] = None,
    suffix: Optional[str] = None,
    known_as: Optional[str] = None,
    honors: Optional[str] = None,
) -> CreateCandidateResponse:
    """
    Creates a candidate in Oracle HCM.

    Args:
        last_name: The candidate's last name.
        first_name: The candidate's first name.
        email_address: The candidate's primary email contact.
        middle_name: The candidate's middle name.
        suffix: The suffix associated with the candidate's name.
        known_as: The name the candidate is commonly known by or prefers to be called.
        honors: Any academic or professional honors or titles held by the candidate.

    Returns:
        The status of the candidate creation process.
    """

    client = get_oracle_hcm_client()

    payload = {
        "LastName": last_name,
        "MiddleNames": middle_name,
        "FirstName": first_name,
        "Suffix": suffix,
        "KnownAs": known_as,
        "Honors": honors,
        "Email": email_address,
    }
    payload = {key: value for key, value in payload.items() if value}
    response = client.post_request(entity="recruitingCandidates", payload=payload)

    if response.get("status_code") == HTTPStatus.CREATED:
        return CreateCandidateResponse(http_code=response.get("status_code", ""), message=None)
    else:
        return CreateCandidateResponse(
            http_code=response.get("status_code", ""),
            message=response.get("message", "There was an error creating the candidate."),
        )
