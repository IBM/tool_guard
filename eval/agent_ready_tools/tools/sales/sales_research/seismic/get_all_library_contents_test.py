from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.seismic.get_all_library_contents import (
    get_all_library_contents,
)


def test_get_all_library_contents() -> None:
    """Test that the `get_all_library_contents` function returns the expected response."""

    # Define test data:
    test_data = {
        "document_id": "DSAADD1ED231",
        "created_at_start_time": "2019-06-18T16:29:37.960Z",
        "created_at_end_time": "2019-06-19T16:29:37.960Z",
        "limit": "1",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.seismic.get_all_library_contents.get_seismic_client"
    ) as mock_seismic_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_seismic_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": test_data["document_id"],
                "name": "beta",
                "version": "1",
                "createdAt": test_data["created_at_start_time"],
                "modifiedAt": test_data["created_at_end_time"],
                "lastModified": test_data["created_at_end_time"],
            }
        ]

        # Get All Library Content
        response = get_all_library_contents(
            limit=test_data["limit"],
            created_at_start_time=test_data["created_at_start_time"],
            created_at_end_time=test_data["created_at_end_time"],
        )

        # Ensure that get_all_library_contents() executed and returned proper values
        assert response
        assert response.library_contents
        assert len(response.library_contents) == int(test_data["limit"])
        assert response.library_contents[0].id == test_data["document_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            endpoint="libraryContents",
            category=mock_seismic_client().REPORTING,
            params={
                "limit": test_data["limit"],
                "createdAtStartTime": test_data["created_at_start_time"],
                "createdAtEndTime": test_data["created_at_end_time"],
                "modifiedAtStartTime": None,
                "modifiedAtEndTime": None,
                "lastModifiedStartTime": None,
                "lastModifiedEndTime": None,
            },
        )
