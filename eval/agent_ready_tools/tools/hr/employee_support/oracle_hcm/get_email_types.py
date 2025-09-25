from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass(frozen=True)
class EmailTypes:
    """Represents an email type in Oracle HCM."""

    email_type_code: str
    email_type_name: str


@dataclass
class EmailTypeResponse:
    """A list of email types configured for an Oracle HCM deployment."""

    email_types: list[EmailTypes]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_email_types_oracle() -> EmailTypeResponse:
    """
    Gets a list of email types configured for an Oracle HCM deployment.

    Returns:
        A response containing a list of email types.
    """

    client = get_oracle_hcm_client()
    response = client.get_request(
        entity="commonLookupsLOV", q_expr="LookupType='EMAIL_TYPE'", path="fscmRestApi"
    )

    email_types_list: List[EmailTypes] = [
        EmailTypes(
            email_type_code=email.get("LookupCode", ""),
            email_type_name=email.get("Meaning", ""),
        )
        for email in response.get("items", [])
    ]

    return EmailTypeResponse(email_types=email_types_list)
