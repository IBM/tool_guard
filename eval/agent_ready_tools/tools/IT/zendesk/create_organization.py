from http import HTTPStatus
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CreateOrganizationResponse:
    """Represents the result of creating an organization in Zendesk."""

    id: Optional[str] = None
    organization_name: Optional[str] = None
    message: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def create_organization(
    organization_name: str, domain_name: Optional[str] = None
) -> CreateOrganizationResponse:
    """
    Creates an organization in Zendesk.

    Args:
        organization_name: The name of the organization in Zendesk.
        domain_name: The domain names of email addresses of the users separated by commas from Zendesk.

    Returns:
        Details of the created organization in Zendesk.
    """
    try:
        client = get_zendesk_client()

        payload: dict[str, Any] = {"organization": {"name": organization_name}}

        if domain_name:
            payload["organization"]["domain_names"] = domain_name.split(",")

        response = client.post_request(entity="organizations", payload=payload)

        organization_data = response.get("organization", {})

        return CreateOrganizationResponse(
            id=str(organization_data.get("id", "")),
            organization_name=organization_data.get("name", ""),
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        message = (
            error_response.get("details", {}).get("name", [])[0].get("description", "")
            if error_response
            else "An unexpected error occurred."
        )
        return CreateOrganizationResponse(
            message=message,
            http_code=(
                e.response.status_code
                if e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )

    except Exception as e:  # pylint: disable=broad-except
        return CreateOrganizationResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            message=str(e),
        )
