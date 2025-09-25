from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_access_levels import (
    AccessLevel,
    list_access_levels,
)


def test_list_access_levels() -> None:
    """Verifies that the `list_access_levels` tool can successfully retrieve Adobe Workfront
    groups."""

    # Define the test data
    test_date = {
        "access_level_id": "66db21100646c6ae9dd4407ab4242935",
        "access_level_name": "Light",
        "access_level_restrictions": "AIOFF",
        "license_type": "C",
    }

    # patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_access_levels.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # create mock client
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client

        # mock the API response
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_date["access_level_id"],
                    "name": test_date["access_level_name"],
                    "accessRestrictions": test_date["access_level_restrictions"],
                    "licenseType": test_date["license_type"],
                }
            ]
        }

        # List Adobe workfront access levels
        response = list_access_levels(
            access_level_name=test_date["access_level_name"], limit=50, skip=1
        )

        # Ensure that list_access_levels() has executed and returned proper values.
        excpected_output = AccessLevel(
            access_level_id=str(test_date["access_level_id"]),
            access_level_name=str(test_date["access_level_name"]),
            access_level_restrictions=str(test_date["access_level_restrictions"]),
            license_type=str(test_date["license_type"]),
        )

        assert response.access_levels[0] == excpected_output

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="accessLevel/search",
            params={
                "name": test_date["access_level_name"],
                "$$LIMIT": 50,
                "$$SKIP": 1,
            },
        )
