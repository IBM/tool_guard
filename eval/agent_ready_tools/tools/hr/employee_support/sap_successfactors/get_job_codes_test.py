from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_job_codes import (
    get_job_codes,
)


def test_get_job_codes() -> None:
    """Verifies that the `get_job_codes` tool is retrieving data successfully."""
    # Define test data:
    test_data = {
        "name": "Lawyer",
        "code": "50070923",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_job_codes.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "externalCode": test_data["code"],
                        "name": test_data["name"],
                    }
                ]
            }
        }

        # Get job codes
        response = get_job_codes()

        # Ensure that get_job_codes() executed and returned proper values
        assert response
        assert len(response.job_codes)
        assert response.job_codes[0].name == test_data["name"]
        assert response.job_codes[0].code == test_data["code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="FOJobCode", select_expr="externalCode,name"
        )
