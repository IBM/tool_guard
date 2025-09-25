from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_groups import Group, get_groups


def test_get_all_groups() -> None:
    """Tests that the groups can be retrieved by the `get_groups` tool in Microsoft Teams."""

    # Define updated test data for groups
    test_data = {
        "group_name": "CCT1-1730963289066",
        "group_id": "0057c7fe-44cc-47fa-9928-0a01a11f3cee",
        "group_mail": "CCT1-1730963289066@ibmappcon.onmicrosoft.com",
        "group_description": "description",
        "group_created_date_time": "2024-11-07T07:08:10Z",
        "group_visibility": "Public",
        "output_limit": 100,
        "output_skip": "RFNwdAIAACpHcm91cF8wYjZjYmIzMy1lMjNhLTQxNzktOWYyMy04ZmQ2ZDQyMTBiYjkqR3JvdXBfMGI2Y2JiMzMtZTIzYS00MTc5LTlmMjMtOGZkNmQ0MjEwYmI5ACpHcm91cF8xMzc4OTQzYi1mM2I1LTQ3MzctYjc0My00OGUwZjhmNGU5ZWIqR3JvdXBfMTM3ODk0M2ItZjNiNS00NzM3LWI3NDMtNDhlMGY4ZjRlOWViAAAAAAAAAAAAAAA",
    }
    limit = 100
    skip_token = "RFNwdAIAACpHcm91cF8wYjZjYmIzMy1lMjNhLTQxNzktOWYyMy04ZmQ2ZDQyMTBiYjkqR3JvdXBfMGI2Y2JiMzMtZTIzYS00MTc5LTlmMjMtOGZkNmQ0MjEwYmI5ACpHcm91cF8xMzc4OTQzYi1mM2I1LTQ3MzctYjc0My00OGUwZjhmNGU5ZWIqR3JvdXBfMTM3ODk0M2ItZjNiNS00NzM3LWI3NDMtNDhlMGY4ZjRlOWViAAAAAAAAAAAAAAA"

    # Patch `get_microsoft_client` to return our mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_groups.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "displayName": test_data["group_name"],
                    "id": test_data["group_id"],
                    "mail": test_data["group_mail"],
                    "description": test_data["group_description"],
                    "createdDateTime": test_data["group_created_date_time"],
                    "visibility": test_data["group_visibility"],
                }
            ],
            "@odata.nextLink": f"https://example.com/nextLink?$top={test_data['output_limit']}&$skiptoken={test_data['output_skip']}",
        }

        # Call the function
        response = get_groups(
            group_mail=test_data["group_mail"], limit=limit, skip_token=skip_token
        )

        # Create the expected group object with explicitly casted types
        expected_group = Group(
            group_name=str(test_data["group_name"]),
            group_id=str(test_data["group_id"]),
            group_mail=str(test_data["group_mail"]),
            group_description=str(test_data["group_description"]),
            group_created_date_time=str(test_data["group_created_date_time"]),
            group_visibility=str(test_data["group_visibility"]),
        )

        # Verify that the first group matches the expected data
        assert response.groups[0] == expected_group
        assert response.limit == test_data["output_limit"]
        assert response.skip_token == test_data["output_skip"]

        # Ensure the API call was made with the expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="groups",
            params={
                "$top": limit,
                "$skiptoken": skip_token,
                "$filter": f"mail eq '{test_data['group_mail']}'",
            },
        )
