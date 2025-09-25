from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_relationship_types import (
    get_relationship_types,
)


def test_get_relationship_types() -> None:
    """Test that the `get_relationship_types` function returns the expected response."""
    # Define test data:
    test_data = {
        "relationship_id": "5461",
        "relationship_type": "Child",
        "locale": "en_US",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_relationship_types.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "id": test_data["relationship_id"],
                            "picklistLabels": {
                                "results": [
                                    {
                                        "locale": test_data["locale"],
                                        "label": test_data["relationship_type"],
                                    },
                                ]
                            },
                        }
                    ]
                }
            }
        }

        # Get relationship types
        response = get_relationship_types()

        # Ensure that get_relationship_types() executed and returned proper values
        assert response
        assert len(response.relationship_types)
        assert response.relationship_types[0].relationship_id == test_data["relationship_id"]
        assert response.relationship_types[0].relationship_type == test_data["relationship_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="relation")
