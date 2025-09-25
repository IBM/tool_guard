from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_sites import Site, get_sites


def test_get_sites() -> None:
    """Tests that the sites can be retrieved by the `get_sites` tool in Microsoft SharePoint."""

    # Define test data
    test_data = {
        "site_name": "Library",
        "site_url": "https://ibmappcon.sharepoint.com/sites/goal",
        "site_id": "ibmappcon.sharepoint.com,92a5bf12-65ac-45fe-93ce-c71140b4c6c5,afdc0ed8-07ec-49ab-a724-f2f11eda1414",
        "site_description": "community for library",
        "output_limit": 5,
        "output_skip_token": "s!NTtlYjFmM2ZjNy02MTI4LTQ1ZDQtOThkYy1mOTRlYjQ1M2FkZWM",
    }
    limit = 5
    skip_token = None

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_sites.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "displayName": test_data["site_name"],
                    "webUrl": test_data["site_url"],
                    "id": test_data["site_id"],
                    "description": test_data["site_description"],
                }
            ],
            "@odata.nextLink": f"https://example.com/nextLink?$top={test_data['output_limit']}&search={test_data['site_name']}&$skiptoken={test_data['output_skip_token']}",
        }

        # Call the function
        response = get_sites(site_name=test_data["site_name"], limit=limit, skip_token=skip_token)
        # Verify that the site details match the expected data

        expected_site = Site(
            site_name=str(test_data["site_name"]),
            site_url=str(test_data["site_url"]),
            site_id=str(test_data["site_id"]),
            site_description=str(test_data["site_description"]),
        )

        assert response.sites[0] == expected_site
        assert response.limit == test_data["output_limit"]
        assert response.skip_token == test_data["output_skip_token"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="sites",
            params={"$top": limit, "search": test_data["site_name"]},
        )
