from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_job_functions import (
    search_job_functions,
)


def test_search_job_functions() -> None:
    """Test that the `search_job_functions` function returns the expected response."""

    # Define test data:
    test_data: Dict[str, Any] = {
        "picklist_id": "11962",
        "job_function": "Administration",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_job_functions.get_sap_successfactors_client"
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
                                "results": [{"label": test_data["job_function"], "locale": "en_US"}]
                            },
                        }
                    ]
                }
            }
        }

        # Search the job functions
        response = search_job_functions()

        # Ensure that search_job_functions() executed and returned proper values
        assert response is not None
        option = response.options[0]
        assert option.picklist_id == test_data["picklist_id"]
        assert option.job_function == test_data["job_function"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="jobFunction")


def test_search_job_functions_with_query() -> None:
    """Test fuzzy matching logic in `search_job_functions` with a job_function_query."""

    # Define test data:
    test_data = [
        {"picklist_id": "11962", "job_function": "Administration"},
        {"picklist_id": "11963", "job_function": "Engineering"},
        {"picklist_id": "11964", "job_function": "Finance"},
    ]

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_job_functions.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client

        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "id": item["picklist_id"],
                            "picklistLabels": {
                                "results": [{"label": item["job_function"], "locale": "en_US"}]
                            },
                        }
                        for item in test_data
                    ]
                }
            },
            "status_code": 200,
        }

        # Intentionally misspelled query to test fuzzy matching
        response = search_job_functions(job_function_query="Engneering")
        # Ensure that search_job_functions() executed and returned proper values
        assert response is not None
        # Expect "Engineering" to be the top match
        assert response.options[0].job_function == "Engineering"

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="jobFunction")
