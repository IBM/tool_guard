from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.zoominfo.search_company_by_criteria import (
    ZoominfoCompany,
    zoominfo_search_company_by_criteria,
)


def test_zoominfo_search_company_by_criteria() -> None:
    """Test if the 'search_company' function returns the expected response when input is a company
    ID."""
    # Define test data:
    test_data = {
        "company_id": 12240745,
        "company_name": "Church & Dwight Co.",
        "revenue_min": 6000000,
        "revenue_max": 7000000,
        "employee_count_min": 5000,
        "employee_count_max": 6000,
        "state": "New Jersey",
        "country": None,
        "industry_keywords": "Manufacturing",
    }

    # Patch `get_zoominfo_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.zoominfo.search_company_by_criteria.get_zoominfo_client"
    ) as mock_zoominfo_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zoominfo_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": [
                {
                    "id": test_data["company_id"],
                    "name": test_data["company_name"],
                }
            ]
        }

        # Search company by different filters
        response = zoominfo_search_company_by_criteria(
            company_id=test_data["company_id"],
            company_name=test_data["company_name"],
            revenue_min=test_data["revenue_min"],
            revenue_max=test_data["revenue_max"],
            employee_count_min=test_data["employee_count_min"],
            employee_count_max=test_data["employee_count_max"],
            state=test_data["state"],
            country=test_data["country"],
            industry_keywords=test_data["industry_keywords"],
        )

        # Ensure that search_company_by_criteria() executed and returned proper values
        assert response and len(response)
        assert isinstance(response[0], ZoominfoCompany)
        assert response[0].company_id == test_data["company_id"]
        assert response[0].company_name == test_data["company_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            category="search",
            endpoint="company",
            data={
                "companyId": test_data["company_id"],
                "companyName": test_data["company_name"],
                "revenueMin": test_data["revenue_min"],
                "revenueMax": test_data["revenue_max"],
                "employeeRangeMin": test_data["employee_count_min"],
                "employeeRangeMax": test_data["employee_count_max"],
                "state": test_data["state"],
                "country": test_data["country"],
                "industryKeywords": test_data["industry_keywords"],
            },
        )
