from typing import Any
from unittest.mock import MagicMock, patch

from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_assets import list_assets
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Asset


def test_list_assets() -> None:
    """Test that the `list_assets` function returns the expected response."""
    test_data: dict[str, Any] = {"asset_id": "02igL0000000LfZQA", "asset_name": "Test Laptop"}

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_assets.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["asset_id"],
                "Name": test_data["asset_name"],
            }
        ]

        # List all account contacts
        response = list_assets("Name = Test Laptop")

        # Construct expected object
        expected_value = [
            Asset(
                asset_id=test_data["asset_id"],
                asset_name=test_data["asset_name"],
            )
        ]

        # Assertions
        assert response == expected_value
        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(f"SELECT Id, Name FROM Asset WHERE Name = 'Test Laptop'")
        )


def test_list_assets_without_filters() -> None:
    """Test that the `list_assets` function returns the expected response."""
    test_data: dict[str, Any] = {"asset_id": "02igL0000000LfZQA", "asset_name": "Test Laptop"}

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_assets.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["asset_id"],
                "Name": test_data["asset_name"],
            }
        ]

        # List all account contacts
        response = list_assets()

        # Construct expected object
        expected_value = [
            Asset(
                asset_id=test_data["asset_id"],
                asset_name=test_data["asset_name"],
            )
        ]

        # Assertions
        assert response[:1] == expected_value
        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(f"SELECT Id, Name FROM Asset ")
        )
