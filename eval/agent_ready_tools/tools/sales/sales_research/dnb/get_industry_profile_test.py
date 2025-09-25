from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.get_industry_profile import (
    IndustryProfileResponse,
    get_industry_profile,
)


def test_get_industry_profile() -> None:
    """Test that the `get_industry_profile` function returns the expected response."""

    # Define test data:
    test_data = {
        "search_value": "search",
        "profile_name": "Alpha Omega",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_industry_profile.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "profiles": [
                {
                    "profileName": test_data["profile_name"],
                }
            ],
        }

        # Get industry profiles
        response = get_industry_profile(search_term=test_data["search_value"])
        # Ensure that get_industry_profile() executed and returned proper values
        assert response
        assert isinstance(response[0], IndustryProfileResponse)
        assert response[0].profile_name == test_data["profile_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            version="v1",
            category="industryprofile",
            params={
                "productId": "inddet",
                "versionId": "v1",
                f"searchTerm": test_data["search_value"],
            },
        )
