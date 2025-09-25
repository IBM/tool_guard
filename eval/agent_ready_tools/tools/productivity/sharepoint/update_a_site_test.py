from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.update_a_site import update_a_site


def test_update_a_site() -> None:
    """Verifies that the `update_a_site` tool can successfully update a SharePoint site."""

    # Define test data:
    test_data = {
        "site_id": "ibmappcon.sharepoint.com,66275c9d-54e5-4869-acb2-e5df23bc8edf,c8610d67-0958-4776-976b-d38877dcb67f",
        "new_site_name": "Updated Site Title",
        "site_description": "Updated description for the site",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.update_a_site.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "displayName": test_data["new_site_name"],
            "description": test_data["site_description"],
        }

        # Update a site
        response = update_a_site(
            site_id=test_data["site_id"],
            new_site_name=test_data["new_site_name"],
            site_description=test_data["site_description"],
        )

        # Ensure that update_a_site() executed and returned proper values
        assert response
        assert response.new_site_name == test_data["new_site_name"]
        assert response.site_description == test_data["site_description"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            endpoint=f"sites/{test_data['site_id']}",
            data={
                "displayName": test_data["new_site_name"],
                "description": test_data["site_description"],
            },
        )
