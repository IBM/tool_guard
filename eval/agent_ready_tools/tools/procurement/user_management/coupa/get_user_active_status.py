from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_user_active_status(login_name: str) -> bool:
    """
    Returns whether the given user login name is an active user in Coupa.

    Args:
        login_name: user login name in Coupa.

    Returns:
        bool of whether the user is active or not.
    """
    client = get_coupa_client(scope=["core.user.read"])

    params = {"status": "active", "login": login_name}

    response = client.get_request_list(resource_name="users", params=params)

    # True if response, False empty list if user does not exist or inactive
    return bool(response)
