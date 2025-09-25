from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_event_reasons import (
    get_event_reasons,
)


def test_get_event_reasons() -> None:
    """Test the termination of an employee."""
    # Define test data:
    test_data = {
        "description": "Sabbatical Leave",
        "external_code": "PLASAB",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_event_reasons.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "description": test_data["description"],
                        "externalCode": test_data["external_code"],
                    }
                ]
            }
        }

        # Get event reasons
        response = get_event_reasons()

        # Ensure that get_event_reasons() executed and returned proper values
        assert response
        assert len(response.event_reasons)
        assert response.event_reasons[0].description == test_data["description"]
        assert response.event_reasons[0].external_code == test_data["external_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="FOEventReason",
            filter_expr="eventNav/externalCode eq '26' and status eq 'A'",
        )
