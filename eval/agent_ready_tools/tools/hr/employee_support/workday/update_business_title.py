from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class UpdateBusinessTitleResponse:
    """Represents the result of a business title update operation in Workday."""

    change_description: str
    new_business_title: str


# TODO Investigate whether you need specific permissions to perform this update
@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def update_business_title(user_id: str, new_business_title: str) -> UpdateBusinessTitleResponse:
    """
    Updates a user's business title in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        new_business_title: The new business title for the user.

    Returns:
        The result from performing the update to the user's business title.
    """
    client = get_workday_client()
    response = client.update_business_title(
        user_id=user_id, payload={"proposedBusinessTitle": new_business_title}
    )
    return UpdateBusinessTitleResponse(
        change_description=response.get("descriptor", ""),
        new_business_title=response.get("proposedBusinessTitle", ""),
    )
