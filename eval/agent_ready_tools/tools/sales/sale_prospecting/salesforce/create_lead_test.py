from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_lead import create_lead
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Lead


def test_create_lead() -> None:
    """Test that the `create_lead` function returns the expected response."""

    # Define test data:
    test_data = {
        "first_name": "Rexii",
        "last_name": "T",
        "email": "rex_t@gmail.com",
        "company": "Best Easts",
        "description": "New leads to sell.",
        "title": "General Manager",
        "industry": "WXO TEST",
        "annual_revenue": 900000000,
        "number_of_employees": 350,
        "city": "San Jose",
        "state": "California",
        "country": "USA",
        "zip_code": "95008",
        "rating": "hot",
        "status": "unconverted",
    }

    lead_data = {"id": "00QfJ000004GkHVUA0", **test_data}

    expected = Lead(**lead_data)  # type: ignore[arg-type]

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_lead.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Lead.create.return_value = {"id": "00QfJ000004GkHVUA0"}

        # Create Lead
        response = create_lead(**test_data)

        # Ensure that create_lead() executed and returned proper values
        assert response
        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Lead.create(
            {
                "FirstName": test_data["first_name"],
                "LastName": test_data["last_name"],
                "Email": test_data["email"],
                "Company": test_data["company"],
                "Description": test_data["description"],
                "Title": test_data["title"],
                "Industry": test_data["industry"],
                "AnnualRevenue": test_data["annual_revenue"],
                "NumberOfEmployees": test_data["number_of_employees"],
                "City": test_data["city"],
                "State": test_data["state"],
                "Country": test_data["country"],
                "PostalCode": test_data["zip_code"],
                "Rating": test_data["rating"],
                "Status": test_data["status"],
            }
        )
