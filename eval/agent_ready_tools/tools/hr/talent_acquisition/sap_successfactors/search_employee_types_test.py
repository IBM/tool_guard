from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_employee_types import (
    search_employee_type,
)


def test_search_employee_type_with_casual() -> None:
    """Test that the `search_employee_type` function returns the expected response."""

    # Define test data:
    test_data: Dict[str, Any] = {
        "picklist_id": "3982",
        "employee_type": "Casual",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_employee_types.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client

        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "id": test_data["picklist_id"],
                            "picklistLabels": {
                                "results": [
                                    {"label": test_data["employee_type"], "locale": "en_US"}
                                ]
                            },
                        },
                    ]
                }
            }
        }

        response = search_employee_type()

        # Ensure that search_employee_types() executed and returned proper values
        assert response is not None
        matched = response.options[0]
        assert matched.picklist_id == test_data["picklist_id"]
        assert matched.employee_type == test_data["employee_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="employType")


def test_search_employee_type_with_contract() -> None:
    """Test that the `search_employee_type` function returns the expected response."""

    # Define test data:
    test_data: Dict[str, Any] = {
        "picklist_id": "3980",
        "employee_type": "Fixed-term contract",
    }
    test_data_1: Dict[str, Any] = {
        "picklist_id": "3979",
        "employee_type": "Full-time",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_employee_types.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client

        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "id": test_data["picklist_id"],
                            "picklistLabels": {
                                "results": [
                                    {"label": test_data["employee_type"], "locale": "en_US"}
                                ]
                            },
                        },
                        {
                            "id": test_data_1["picklist_id"],
                            "picklistLabels": {
                                "results": [
                                    {"label": test_data_1["employee_type"], "locale": "en_US"}
                                ]
                            },
                        },
                    ]
                }
            }
        }

        response = search_employee_type("Fixed-term contract")

        # Ensure that search_employee_types() executed and returned proper values
        assert response is not None
        matched = response.options[0]
        assert matched.picklist_id == test_data["picklist_id"]
        assert matched.employee_type == test_data["employee_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="employType")
