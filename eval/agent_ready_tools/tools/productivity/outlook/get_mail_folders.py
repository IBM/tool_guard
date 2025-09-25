from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class MailFolders:
    """Represents the mail folders in Microsoft Outlook."""

    folder_id: str
    display_name: str
    total_item_count: int
    is_hidden: bool


@dataclass
class MailfolderResponse:
    """A list of mail folders in Microsoft Outlook."""

    mail_folders: List[MailFolders]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_mail_folders(
    include_hidden_folders: Optional[bool] = True,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> MailfolderResponse:
    """
    Gets a list of mail folders in the Microsoft Outlook.

    Args:
        include_hidden_folders: Include hidden mail folders in Microsoft Outlook data retrieval.
        limit: Limits the number of items to retrieve/filter in Microsoft Outlook.
        skip: Skips a set number of items for pagination in Microsoft Outlook.

    Returns:
        A list of mail folders from Microsoft Outlook.
    """

    client = get_microsoft_client()
    params = {"includeHiddenFolders": include_hidden_folders, "$top": limit, "$skip": skip}
    # Filters out the parameter that are None.
    params = {key: value for key, value in params.items() if value}

    endpoint = f"{client.get_user_resource_path()}/mailFolders"
    response = client.get_request(endpoint=endpoint, params=params)
    mailfolders_list = [
        MailFolders(
            folder_id=detail.get("id"),
            display_name=detail.get("displayName"),
            total_item_count=detail.get("totalItemCount"),
            is_hidden=detail.get("isHidden"),
        )
        for detail in response.get("value", [])
    ]
    return MailfolderResponse(mail_folders=mailfolders_list)
