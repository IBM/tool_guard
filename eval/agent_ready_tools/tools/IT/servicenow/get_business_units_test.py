from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_business_units import get_business_units


def test_get_business_units() -> None:
    """Test that business units can be retrieved successfully."""

    # Define test data:
    test_data = {
        "id": "2d26c204870221003ff35d88e3e3ec62",
        "name": "Legal",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_business_units.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "name": test_data["name"],
                }
            ],
        }

        # Get business units
        response = get_business_units()

        # Ensure that get_business_units() executed and returned proper values
        assert response
        assert len(response.business_units)
        assert response.business_units[0].system_id == test_data["id"]
        assert response.business_units[0].business_unit_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="business_unit", params={})
