from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.list_user_segments import UserSegment, list_user_segments


def test_list_user_segment() -> None:
    """Verifies that the `list_user_segments` tool can successfully retrieve Zendesk helpcenter user
    segments."""

    # Define the test data
    test_data: dict[str, int | str] = {
        "user_segment_id": "4412087522713",
        "user_type": "staff",
        "user_segment_name": "Agents and admins",
    }

    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = 2
    output_per_page = 5

    # patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.list_user_segments.get_zendesk_client"
    ) as mock_zendesk_client:
        # create mock client
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client

        # mock the API response
        mock_client.get_request.return_value = {
            "user_segments": [
                {
                    "id": test_data["user_segment_id"],
                    "user_type": test_data["user_type"],
                    "name": test_data["user_segment_name"],
                }
            ],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/v2/help_center/user_segments?page=2&per_page=5",
        }

        # Patch pagination helper if needed
        with patch(
            "agent_ready_tools.utils.get_id_from_links.get_query_param_from_links"
        ) as mock_get_query_params:
            mock_get_query_params.return_value = {
                "name": test_data["user_segment_name"],
                "page": str(output_page),
                "per_page": str(output_per_page),
            }

        # List Zendesk user segments.
        response = list_user_segments(
            user_segment_name=test_data["user_segment_name"], per_page=per_page, page=page
        )

        # Ensure that list_user_segments() has executed and returned proper values.
        expected_output = UserSegment(
            user_segment_id=str(test_data["user_segment_id"]),
            user_type=str(test_data["user_type"]),
            user_segment_name=str(test_data["user_segment_name"]),
        )

        assert response.user_segments[0] == expected_output
        assert response.page == output_page
        assert response.per_page == output_per_page

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="help_center/user_segments",
            params={
                "name": test_data["user_segment_name"],
                "per_page": per_page,
                "page": page,
            },
        )
