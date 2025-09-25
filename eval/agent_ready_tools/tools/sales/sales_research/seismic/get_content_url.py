from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.seismic_client import SeismicClient, get_seismic_client
from agent_ready_tools.utils.tool_credentials import SEISMIC_CONNECTIONS


@dataclass
class GetContentURLResponse:
    """Download link for content in Seismic deployment."""

    url: Optional[str] = None


@tool(expected_credentials=SEISMIC_CONNECTIONS)
def get_content_url(workspace_id: str) -> GetContentURLResponse:
    """
    Get a content's URL in Seismic for download.

    Args:
        workspace_id: The content's workspace id.

    Returns:
        URL to requested content.
    """
    client = get_seismic_client()

    custom_path_suffix = "/".join(["files", workspace_id, "content"])

    # TODO: category and endpoint should be managed somewhere else.
    response = client.get_request(
        category=SeismicClient.INTEGRATION,
        endpoint="workspace",
        custom_path_suffix=custom_path_suffix,
        params={
            "redirect": "false",
        },
    )

    download_content_response = GetContentURLResponse(
        url=response.get("downloadUrl"),
    )
    return download_content_response
