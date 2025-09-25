from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_opportunity import (
    create_opportunity,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Opportunity


def test_create_opportunity() -> None:
    """Test that the `create_opportunity` function returns the expected response."""

    test_data = Opportunity(
        id="006fJ000002PtEgQAK",
        account_id="001fJ00001wHPkwQAG",
        name="Wxo Create with Account 9",
        amount=3.0,
        close_date="2025-03-31",
        stage_name="Value Proposition",
        description="Wxo Test Account",
        opportunity_type="New Customer",
        lead_source="Other",
        age_in_days=None,
        probability=0,
    )

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_opportunity.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Opportunity.create.return_value = {"id": "006fJ000002PtEgQAK"}

        # Create opportunity
        response = create_opportunity(
            account_id=test_data.account_id,
            name=test_data.name,
            amount=test_data.amount,
            close_date=test_data.close_date,
            stage_name=test_data.stage_name,
            description=test_data.description,
            opportunity_type=test_data.opportunity_type,
            lead_source=test_data.lead_source,
        )

        # Ensure that create_opportunity() executed and returned proper values
        assert response
        assert response == test_data

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Opportunity.create(
            {
                "AccountId": test_data.account_id,
                "Name": test_data.name,
                "Amount": test_data.amount,
                "CloseDate": test_data.close_date,
                "StageName": test_data.stage_name,
                "Description": test_data.description,
                "Type": test_data.opportunity_type,
                "LeadSource": test_data.lead_source,
                "Probability": test_data.probability,
            }
        )
