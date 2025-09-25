from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class PhoneType:
    """An email type configured for a SuccessFactors deployment."""

    id: str
    label: str


@dataclass
class PhoneTypesResponse:
    """A list of phone types configured for a SuccessFactors deployment."""

    phone_types: list[PhoneType]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_phone_types_sap() -> PhoneTypesResponse:
    """
    Gets a list of phone types configured for this SuccessFactors deployment.

    Returns:
        A list of phone types.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field="ecPhoneType")

    phone_types = [
        PhoneType(
            id=option["id"], label=get_first_en_label(labels=option["picklistLabels"]["results"])
        )
        for option in response["d"]["picklistOptions"]["results"]
    ]
    return PhoneTypesResponse(phone_types=phone_types)
