from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class EmergencyContacts:
    """Represents an emergency contact in Oracle HCM."""

    contact_relationship_id: Optional[int]
    name: Optional[str]
    contact_type: Optional[str]
    related_person_id: Optional[int]
    related_person_number: Optional[str]
    email_address_id: Optional[int]
    email_address: Optional[str]
    phone_id: Optional[int]
    phone_number: Optional[str]
    address_line1: Optional[str]
    town_or_city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    person_address_usage_id: Optional[int]
    contact_id: Optional[str]


@dataclass
class EmergencyContactsResponse:
    """Represents the response from getting a user's emergency contacts in Oracle HCM."""

    emergency_contacts: List[EmergencyContacts]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_emergency_contacts(person_id: str) -> EmergencyContactsResponse:
    """
    Gets a user's emergency contacts in Oracle HCM.

    Args:
        person_id: The person_id of the user, returned by the `get_user_oracle_ids` tool.

    Returns:
        The user's emergency contacts.
    """
    client = get_oracle_hcm_client()
    response = client.get_request(
        "hcmContacts",
        finder_expr=f"findContactsByWorker;RelatedPersonId={person_id}",
        expand_expr="contactRelationships,names,phones,emails,addresses",
        q_expr="contactRelationships.EmergencyContactFlag=true",
        headers={"REST-Framework-Version": "4"},
    )

    if not response["items"]:
        return EmergencyContactsResponse(emergency_contacts=[])

    emergency_contacts_list = []
    for result in response["items"]:
        contact_relationships = result.get("contactRelationships", {}).get("items", [{}])
        names = result.get("names", {}).get("items", [{}])
        emails = result.get("emails", {}).get("items", [{}])
        phones = result.get("phones", {}).get("items", [{}])
        addresses = result.get("addresses", {}).get("items", [{}])

        contact_relationship = contact_relationships[0] if contact_relationships else {}
        name = names[0] if names else {}
        email = emails[0] if emails else {}
        phone = phones[0] if phones else {}
        address = addresses[0] if addresses else {}

        emergency_contacts_list.append(
            EmergencyContacts(
                contact_relationship_id=contact_relationship.get("ContactRelationshipId", None),
                name=name.get("DisplayName", ""),
                contact_type=contact_relationship.get("ContactType", ""),
                related_person_id=contact_relationship.get("RelatedPersonId", None),
                related_person_number=contact_relationship.get("RelatedPersonNumber", ""),
                email_address_id=email.get("EmailAddressId", None),
                email_address=email.get("EmailAddress", ""),
                phone_id=phone.get("PhoneId", None),
                phone_number=phone.get("PhoneNumber", ""),
                address_line1=address.get("AddressLine1", ""),
                town_or_city=address.get("TownOrCity", ""),
                state=address.get("Region2", ""),
                postal_code=address.get("PostalCode", ""),
                person_address_usage_id=address.get("PersonAddrUsageId", None),
                contact_id=get_id_from_links(result.get("links", [])[0].get("href", "")),
            )
        )

    return EmergencyContactsResponse(emergency_contacts=emergency_contacts_list)
