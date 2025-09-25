from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class CreateEmergencyContactResponse:
    """Represents the response from creating a user's emergency contact in Oracle HCM."""

    person_id: int
    person_number: str
    contact_relationship_id: List[int]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_emergency_contact(
    person_id: str,
    first_name: str,
    last_name: str,
    contact_type: str,
    country: str,
    email_address: str,
    phone_number: str,
    email_type: str = "H1",
    phone_type: str = "HM",
) -> CreateEmergencyContactResponse:
    """
    Create a user's emergency contact in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifying them within the Oracle HCM.
        first_name: Name of the emergency contact.
        last_name: Last name of the emergency contact.
        contact_type: Contact type returned by the `get_contact_types` tool.
        country: The 2-digit ISO code (ISO 3166-1 alpha-2) for the country associated with the
            address.
        email_address: The email address of the contact.
        phone_number: The phone number of the contact.
        email_type: Email type, soft default to home email.
        phone_type: Phone type, soft default to home mobile.

    Returns:
        The user's emergency contact response.
    """
    client = get_oracle_hcm_client()

    response = client.post_request(
        entity="hcmContacts",
        payload={
            "names": [{"FirstName": first_name, "LastName": last_name, "LegislationCode": country}],
            "contactRelationships": [
                {
                    "RelatedPersonId": person_id,
                    "ContactType": contact_type,
                    "EmergencyContactFlag": True,
                }
            ],
            "emails": [
                {
                    "EmailAddress": email_address,
                    "EmailType": email_type,
                }
            ],
            "phones": [
                {
                    "PhoneNumber": phone_number,
                    "PhoneType": phone_type,
                }
            ],
        },
    )
    contact_relationships = response.get("contactRelationships", {}).get("items", [])
    return CreateEmergencyContactResponse(
        person_id=response["PersonId"],
        person_number=response["PersonNumber"],
        contact_relationship_id=[
            relationship.get("ContactRelationshipId", "") for relationship in contact_relationships
        ],
    )
