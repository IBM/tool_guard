from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.create_requisition import (
    coupa_create_requisition,
)


def test_coupa_create_requisition() -> None:
    """Test that the `create_requisition_coupa` function returns the expected response."""

    # Define test data:
    test_data = {
        "requester_login_name": "mjordan",
        "requisition_id": 31231898321,
        "currency_code": "USD",
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.create_requisition.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["requisition_id"],
        }

        # Create the requisition
        response = coupa_create_requisition(
            requester_login_name=test_data["requester_login_name"],
            currency_code=test_data["currency_code"],
        ).content

        # Ensure that create_requisition_coupa() executed and returned proper values
        assert response
        assert response.requisition_id == test_data["requisition_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name="requisitions/create_as_cart",
            payload={
                "requested-by": {"login": f"{test_data['requester_login_name']}"},
                "currency": {"code": test_data["currency_code"]},
            },
        )
