from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class ActionDetails:
    """Represents the action details of a worker."""

    action_name: str
    action_id: int


@dataclass
class ActionDetailsResponse:
    """Represents the response from retrieving action details of a worker."""

    action_details_list: List[ActionDetails]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_action_ids() -> ActionDetailsResponse:
    """
    Retrieves the action details of a worker in Oracle HCM.

    Returns:
        The worker's action details
    """
    client = get_oracle_hcm_client()

    response = client.get_request("actionsLOV")

    action_details_list: List[ActionDetails] = [
        ActionDetails(
            action_name=result.get("ActionName"),
            action_id=result.get("ActionId"),
        )
        for result in response["items"]
    ]

    return ActionDetailsResponse(action_details_list=action_details_list)
