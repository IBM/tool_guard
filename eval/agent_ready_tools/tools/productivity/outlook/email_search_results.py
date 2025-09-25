from http import HTTPStatus
import json
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class EmailSearchResult:
    """Represents the result of using a search term to find a particular email in Microsoft
    Outlook."""

    subject: Optional[str]
    body: Optional[str]
    recipient_name: str
    created_date_time: str
    sender_email_address: str


@dataclass
class EmailSearchResponse:
    """Represents a list of emails that match the search term in Microsoft Outlook."""

    searchemail: Optional[List[EmailSearchResult]] = None
    limit: Optional[int] = None
    skip_token: Optional[str] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def email_search_results(
    search_term: str, limit: Optional[int] = 10, skip_token: Optional[str] = None
) -> EmailSearchResponse:
    """
    Searches for an email using a search term in Microsoft Outlook.

    Args:
        search_term: The string that needs to be searched to fetch an email.
        limit: The number of records to retrieve.
        skip_token: The number of records to skip for pagination.

    Returns:
        A list of emails containing the specified search term.
    """

    client = get_microsoft_client()

    params = {
        "$search": search_term,
        "$top": limit,
        "$skiptoken": skip_token,
    }
    params = {key: value for key, value in params.items() if value}

    try:
        response = client.get_request(
            endpoint=f"{client.get_user_resource_path()}/messages", params=params
        )

        searchemail_list = [
            EmailSearchResult(
                subject=record.get("subject", ""),
                body=record.get("bodyPreview", ""),
                recipient_name=record.get("toRecipients", [{}])[0]
                .get("emailAddress", {})
                .get("name", ""),
                created_date_time=record.get("createdDateTime", ""),
                sender_email_address=record.get("sender", {})
                .get("emailAddress", {})
                .get("address", ""),
            )
            for record in response.get("value", [])
        ]

        # Extract limit and skiptoken from @odata.nextLink if it exists
        output_limit = None
        output_skiptoken = None
        next_api_link = response.get("@odata.nextLink", "")
        if next_api_link:
            query_params = get_query_param_from_links(next_api_link)
            output_limit = int(query_params["$top"])
            output_skiptoken = query_params.get("$skiptoken")

        return EmailSearchResponse(
            searchemail=searchemail_list,
            limit=output_limit,
            skip_token=output_skiptoken,
        )
    except HTTPError as e:
        error_message = ""
        try:
            # Try to parse the JSON error response from the API
            error_response = e.response.json()
            error_message = error_response.get("error", {}).get("message", "")
        except json.JSONDecodeError:
            # Fallback for non-JSON error responses (e.g., HTML from a proxy)
            error_message = e.response.text or "An HTTP error occurred without a JSON response."

        return EmailSearchResponse(
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return EmailSearchResponse(
            error_message=str(e), http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
        )
