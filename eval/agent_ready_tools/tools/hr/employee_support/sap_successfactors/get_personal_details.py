from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class PersonalDetailsResponse:
    """Represents a user's personal details in SAP SuccessFactors."""

    first_name: str = ""
    last_name: str = ""
    nationality: str = ""
    gender: str = ""
    country: str = ""


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_personal_details(person_id_external: str) -> PersonalDetailsResponse:
    """
    Gets a user's personal details in SAP SuccessFactors.

    Args:
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API.

    Returns:
        The user's personal details.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        entity="PerPerson",
        filter_expr=f"personIdExternal eq '{person_id_external}'",
        expand_expr="personalInfoNav,nationalIdNav",
    )

    res_data = response.get("d", {}).get("results", None)
    results = PersonalDetailsResponse()

    if res_data and len(res_data) > 0:
        res_data = res_data[0]
        personal_info = res_data.get("personalInfoNav", None).get("results", None)
        national_id_info = res_data.get("nationalIdNav", None).get("results", None)
        if personal_info and len(personal_info) > 0:
            personal_info = personal_info[0]

            results.first_name = personal_info.get("firstName", "")
            results.last_name = personal_info.get("lastName", "")
            results.nationality = personal_info.get("nationality", "")
            results.gender = personal_info.get("gender", "")

        if national_id_info and len(national_id_info) > 0:
            national_id_info = national_id_info[0]
            results.country = national_id_info.get("country", "")

    return results
