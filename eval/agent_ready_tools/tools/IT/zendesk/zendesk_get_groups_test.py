from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.zendesk_get_groups import Group, zendesk_get_groups


def test_get_groups_first_item() -> None:
    """Tests that the first Zendesk group in the response matches the expected data."""

    # Define test data based on the provided response file
    group_id = 22933923432985
    test_data = {
        "name": "ACE Zendesk Group",
        "is_public": True,
        "created_at": "2023-09-13T11:04:18Z",
        "updated_at": "2025-07-07T05:28:33Z",
        "user_ids": [
            903556258786,
            16722876680089,
            35376705273369,
        ],
        "description": "Test description for the group.",
    }

    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = 2
    output_per_page = 5

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_get_groups.get_zendesk_client"
    ) as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "results": [
                {
                    "id": group_id,
                    "name": test_data["name"],
                    "is_public": test_data["is_public"],
                    "created_at": test_data["created_at"],
                    "updated_at": test_data["updated_at"],
                    "user_ids": test_data["user_ids"],
                    "description": test_data["description"],
                }
            ],
            "users": [
                {"id": 903556258786, "name": "pratik"},
                {"id": 16722876680089, "name": "Alison Lucas"},
                {"id": 35376705273369, "name": "vae"},
            ],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/groups?page=2&per_page=5",
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
            response = zendesk_get_groups(per_page=per_page, page=page)

            # Expected first group
            expected_first_group = Group(
                group_id=str(group_id),
                name=str(test_data["name"]),
                is_public=bool(test_data["is_public"]),
                created_at=str(test_data["created_at"]),
                updated_at=str(test_data["updated_at"]),
                user_names=["pratik", "Alison Lucas", "vae"],
                description="Test description for the group.",
            )

            # Assertions
            assert response.groups[0] == expected_first_group
            assert response.page == output_page
            assert response.per_page == output_per_page

            # Assert correct API call
            mock_client.get_request.assert_called_once_with(
                entity="search",
                params={
                    "query": "type:group",
                    "per_page": per_page,
                    "page": page,
                    "include": "groups(users)",
                },
            )
