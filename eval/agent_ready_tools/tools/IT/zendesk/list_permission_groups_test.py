from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.list_permission_groups import (
    PermissionGroup,
    list_permission_groups,
)


def test_list_permission_group() -> None:
    """Verifies that the `list_permission_groups` tool can successfully retrieve Zendesk permission
    groups."""

    # Define the test data
    test_data: dict[str, int | str] = {
        "permission_group_id": "4412080508697",
        "permission_group_name": "Admins",
    }

    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = 2
    output_per_page = 5

    # patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.list_permission_groups.get_zendesk_client"
    ) as mock_zendesk_client:
        # create mock client
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client

        # mock the API response
        mock_client.get_request.return_value = {
            "permission_groups": [
                {
                    "id": test_data["permission_group_id"],
                    "name": test_data["permission_group_name"],
                }
            ],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/v2/guide/permission_groups?page=2&per_page=5",
        }

        with patch(
            "agent_ready_tools.utils.get_id_from_links.get_query_param_from_links"
        ) as mock_get_query_params:
            mock_get_query_params.return_value = {
                "name": test_data["permission_group_name"],
                "page": str(output_page),
                "per_page": str(output_per_page),
            }

            # Call the function
            response = list_permission_groups(
                permission_group_name=test_data["permission_group_name"],
                per_page=per_page,
                page=page,
            )

            # Ensure that list_permission_groups() has executed and returned proper values.
            expected_output = PermissionGroup(
                permission_group_id=str(test_data["permission_group_id"]),
                permission_group_name=str(test_data["permission_group_name"]),
            )
            print(response)
            print(expected_output)
            assert response.permission_groups[0] == expected_output
            assert response.page == output_page
            assert response.per_page == output_per_page

            # Ensure the API call was made with expected parameters
            mock_client.get_request.assert_called_once_with(
                entity="guide/permission_groups",
                params={
                    "name": test_data["permission_group_name"],
                    "per_page": per_page,
                    "page": page,
                },
            )
