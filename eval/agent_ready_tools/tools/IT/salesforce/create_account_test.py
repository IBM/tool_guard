from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_account import create_account


def test_create_account() -> None:
    """Tests that `create_account` function returns the expected response."""

    # Define test data:
    test_data = {
        "name": "Example Acc - Test May 6",
        "account_type": "Customer - Direct",
        "phone": "+9165764",
        "website": "www.jgTKJBK.com",
    }

    account_id = "001fJ00551yICyvBCG"

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_account.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Account.create.return_value = {"id": account_id}

        # Create Account
        response = create_account(**test_data)

        # Ensure that create_ccount() executed and returned proper values
        assert response
        assert response.id == account_id

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Account.create(
            {
                "Name": test_data["name"],
                "Type": test_data["account_type"],
                "Phone": test_data["phone"],
                "Website": test_data["website"],
            }
        )
