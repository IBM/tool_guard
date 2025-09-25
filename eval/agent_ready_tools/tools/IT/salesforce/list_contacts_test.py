from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_contacts import list_contacts
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Contact


def test_list_contacts() -> None:
    """Test that the `list_contacts` function returns the expected response."""
    test_data = [
        Contact(
            account_id="001fJ00000223nBQAQ",
            id="003fJ000000bxR3QAI",
            name="Stella Pavlova",
            email="spavlova@uog.com",
            phone="(212) 842-5500",
            title="SVP, Production",
            mobile_phone="(212) 842-5501",
        )
    ]

    expected: list[Contact] = test_data
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_contacts.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "AccountId": test_data[0].account_id,
                "Id": test_data[0].id,
                "Name": test_data[0].name,
                "Email": test_data[0].email,
                "Phone": test_data[0].phone,
                "Title": test_data[0].title,
                "MobilePhone": test_data[0].mobile_phone,
            }
        ]

        response = list_contacts("Name=Stella Pavlova")

        assert response == expected
