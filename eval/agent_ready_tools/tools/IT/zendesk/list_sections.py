from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class Section:
    """Represents the class for retrieving the sections in Zendesk."""

    section_id: str
    section_name: str
    section_locale: str


@dataclass
class ListSectionsResponse:
    """Represents the response for retrieving sections in Zendesk."""

    sections: List[Section]
    per_page: Optional[int]
    page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def list_sections(
    section_name: Optional[str] = None, per_page: Optional[int] = 10, page: Optional[int] = 1
) -> ListSectionsResponse:
    """
    Gets a list of sections from Zendesk.

    Args:
        section_name: The name of the section in Zendesk.
        per_page: Number of sections to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of sections.
    """

    try:
        client = get_zendesk_client()

        params = {"name": section_name, "per_page": per_page, "page": page}

        params = {key: value for key, value in params.items() if value}

        entity = "help_center/en-us/sections"
        response = client.get_request(entity=entity, params=params)

        sections: List[Section] = [
            Section(
                section_id=str(result.get("id", "")),
                section_name=result.get("name", ""),
                section_locale=result.get("locale", ""),
            )
            for result in response.get("sections", [])
        ]
        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return ListSectionsResponse(
            sections=sections,
            page=output_page,
            per_page=output_per_page,
        )

    except HTTPError as e:
        error_response = e.response.json()
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return ListSectionsResponse(
            sections=[],
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return ListSectionsResponse(
            sections=[],
            page=None,
            per_page=None,
            http_code=500,
            error_message=str(e),
        )
