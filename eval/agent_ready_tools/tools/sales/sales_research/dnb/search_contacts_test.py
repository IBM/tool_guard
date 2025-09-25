from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.search_contacts import (
    Contact,
    search_contacts,
)


def test_search_contacts() -> None:
    """Test if the 'search_contacts' function returns the expected response when input is a
    duns_number."""
    # Define test data:
    test_data = {
        "duns_number": "916728585",
        "search_term": "",
        "full_name": "John Smith",
        "email": "john.smith@ibm.com",
        "job_title": "Software Engineer",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.search_contacts.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "searchCandidates": [
                {
                    "displaySequence": 1,
                    "contact": {
                        "fullName": test_data["full_name"],
                        "email": test_data["email"],
                        "jobTitles": [{"title": test_data["job_title"]}],
                    },
                }
            ]
        }

        # Search contacts by different filters
        response = search_contacts(
            duns_number=test_data["duns_number"],
            search_term=test_data["search_term"],
        )

        # Ensure that search_contacts() executed and returned proper values
        assert response and len(response)
        assert isinstance(response[0], Contact)
        assert response[0].full_name == test_data["full_name"]
        assert response[0].email == test_data["email"]
        assert response[0].job_title == [test_data["job_title"]]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            version="v2",
            category="search",
            endpoint="contact",
            data={
                "duns": test_data["duns_number"],
                "searchTerm": test_data["search_term"],
            },
        )
