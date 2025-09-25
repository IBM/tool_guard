from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_leads import list_leads
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Lead


def test_list_leads() -> None:
    """Test that the `list_leads` function returns the expected response."""
    test_data = [
        Lead(
            id="00QfJ000000TV23UAG",
            first_name="Bertha",
            last_name="Boxer",
            email="bertha@fcof.net",
            company="Farmers Coop. of Florida",
            description="",
            title="Director of Vendor Relations",
            industry="Agriculture",
            annual_revenue=900750000,
            number_of_employees=None,
            city="Tallahassee",
            state="FL",
            country="USA",
            zip_code="32306",
            rating="Hot",
            status="Working - Contacted",
        )
    ]

    expected: list[Lead] = test_data
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_leads.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data[0].id,
                "FirstName": test_data[0].first_name,
                "LastName": test_data[0].last_name,
                "Email": test_data[0].email,
                "Company": test_data[0].company,
                "Description": test_data[0].description,
                "Title": test_data[0].title,
                "Industry": test_data[0].industry,
                "AnnualRevenue": test_data[0].annual_revenue,
                "NumberOfEmployees": test_data[0].number_of_employees,
                "City": test_data[0].city,
                "State": test_data[0].state,
                "Country": test_data[0].country,
                "PostalCode": test_data[0].zip_code,
                "Rating": test_data[0].rating,
                "Status": test_data[0].status,
            }
        ]

        response = list_leads(search="State = 'FL'")

        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT AnnualRevenue, City, Company, Country, Description, Email, FirstName, Id, Industry, LastName, NumberOfEmployees, PostalCode, Rating, State, Status, Title FROM Lead WHERE State = 'FL'"
        )
