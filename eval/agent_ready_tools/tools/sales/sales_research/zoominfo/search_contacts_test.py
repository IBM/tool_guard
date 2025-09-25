from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.zoominfo.search_contacts import (
    zoominfo_search_contacts,
)
from agent_ready_tools.tools.sales.sales_research.zoominfo.zoominfo_schemas import ZoominfoContact


def test_zoominfo_search_contacts() -> None:
    """Test if the 'search_contacts' function returns the expected response when input is a company
    ID."""
    # Define test data:
    test_data = {
        "company_id": "12240745",
        "first_name": "Kevin",
        "last_name": "Gokey",
        "job_title": "Executive Vice President and Chief Information Officer",
        "company_name": "Church & Dwight Co.",
        "management_level": None,
        "country": "US",
        "state": None,
        "address": None,
        "zip_code": None,
        "zipcode_radius_miles": None,
        "id": 1453845666,
        "has_email": True,
    }

    # Patch `get_zoominfo_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.zoominfo.search_contacts.get_zoominfo_client"
    ) as mock_zoominfo_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zoominfo_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": [
                {
                    "id": test_data["id"],
                    "firstName": test_data["first_name"],
                    "lastName": test_data["last_name"],
                    "jobTitle": test_data["job_title"],
                    "company": {
                        "id": test_data["company_id"],
                        "name": test_data["company_name"],
                    },
                    "hasEmail": test_data["has_email"],
                }
            ]
        }

        # Search contacts by different filters
        response = zoominfo_search_contacts(
            company_id=test_data["company_id"],
            company_name=test_data["company_name"],
            job_title=test_data["job_title"],
            management_level=test_data["management_level"],
            country=test_data["country"],
            state=test_data["state"],
            zip_code=test_data["zip_code"],
            zipcode_radius_miles=test_data["zipcode_radius_miles"],
        )

        # Ensure that search_contacts() executed and returned proper values
        assert response and len(response)
        assert isinstance(response[0], ZoominfoContact)
        assert response[0].person_id == test_data["id"]
        assert response[0].first_name == test_data["first_name"]
        assert response[0].last_name == test_data["last_name"]
        assert response[0].job_title == test_data["job_title"]
        assert response[0].company_name == test_data["company_name"]
        assert response[0].has_email == test_data["has_email"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            category="search",
            endpoint="contact",
            data={
                "firstName": None,
                "lastName": None,
                "emailAddress": None,
                "companyId": test_data["company_id"],
                "companyName": test_data["company_name"],
                "jobTitle": test_data["job_title"],
                "managementLevel": test_data["management_level"],
                "country": test_data["country"],
                "state": test_data["state"],
                "address": test_data["address"],
                "zipCode": test_data["zip_code"],
                "zipCodeRadiusMiles": test_data["zipcode_radius_miles"],
                "locationSearchType": "Person",
            },
        )
