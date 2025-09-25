from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpsertEmergencyContactSapResult:
    """Represents the result of an emergency contact update operation in SAP SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def upsert_emergency_contact_sap(
    person_id_external: str,
    name: str,
    email: str,
    phone: str,
    relationship: str,
    is_primary: bool = False,
) -> UpsertEmergencyContactSapResult:
    """
    Updates the user's emergency contact in SAP SuccessFactors.

    Args:
        person_id_external: The user's person_id_external uniquely identifying them within the SuccessFactors API.
        name: The name of the emergency contact returned by the `get_emergency_contacts_sap` tool.
        email: The emergency contact's email returned by the `get_emergency_contacts_sap` tool.
        phone: The emergency contact's phone number returned by the `get_emergency_contacts_sap` tool.
        relationship: The emergency contact's relationship_id returned by the `get_emergency_contacts_sap` tool.
        is_primary: Whether the emergency contact is primary or not.

    Returns:
        The result from performing the update to the user's emergency contact.
    """
    client = get_sap_successfactors_client()

    primary_flag = "Y" if is_primary else "N"

    payload = {
        "__metadata": {"uri": "PerEmergencyContacts", "type": "SFOData.PerEmergencyContacts"},
        "name": name,
        "personIdExternal": person_id_external,
        "primaryFlag": primary_flag,
        "email": email,
        "phone": phone,
        "relationship": relationship,
    }

    try:
        response = client.upsert_request(payload=payload)
        return UpsertEmergencyContactSapResult(http_code=response["d"][0]["httpCode"])
    except Exception as e:  # pylint: disable=broad-except
        error_message = "An unexpected error occurred."
        if hasattr(e, "response"):
            error_response = e.response.json()
            if "d" in error_response and error_response["d"]:
                error_message = error_response["d"][0].get("message", error_message)
        print(f"Extracted error message: {error_message}")
        return UpsertEmergencyContactSapResult(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=error_message
        )
