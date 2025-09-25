from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class ContactType:
    """Represents a contact type in Oracle HCM."""

    contact_type: str
    relation: str


@dataclass
class ContactTypesResponse:
    """Represents the list of contact types in Oracle HCM."""

    contact_types: list[ContactType]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_contact_types(country: str) -> ContactTypesResponse:
    """
    Retrieve the list of contact types in Oracle HCM.

    Args:
        country: The 2-digit ISO code (ISO 3166-1 alpha-2) for the country associated with the
            address.

    Returns:
        A list of contact types.
    """

    client = get_oracle_hcm_client()
    headers = {"REST-Framework-Version": "4"}

    response = client.get_request(
        entity=f"commonLookupsLOV",
        q_expr=f"LookupType='CONTACT'",
        path="fscmRestApi",
        headers=headers,
        params={"limit": 500},
    )

    contact_types: list[ContactType] = []

    for result in response["items"]:
        tag = result.get("Tag", "")
        if tag:
            new_tag = [item.strip() for item in tag.split(",")]
            if new_tag[0].startswith("-"):
                countries = {item.lstrip("-") for item in new_tag}
                if country not in countries:
                    contact_types.append(
                        ContactType(
                            contact_type=result.get("LookupCode", ""),
                            relation=result.get("Meaning", ""),
                        )
                    )
            else:
                if f"+{country}" in new_tag or f"{country}" in new_tag:
                    contact_types.append(
                        ContactType(
                            contact_type=result.get("LookupCode", ""),
                            relation=result.get("Meaning", ""),
                        )
                    )

    return ContactTypesResponse(contact_types=contact_types)
