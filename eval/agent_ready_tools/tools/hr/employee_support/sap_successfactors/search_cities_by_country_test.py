from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_cities_by_country import (
    search_cities_by_country,
)


def test_search_cities_by_country() -> None:
    """Test that the `search_cities_by_country` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "QAT",
        "query": "Al Hilal al Gharbiyah",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_cities_by_country.get_sap_successfactors_client"
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

        # Search cities by country
        response = search_cities_by_country(
            country=test_data["country"], city_query=test_data["query"]
        )

        # Ensure that search_cities_by_country() executed and returned proper values
        assert response
        assert len(response.options)
        assert response.options[0].city == test_data["query"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            picklist_field=f"CITY_{test_data['country']}"
        )
