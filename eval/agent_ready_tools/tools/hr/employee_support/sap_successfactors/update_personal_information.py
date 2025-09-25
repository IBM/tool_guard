from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdatePersonalInformationResult:
    """Represents the result of the update to a user's personal information in SAP
    SuccessFactors."""

    http_code: int


# TODO Uncomment input parameters once the necessary support for them has been added
@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_personal_information(
    person_id_external: str,
    preferred_name: Optional[str],
    start_date: str,
    # first_name: Optional[str] = None,
    # first_name_alt1: Optional[str] = None,
    # gender: Optional[str] = None,
    # last_name: Optional[str] = None,
    # last_name_alt1: Optional[str] = None,
    # marital_status: Optional[str] = None,
    # middle_name: Optional[str] = None,
    # middle_name_alt1: Optional[str] = None,
    # nationality: Optional[str] = None,
    # native_preferred_lang: Optional[str] = None,
    # salutation: Optional[str] = None,
    # suffix: Optional[str] = None,
) -> UpdatePersonalInformationResult:
    """
    Updates a user's personal information in SAP SuccessFactors.

    Args:
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API.
        preferred_name: The employee's preferred name.
        start_date: The start date associated with the profile change in ISO 8601 format (e.g.,
            YYYY-MM-DD).

    Returns:
        The result from performing the update to the user's personal information.
    """
    client = get_sap_successfactors_client()

    payload = {
        "__metadata": {"uri": "PerPersonal", "type": "SFOData.PerPersonal"},
        "personIdExternal": person_id_external,
        "preferredName": preferred_name,
        "startDate": iso_8601_to_sap_date(start_date),
        # "firstName": first_name,
        # "firstNameAlt1": first_name_alt1,
        # "gender": gender,
        # "lastName": last_name,
        # "lastNameAlt1": last_name_alt1,
        # "maritalStatus": marital_status,
        # "middleName": middle_name,
        # "middleNameAlt1": middle_name_alt1,
        # "nationality": nationality,
        # "nativePreferredLang": native_preferred_lang,
        # "salutation": salutation,
        # "suffix": suffix,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.upsert_request(payload=payload)
    return UpdatePersonalInformationResult(http_code=response["d"][0]["httpCode"])
