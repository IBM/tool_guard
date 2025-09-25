from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.zendesk_get_organizations import (
    Organization,
    zendesk_get_organizations,
)


def test_zendesk_get_organizations_first_item() -> None:
    """Tests that the first Zendesk organization in the response matches the expected data."""

    organization_id = "48664574656793"
    custom_fields = {
        "emp_id": "12345",
        "fulltime": False,
        "grade": None,
        "join_date": "2025-07-09T00:00:00+00:00",
        "org": "my org",
        "position": "major",
        "positions": "bengaluru",
        "url": None,
    }
    test_data = {
        "name": "Pruthvi org",
        "created_at": "2025-07-08T03:49:39Z",
        "group_id": "22933923432985",
        "domain_names": ["myorg.com"],
        "notes": "",
        "details": "",
        "tags": ["major"],
    }

    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = 2
    output_per_page = 5

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_get_organizations.get_zendesk_client"
    ) as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "results": [
                {
                    "id": organization_id,
                    "name": test_data["name"],
                    "created_at": test_data["created_at"],
                    "group_id": test_data["group_id"],
                    "domain_names": test_data["domain_names"],
                    "notes": test_data["notes"],
                    "details": test_data["details"],
                    "tags": test_data["tags"],
                    "organization_fields": custom_fields,
                }
            ],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/organizations?page=2&per_page=5",
        }

        # Patch pagination helper if needed
        with patch(
            "agent_ready_tools.utils.get_id_from_links.get_query_param_from_links"
        ) as mock_get_query_params:
            mock_get_query_params.return_value = {
                "page": str(output_page),
                "per_page": str(output_per_page),
            }

            # Call the function
            response = zendesk_get_organizations(per_page=per_page, page=page)

            # Expected first organization
            expected_first_organization = Organization(
                organization_id=str(organization_id),
                name=str(test_data["name"]),
                created_at=str(test_data["created_at"]),
                group_id=str(test_data["group_id"]),
                domain_names=list(test_data["domain_names"]),
                notes=str(test_data["notes"]),
                details=str(test_data["details"]),
                tags=list(test_data["tags"]),
                custom_fields=custom_fields,
            )

            # Assertions
            assert response.organizations[0] == expected_first_organization
            assert response.page == output_page
            assert response.per_page == output_per_page

            # Assert correct API call
            mock_client.get_request.assert_called_once_with(
                entity="search",
                params={
                    "query": "type:organization",
                    "per_page": per_page,
                    "page": page,
                },
            )
