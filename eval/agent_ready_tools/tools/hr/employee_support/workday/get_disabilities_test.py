from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_disabilities import get_disabilities
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_disabilities() -> None:
    """Test that the `get_disabilities` function returns the expected response."""

    # Define test data:
    test_data = {
        "disability_reference_wid": "85883bbbf7a644b3b67dcda864b52c91",
        "disability_data_name": "Speech Impairment",
        "disability_data_id": "Speech_Impairment_USA",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_disabilities.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_disabilities.return_value = Obj(
            {
                "body": {
                    "get_disabilities_response": {
                        "response_data": {
                            "disability": [
                                Obj(
                                    {
                                        "disability_reference": {
                                            "id": [
                                                Obj(
                                                    {"value": test_data["disability_reference_wid"]}
                                                )
                                            ]
                                        },
                                        "disability_data": {
                                            "name": test_data["disability_data_name"],
                                            "id": test_data["disability_data_id"],
                                        },
                                    }
                                )
                            ],
                        }
                    },
                },
            }
        )

        # Get disabilities
        response = get_disabilities()

        # Ensure that get_disabilities() executed and returned proper values
        assert response
        assert len(response)
        assert response[0].disability_reference_wid == test_data["disability_reference_wid"]
        assert response[0].disability_data_name == test_data["disability_data_name"]
        assert response[0].disability_data_id == test_data["disability_data_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_disabilities.assert_called_once_with()
