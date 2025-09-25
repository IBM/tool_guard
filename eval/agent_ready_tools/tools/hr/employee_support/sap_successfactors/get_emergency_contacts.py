from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class SAPEmergencyContact:
    """Represents the details of an emergency contact for a user in SAP SuccessFactors."""

    name: str
    relationship: str
    relationship_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_primary: Optional[bool] = False


@dataclass
class SAPEmergencyContactResponse:
    """A list of emergency contacts for an employee configured in SAP SuccessFactors."""

    emergency_contacts: List[SAPEmergencyContact]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_emergency_contacts_sap(person_id: str) -> SAPEmergencyContactResponse:
    """
    Get a worker's emergency contacts in SAP SuccessFactors.

    Args:
        person_id: The employee's user ID uniquely identifying them within the SuccessFactors API.

    Returns:
        A list of emergency contacts.
    """
    client = get_sap_successfactors_client()
    response = client.get_request(
        entity="PerEmergencyContacts",
        filter_expr=f"personIdExternal eq '{person_id}'",
        expand_expr="relationshipNav",
    )

    results = response.get("d", {}).get("results", [])
    emergency_contacts_list = []

    for contact in results:
        primary_flag = contact.get("primaryFlag", "N")
        is_primary_bool = primary_flag.upper() == "Y"

        emergency_contacts_list.append(
            SAPEmergencyContact(
                name=contact.get("name", ""),
                email=contact.get("email"),
                phone=contact.get("phone"),
                relationship=contact.get("relationshipNav", {}).get("externalCode", ""),
                relationship_id=contact.get("relationship", ""),
                is_primary=is_primary_bool,
            )
        )

    return SAPEmergencyContactResponse(emergency_contacts=emergency_contacts_list)
