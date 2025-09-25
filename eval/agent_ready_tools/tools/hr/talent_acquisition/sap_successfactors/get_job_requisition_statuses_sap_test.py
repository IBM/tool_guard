from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_job_requisition_statuses_sap import (
    get_job_requisition_statuses_sap,
)


def test_get_job_requisition_statuses_sap() -> None:
    """Test that the `get_job_requisition_statuses_sap` function returns the expected response."""
    # Define test data
    test_data = {
        "status_id": "20546",
        "status_label": "Open",
        "locale": "en_US",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_job_requisition_statuses_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "id": test_data["status_id"],
                            "picklistLabels": {
                                "results": [
                                    {
                                        "locale": test_data["locale"],
                                        "label": test_data["status_label"],
                                    }
                                ]
                            },
                        }
                    ]
                }
            }
        }

        # Get job requisition statuses
        response = get_job_requisition_statuses_sap()

        # Assertions
        assert response
        assert len(response.requisition_statuses) == 1
        assert response.requisition_statuses[0].status_id == test_data["status_id"]
        assert response.requisition_statuses[0].label == test_data["status_label"]

        # Verify API call
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="reqStatus")
