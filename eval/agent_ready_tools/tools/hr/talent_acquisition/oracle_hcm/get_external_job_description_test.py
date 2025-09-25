from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.get_external_job_description import (
    get_external_job_description,
)


def test_get_external_job_description() -> None:
    """Tests that the `get_external_job_description` function returns the expected response."""

    # Define data
    test_data = {
        "requisition_number": "989",
        "description": "text for the job description",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.get_external_job_description.get_oracle_hcm_client"
    ) as mock_oracle_client:

        # Mock the Oracle HCM client
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_response_text.return_value = test_data["description"]

        # Get external job description
        response = get_external_job_description(requisition_number=test_data["requisition_number"])

        # Ensure that get_external_job_description() got executed properly and returned proper values
        assert response
        assert response.description == test_data["description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_response_text.assert_called_once_with(
            entity=f"recruitingJobRequisitions/{test_data['requisition_number']}/enclosure/ExternalDescription",
        )
