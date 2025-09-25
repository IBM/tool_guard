import json
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UpdateOrganizationResponse:
    """Represents the result of updating an organization in Zendesk."""

    organization_id: Optional[str] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def update_organization(
    organization_id: str,
    name: Optional[str] = None,
    shared_tickets: Optional[bool] = None,
    shared_comments: Optional[bool] = None,
    external_id: Optional[str] = None,
    domain_names: Optional[str] = None,
    details: Optional[str] = None,
    notes: Optional[str] = None,
    group_id: Optional[str] = None,
    tags: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
) -> UpdateOrganizationResponse:
    """
    Updates an organization details in Zendesk.

    Args:
        organization_id: The unique identifier of the organization to be updated, returned by the `get_organizations` tool.
        name: The name of the organization.
        shared_tickets: Whether end users in this organization can see each other's tickets.
        shared_comments: Whether end users in this organization can comment on each other's tickets.
        external_id: A unique external ID to associate organizations with an external record.
        domain_names: The domain names associated with this organization.
        details: The details about the organization, such as the address.
        notes: Notes about the organization.
        group_id: The unique identifier of the group, returned by the 'get_groups' tool.
        tags: The tags of the organization.
        custom_fields: Custom fields associated with the organization (e.g., emp_id: 87658, org: nothing1).

    Returns:
        The updated organization details.
    """
    client = get_zendesk_client()

    payload = {
        "organization": {
            "name": name,
            "shared_tickets": shared_tickets,
            "shared_comments": shared_comments,
            "external_id": external_id,
            "domain_names": [domain_names] if domain_names else None,
            "details": details,
            "notes": notes,
            "group_id": group_id,
            "tags": [tags] if tags else None,
            "organization_fields": custom_fields,
        }
    }

    # Handling custom fields
    if custom_fields:
        custom_fields_dict = (
            json.loads(custom_fields) if isinstance(custom_fields, str) else custom_fields
        )

        payload["organization"]["organization_fields"] = custom_fields_dict

    payload["organization"] = {
        key: value for key, value in payload.get("organization", {}).items() if value is not None
    }

    try:
        response = client.patch_request(entity=f"organizations/{organization_id}", payload=payload)
        organization = response.get("organization", {})

        return UpdateOrganizationResponse(organization_id=str(organization.get("id", "")))

    except HTTPError as e:
        error_response = e.response.json()
        http_code = e.response.status_code
        if http_code == 400:
            error_message = error_response.get("error", {}).get("title", "")
            error_description = error_response.get("error", {}).get("message", "")
        else:
            error_message = error_response.get("error", "")
            error_description = error_response.get("description", "")
        return UpdateOrganizationResponse(
            error_message=error_message,
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return UpdateOrganizationResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
