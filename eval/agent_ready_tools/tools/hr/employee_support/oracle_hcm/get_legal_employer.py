from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class LegalEmployer:
    """Represents legal employer details in Oracle HCM."""

    legal_employer_name: str


@dataclass
class LegalEmployerResponse:
    """Represents the response from getting a legal employer in Oracle HCM."""

    legal_employer_names: List[LegalEmployer]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_legal_employer(
    legal_employer_name: Optional[str] = None, limit: Optional[int] = 20, offset: Optional[int] = 0
) -> LegalEmployerResponse:
    """
    Gets a legal employer in Oracle HCM.

    Args:
        legal_employer_name: The name of the legal employer to filter results.
        limit: The maximum number of legal employers to retrieve in a single API call. Defaults to
            20. Use this to control the size of the result set.
        offset: The number of legal employers to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        The legal employers.
    """

    client = get_oracle_hcm_client()

    params = {"limit": limit, "offset": offset}
    filter_expr = f"Name='{legal_employer_name}'" if legal_employer_name else None
    response = client.get_request(entity="legalEmployersLov", q_expr=filter_expr, params=params)
    legal_employer_names_list = [
        LegalEmployer(legal_employer_name=employer.get("Name"))
        for employer in response.get("items", [])
    ]
    return LegalEmployerResponse(legal_employer_names=legal_employer_names_list)
