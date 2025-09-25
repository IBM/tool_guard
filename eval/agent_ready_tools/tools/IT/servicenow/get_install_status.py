from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class InstallStatus:
    """Represents single install status object in ServiceNow."""

    install_status: str
    system_id: str


@dataclass
class InstallStatusResponse:
    """A response containing the list of install status."""

    install_status_list: list[InstallStatus]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_install_status(
    install_status: Optional[str] = None, system_id: Optional[str] = None
) -> InstallStatusResponse:
    """
    Gets a list of install status records.

    Args:
        install_status: The name of the install status.
        system_id: The unique system id of the install status.

    Returns:
        A list of install status records.
    """

    client = get_servicenow_client()

    params: dict[str, Any] = {
        "name": "alm_asset",
        "element": "install_status",
        "label": install_status,
        "sys_id": system_id,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="sys_choice", params=params)

    install_status_list: list[InstallStatus] = [
        InstallStatus(
            install_status=status.get("label", ""),
            system_id=status.get("sys_id", ""),
        )
        for status in response["result"]
    ]

    return InstallStatusResponse(install_status_list=install_status_list)
