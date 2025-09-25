from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdateEmailResult:
    """Represents the result of an email update operation in SAP SuccessFactors."""

    http_code: int
    messages: Optional[list[str]] = None


def upsert_primary_email(
    email_address: str, email_type_id: str, person_id_external: str
) -> UpdateEmailResult:
    """
    Upserts a primary email address for a given user.

    This function performs a full upsert (with
    purgeType=Full) of all the user's email records:

    - Fetches current primary email for the user
    - Marks existing primary email as non-primary
    - Adds the new email record as primary
    - Sends the both emails back to the server, replacing the current state

    This approach ensures compliance with SuccessFactors' requirement that each user must have exactly one primary email.

    Args:
        email_address: The email address.
        email_type_id: The picklist option ID of the email type matching one of the cases returned
            by the `get_email_types_sap` tool.
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API.

    Returns:
        An UpdateEmailResult indicating success or containing error details.
    """

    client = get_sap_successfactors_client()

    # 1. Create the new email record
    new_email = {
        "__metadata": {"uri": "PerEmail", "type": "SFOData.PerEmail"},
        "personIdExternal": person_id_external,
        "emailType": email_type_id,
        "emailAddress": email_address,
        "isPrimary": True,
    }

    # 2. Get current primary emails
    existing_emails = client.get_request(
        entity="PerEmail",
        filter_expr=f"personIdExternal eq '{person_id_external}' and isPrimary eq true",
        select_expr="personIdExternal,emailType,emailAddress,isPrimary",
    )["d"]["results"]

    existing_email = existing_emails[0] if existing_emails else {}

    # 3. If current primary email has the same type as new primary, or the user doesn't have the primary email yet call ordinary update
    if not existing_emails or existing_email.get("emailType") == email_type_id:
        response = client.upsert_request(payload=new_email)
        return UpdateEmailResult(
            http_code=response["d"][0]["httpCode"],
            messages=[
                res_data["message"]
                for res_data in response["d"]
                if res_data.get("message") is not None
            ],
        )

    # 4. Set current email to isPrimary: false
    existing_email["isPrimary"] = False
    existing_email["__metadata"] = {"uri": "PerEmail", "type": "SFOData.PerEmail"}

    # 4. Combine and send
    updated_emails = [existing_email, new_email]
    response = client.upsert_request(payload=updated_emails, purge_type_full=True)
    return UpdateEmailResult(
        http_code=max(response["d"], key=lambda item: item["httpCode"])["httpCode"],
        messages=[
            res_data["message"] for res_data in response["d"] if res_data.get("message") is not None
        ],
    )


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_email(
    email_address: str, email_type_id: str, person_id_external: str, is_primary: Optional[bool]
) -> UpdateEmailResult:
    """
    Updates a user's email address in SAP SuccessFactors.

    Args:
        email_address: The email address.
        email_type_id: The picklist option ID of the email type matching one of the cases returned
            by the `get_email_types_sap` tool.
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API.
        is_primary: Indicates whether this is the primary email for the user.

    Returns:
        The result from performing the update to the user's email.
    """
    client = get_sap_successfactors_client()

    payload: dict[str, Any] = {
        "__metadata": {"uri": "PerEmail", "type": "SFOData.PerEmail"},
        "personIdExternal": person_id_external,
        "emailType": email_type_id,
        "emailAddress": email_address,
        "isPrimary": False,
    }
    if is_primary:
        # If the new email address should be primary, we perform a full upsert of all email records.
        # This is required because SuccessFactors enforces that a user must always have exactly one primary email.
        # To update the primary, we must send the complete list of email records:
        #   - mark existing primary emails as non-primary
        #   - include the new email as the only primary
        # We use purgeType=Full so that the server replaces all existing email records with the ones we provide.
        return upsert_primary_email(
            email_address=email_address,
            email_type_id=email_type_id,
            person_id_external=person_id_external,
        )

    response = client.upsert_request(payload=payload)
    return UpdateEmailResult(
        http_code=response["d"][0]["httpCode"],
        messages=[
            res_data["message"] for res_data in response["d"] if res_data.get("message") is not None
        ],
    )
