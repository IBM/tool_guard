from typing import Any, List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class ListItem:
    """Represents the details of an item in a list in Microsoft Sharepoint."""

    fields: dict[str, Any]


@dataclass
class ListItemsResponse:
    """Represents a list of items from a list in Microsoft Sharepoint."""

    list_items: List[ListItem]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_list_items(site_id: str, list_name: str) -> ListItemsResponse:
    """
    Retrieves a list of items from a list in Microsoft Sharepoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        list_name: The name of the list in Microsoft Sharepoint is returned by the `get_lists` tool.

    Returns:
        A list of items in a list.
    """

    client = get_microsoft_client()
    params = {"expand": "fields"}

    response = client.get_request(
        endpoint=f"sites/{site_id}/lists/{list_name}/items", params=params
    )

    # Removing these parameters because they are common for every item in the lists and not specific to individual entries.
    remove_fields = [
        "@odata.etag",
        "LinkTitleNoMenu",
        "LinkTitle",
        "id",
        "ContentType",
        "Modified",
        "Created",
        "AuthorLookupId",
        "EditorLookupId",
        "_UIVersionString",
        "Edit",
        "ItemChildCount",
        "FolderChildCount",
        "AppEditorLookupId",
        "_ComplianceFlags",
        "_ComplianceTag",
        "_ComplianceTagWrittenTime",
        "_ComplianceTagUserId",
    ]

    list_items: List[ListItem] = []

    for item in response.get("value", []):
        fields = item.get("fields", {})

        final_fields = {key: value for key, value in fields.items() if key not in remove_fields}

        list_items.append(ListItem(fields=final_fields))

    return ListItemsResponse(list_items=list_items)
