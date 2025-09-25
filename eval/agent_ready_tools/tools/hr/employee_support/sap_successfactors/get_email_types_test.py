from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_email_types import (
    get_email_types_sap,
)


def test_get_email_types_sap() -> None:
    """Test that the `get_email_types_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "id": "8448",
        "label": "Business",
        "locale": "en_US",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_email_types.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "id": test_data["id"],
                            "picklistLabels": {
                                "results": [
                                    {"locale": test_data["locale"], "label": test_data["label"]}
                                ]
                            },
                        },
                    ]
                }
            }
        }

        # Get all email types
        response = get_email_types_sap()

        # Ensure that get_email_types_sap() executed and returned proper values
        assert response
        assert len(response.email_types)
        assert response.email_types[0].id == test_data["id"]
        assert response.email_types[0].label == test_data["label"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with("ecEmailType")
