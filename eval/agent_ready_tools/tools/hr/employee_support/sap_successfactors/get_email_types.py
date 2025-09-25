from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class EmailType:
    """An email type configured for a SuccessFactors deployment."""

    id: str
    label: str


@dataclass
class EmailTypesResponse:
    """A list of email types configured for a SuccessFactors deployment."""

    email_types: list[EmailType]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_email_types_sap() -> EmailTypesResponse:
    """
    Gets a list of email types configured for this SuccessFactors deployment.

    Returns:
        A list of email types.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options("ecEmailType")

    email_types = EmailTypesResponse(
        email_types=[
            EmailType(
                id=option["id"], label=get_first_en_label(option["picklistLabels"]["results"])
            )
            for option in response["d"]["picklistOptions"]["results"]
        ]
    )
    return email_types
