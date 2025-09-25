from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_states_by_country import (
    search_states_by_country,
)


def test_search_states_by_country() -> None:
    """Test that the `search_states_by_country` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "USA",
        "query": "California",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_states_by_country.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {
                            "picklistLabels": {
                                "results": [{"label": test_data["query"], "locale": "en_US"}]
                            },
                            "id": test_data["country"],
                        }
                    ]
                }
            }
        }

        # Search states by country
        response = search_states_by_country(country="USA", state_query=test_data["query"])

        # Ensure that search_states_by_country() executed and returned proper values
        assert response
        assert len(response.options)
        assert response.options[0].state == test_data["query"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            picklist_field=f"STATE_{test_data['country']}"
        )
