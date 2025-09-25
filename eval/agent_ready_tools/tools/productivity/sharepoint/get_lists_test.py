from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_lists import get_lists


def test_get_all_lists() -> None:
    """Tests that all lists can be retrieved by the `get_lists` tool along with link for next set of
    records in Microsoft SharePoint."""

    # Define test data:
    site_id = "ibmappcon.sharepoint.com,66275c9d-54e5-4869-acb2-e5df23bc8edf,c8610d67-0958-4776-976b-d38877dcb67f"
    test_data = {
        "lists": [
            {
                "id": "829d26ec-0526-4cd5-9413-29974c08a6a4",
                "displayName": "Events",
                "description": "",
                "list": {"template": "genericList"},
            },
            {
                "id": "b75c4d06-9734-478e-be57-841bf3448255",
                "displayName": "Sharing Links",
                "description": "Use this list to track documents which have internal or anonymous sharing links in the site.",
                "list": {"template": "genericList"},
            },
        ],
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_lists.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.get_request.return_value = {"value": test_data["lists"]}

        # Get Microsoft lists
        response = get_lists(site_id=site_id)

        # Ensure that get_lists() executed and returned proper values
        assert response
        assert len(response.lists) == 2
        assert response.lists[0].list_id == test_data["lists"][0]["id"]
        assert response.lists[0].list_name == test_data["lists"][0]["displayName"]
        assert response.lists[0].description == test_data["lists"][0]["description"]
        assert response.lists[1].list_id == test_data["lists"][1]["id"]
        assert response.lists[1].list_name == test_data["lists"][1]["displayName"]
        assert response.lists[1].description == test_data["lists"][1]["description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"sites/{site_id}/lists",
            params={"$top": 500},
        )
