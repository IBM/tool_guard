from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdatePhoneResult:
    """Represents the result of a phone update operation in SAP SuccessFactors."""

    http_code: int
    messages: Optional[List[str]] = None


def upsert_primary_phone(
    area_code: Optional[str],
    country_code: Optional[str],
    extension: Optional[str],
    person_id_external: str,
    phone_number: Optional[str],
    phone_type: str,
) -> UpdatePhoneResult:
    """
    Upserts a primary phone number for a given user This function performs a full upsert (with
    purgeType=Full) of all the user's phone records:

    - Fetches current primary phone for the user
    - Marks existing primary phone as non-primary
    - Adds the new phone record as primary
    - Sends the both phones back to the server, replacing the current state

    This approach ensures compliance with SuccessFactors' requirement that each user must have exactly one primary phone.

    Args:
        area_code: Optional area code for the phone number.
        country_code: Optional country code for the phone number.
        extension: Optional phone extension.
        person_id_external: The external ID of the person in SuccessFactors.
        phone_number: The phone number to upsert.
        phone_type: The type of phone number (e.g., "CELL", "HOME", "BUSINESS").

    Returns:
        An UpdatePhoneResult indicating success or containing error details.
    """

    client = get_sap_successfactors_client()

    # 1. Create the new phone record
    new_phone = {
        "__metadata": {"uri": "PerPhone", "type": "SFOData.PerPhone"},
        "areaCode": area_code,
        "countryCode": country_code,
        "extension": extension,
        "isPrimary": True,
        "personIdExternal": person_id_external,
        "phoneNumber": phone_number,
        "phoneType": phone_type,
    }

    # 2. Get current primary phones
    existing_phones = client.get_request(
        entity="PerPhone",
        filter_expr=f"personIdExternal eq '{person_id_external}' and isPrimary eq true",
        select_expr="personIdExternal,phoneType,phoneNumber,isPrimary,extension,countryCode,areaCode",
    )["d"]["results"]

    existing_phone = existing_phones[0] if existing_phones else {}

    # 3. If current primary phone has the same type as new primary, or the user doesn't have the primary number yet call ordinary update
    if not existing_phones or existing_phone.get("phoneType") == phone_type:
        response = client.upsert_request(payload=new_phone)
        return UpdatePhoneResult(
            http_code=response["d"][0]["httpCode"],
            messages=[
                res_data["message"] for res_data in response["d"] if res_data["message"] is not None
            ],
        )

    # 4. Set current phone to isPrimary: false
    existing_phone["isPrimary"] = False
    existing_phone["__metadata"] = {"uri": "PerPhone", "type": "SFOData.PerPhone"}

    # 4. Combine and send
    updated_phones = [existing_phone, new_phone]
    response = client.upsert_request(payload=updated_phones, purge_type_full=True)
    return UpdatePhoneResult(
        http_code=max(response["d"], key=lambda item: item["httpCode"])["httpCode"],
        messages=[
            res_data["message"] for res_data in response["d"] if res_data["message"] is not None
        ],
    )


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_phone(
    is_primary: bool,
    person_id_external: str,
    phone_type_id: str,
    area_code: Optional[str] = None,
    country_code: Optional[str] = None,
    extension: Optional[str] = None,
    phone_number: Optional[str] = None,
) -> UpdatePhoneResult:
    """
    Updates a user's phone number in SAP SuccessFactors.

    Args:
        is_primary: Indicates whether this is the primary phone number for the user.
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API.
        phone_type_id: The phone type's id matching one of the cases returned by the
            `get_phone_types_sap` tool.
        area_code: The area code associated with the phone number.
        country_code: The country code associated with the phone number.
        extension: The extension associated with the phone number.
        phone_number: The phone number.

    Returns:
        The result from performing the update to the user's phone.
    """
    client = get_sap_successfactors_client()

    payload = {
        "__metadata": {"uri": "PerPhone", "type": "SFOData.PerPhone"},
        "areaCode": area_code,
        "countryCode": country_code,
        "extension": extension,
        "isPrimary": is_primary,
        "personIdExternal": person_id_external,
        "phoneNumber": phone_number,
        "phoneType": phone_type_id,
    }
    if is_primary:
        # If the new phone number should be primary, we perform a full upsert of all phone records.
        # This is required because SuccessFactors enforces that a user must always have exactly one primary phone.
        # To update the primary, we must send the complete list of phone records:
        #   - mark existing primary phones as non-primary
        #   - include the new phone as the only primary
        # We use purgeType=Full so that the server replaces all existing phone records with the ones we provide.
        return upsert_primary_phone(
            area_code,
            country_code,
            extension,
            person_id_external,
            phone_number,
            phone_type_id,
        )

    response = client.upsert_request(payload=payload)
    return UpdatePhoneResult(
        http_code=response["d"][0]["httpCode"],
        messages=[
            res_data["message"] for res_data in response["d"] if res_data["message"] is not None
        ],
    )
