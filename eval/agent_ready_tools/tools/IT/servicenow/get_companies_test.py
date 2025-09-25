from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_companies import get_companies


def test_get_company() -> None:
    """Test that all the companies can be retrieved successfully."""

    # Define test data:
    test_data = {
        "name": "SAP America",
        "id": "0c43bda7c611227500002515fd14d70d",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_companies.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "name": test_data["name"],
                },
            ],
        }

        # Get companies
        response = get_companies(company=test_data["name"])

        # Ensure that get_companies() executed and returned proper values
        assert response
        assert len(response.companies)
        assert response.companies[0].system_id == test_data["id"]
        assert response.companies[0].company == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="core_company", params={"name": test_data["name"]}
        )
