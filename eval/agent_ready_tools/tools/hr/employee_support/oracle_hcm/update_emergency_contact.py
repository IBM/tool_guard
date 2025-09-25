from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UpdateEmergencyContactResponse:
    """Represents the result of an emergency contact update operation in Oracle HCM."""

    http_code: int


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_emergency_contact_oracle(
    contact_uniq_id: str,
    contact_relationship_id: Optional[int] = None,
    contact_type: Optional[str] = None,
    email_address_id: Optional[int] = None,
    email_address: Optional[str] = None,
    phone_id: Optional[int] = None,
    phone_number: Optional[str] = None,
    address_line1: Optional[str] = None,
    town_or_city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    person_address_usage_id: Optional[int] = None,
) -> UpdateEmergencyContactResponse:
    """
    Updates the emergency contact of a user in Oracle HCM.

    Args:
        contact_uniq_id: The contact_id of the contact is returned by the `get_emergency_contacts`
            tool.
        contact_relationship_id: The contact_relationship_id for the contact relationship is
            returned by the `get_emergency_contacts` tool.
        contact_type: The contact_type of the contact relationship is returned by the
            `get_contact_types` tool using the 'relation'.
        email_address_id: The email_address_id, associated with the email address, is returned by
            the `get_emergency_contacts` tool.
        email_address: The email address of the contact.
        phone_id: The phone_id, associated with the phone, is returned by the
            `get_emergency_contacts` tool.
        phone_number: The phone number of the contact.
        address_line1: The first line of the contact's address.
        town_or_city: The town or city of the contact's address.
        state: The region or state of the contact's address.
        postal_code: The postal code of the contact's address.
        person_address_usage_id: The person_address_usage_id for the address usage by the person is
            returned by the `get_emergency_contacts` tool.

    Returns:
        The result from performing the update emergency contact tool.
    """
    client = get_oracle_hcm_client()
    payload = {
        "contactRelationships": [
            {
                "ContactRelationshipId": contact_relationship_id,
                "ContactType": contact_type,
            }
        ],
        "emails": [
            {
                "EmailAddressId": email_address_id,
                "EmailAddress": email_address,
            }
        ],
        "phones": [{"PhoneId": phone_id, "PhoneNumber": phone_number}],
        "addresses": [
            {
                "AddressLine1": address_line1,
                "TownOrCity": town_or_city,
                "Region2": state,
                "PostalCode": postal_code,
                "PersonAddrUsageId": person_address_usage_id,
            }
        ],
    }

    # Clean payload by removing keys with None values and excluding empty nested dictionaries.

    cleaned_payload = {
        key: [
            {field: record[field] for field in record if record[field] is not None}
            for record in payload[key]
            if any(record[field] is not None for field in record)
        ]
        for key in payload
    }

    entity = f"hcmContacts/{contact_uniq_id}"

    response = client.update_request(payload=cleaned_payload, entity=entity)

    http_code = response.get("status_code", "")

    return UpdateEmergencyContactResponse(http_code)
