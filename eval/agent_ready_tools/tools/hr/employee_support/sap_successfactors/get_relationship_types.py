from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class RelationshipType:
    """A relationship type configured for a SuccessFactors deployment."""

    relationship_id: str
    relationship_type: str


@dataclass
class RelationshipTypesResponse:
    """A list of relationship types configured for a SuccessFactors deployment."""

    relationship_types: list[RelationshipType]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_relationship_types() -> RelationshipTypesResponse:
    """
    Gets a list of relationship types configured for this SuccessFactors deployment.

    Returns:
        A list of relationship types.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field="relation")

    relationship_types = RelationshipTypesResponse(
        relationship_types=[
            RelationshipType(
                relationship_id=option["id"],
                relationship_type=get_first_en_label(option["picklistLabels"]["results"]),
            )
            for option in response["d"]["picklistOptions"]["results"]
        ]
    )
    return relationship_types
