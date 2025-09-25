from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_contract import (
    update_contract,
)


def test_update_contract() -> None:
    """Test that the `update_contract` function returns the expected response."""

    expected = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_contract.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Contract.update.return_value = expected

        # Update contract
        response = update_contract(
            contract_id="800gL000005Js5BQAS",
            status="Draft",
            account_id="001gL000004Zin4QAC",
            start_date="2025-05-08",
            contract_term=12,
            owner_expiration_notice="30",
            pricebook2_id="01sgL000000unndQAA",
            billing_street="123 Main St",
            billing_city="San Francisco",
            billing_state_code="AZ",
            billing_postal_code="94105",
            billing_country_code="US",
            description="Test decription",
            owner_id="005gL000001aT2vQAE",
        )

        # Ensure that update_contract() executed and returned proper values
        assert response
        assert response == expected
