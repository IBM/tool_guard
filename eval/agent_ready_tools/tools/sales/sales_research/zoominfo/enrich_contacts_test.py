from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.zoominfo.enrich_contacts import (
    zoominfo_enrich_contacts,
)
from agent_ready_tools.tools.sales.sales_research.zoominfo.zoominfo_schemas import (
    ZoominfoEnrichedContact,
)


def test_zoominfo_enrich_contacts() -> None:
    """Test if the 'enrich_contacts' function returns the expected response when input is a list of
    person IDs."""
    # Define test data:
    test_data = {
        "first_name": "Elena",
        "last_name": "Cirillo",
        "email": "elena.cirillo@gop.it",
        "city": "London",
        "job_title": "Counsel",
        "job_function": "Legal Counsel",
        "department": "Legal",
        "company_name": "Gianni, Origoni, Grippo, Cappelli & Partners",
        "social_media": "https://www.linkedin.com/in/elena-cirillo-05a86b34",
        "person_id": "1584305636",
        "company_id": 372884253,
    }

    with patch(
        "agent_ready_tools.tools.sales.sales_research.zoominfo.enrich_contacts.get_zoominfo_client"
    ) as mock_zoominfo_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zoominfo_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "success": "true",
            "data": {
                "result": [
                    {
                        "data": [
                            {
                                "firstName": test_data["first_name"],
                                "lastName": test_data["last_name"],
                                "email": test_data["email"],
                                "city": test_data["city"],
                                "jobTitle": test_data["job_title"],
                                "jobFunction": [
                                    {
                                        "name": test_data["job_function"],
                                        "department": test_data["department"],
                                    }
                                ],
                                "externalUrls": [
                                    {"type": "linkedin.com", "url": test_data["social_media"]}
                                ],
                                "id": test_data["person_id"],
                                "company": {
                                    "name": test_data["company_name"],
                                    "id": test_data["company_id"],
                                },
                            }
                        ],
                    }
                ],
            },
        }

        # Enrich contacts
        response = zoominfo_enrich_contacts(person_id_list=[test_data["person_id"]])

        # Ensure that enrich_contacts() executed and returned proper values
        assert response and len(response)
        assert isinstance(response[0], ZoominfoEnrichedContact)

        assert response[0].first_name == test_data["first_name"]
        assert response[0].last_name == test_data["last_name"]
        assert response[0].job_title == test_data["job_title"]
        assert response[0].company_name == test_data["company_name"]
        assert response[0].job_function == test_data["job_function"]
        assert response[0].social_media == test_data["social_media"]
        assert response[0].email == test_data["email"]
        assert response[0].city == test_data["city"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            category="enrich",
            endpoint="contact",
            data={
                "outputFields": [
                    "firstName",
                    "lastName",
                    "email",
                    "city",
                    "jobTitle",
                    "jobFunction",
                    "companyName",
                    "externalUrls",
                ],
                "matchPersonInput": [{"personId": test_data["person_id"]}],
            },
        )
