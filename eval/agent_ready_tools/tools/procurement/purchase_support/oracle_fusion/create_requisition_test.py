from typing import Any
from unittest.mock import MagicMock, call, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.create_requisition import (
    oracle_fusion_create_requisition,
)


def test_oracle_fusion_create_requisition() -> None:
    """Test that the `create_requisition` function returns the expected response."""
    test_user_prefs = {
        "items": [
            {
                "DestinationOrganizationCode": "001",
                "DeliverToLocationCode": "USLOC_CENT",
                "DestinationTypeCode": "EXPENSE",
                "favoriteChargeAccounts": [
                    {
                        "PrimaryFlag": True,
                        "ChargeAccount": "101.10.11101.000.000.000",
                    }
                ],
            }
        ]
    }

    test_item_search = {
        "items": [
            {
                "ItemId": 300000025339742,
                "LineTypeId": 1,
                "SupplierId": 300000010011003,
                "Supplier": "United Parcel Service",
                "SupplierSiteId": 300000010011025,
                "SupplierSite": "UPS US1",
                "AgreementNumber": "52279",
                "AgreementHeaderId": 300000025664207,
                "LineNumber": 1,
                "AgreementLineId": 300000025664210,
                "Price": 899,
                "UOM": "Ea",
                "CurrencyCode": "USD",
            }
        ]
    }

    # Define test data
    test_data: dict[str, Any] = {
        "Requisition": "204259",
        "RequisitioningBU": "US1 Business Unit",
        "Description": "refining create requisition tool test",
        "ExternallyManagedFlag": False,
        "PreparerEmail": "Saurabh.Singh36@ibm.com",
        "lines": [
            {
                "RequisitionLineId": 300000026061256,
                "LineNumber": 1,
                "ItemId": 300000025339742,
                "Item": "Macbook Pro 15 inch",
                "ItemDescription": "macbook pro 15 inch for Wxo test",
                "Quantity": 4,
                "Price": 899,
                "UOM": "Ea",
                "CurrencyCode": "USD",
                "Requester": "Singh, Saurabh",
                "RequesterEmail": "Saurabh.Singh36@ibm.com",
                "DeliverToLocationCode": "USLOC_CENT",
                "DestinationOrganizationCode": "001",
                "DestinationTypeCode": "EXPENSE",
                "Supplier": "United Parcel Service",
                "SupplierId": 300000010011003,
                "SupplierSite": "UPS US1",
                "SupplierSiteId": 300000010011025,
                "SourceAgreement": "52279",
                "SourceAgreementHeaderId": 300000025664207,
                "SourceAgreementLineId": 300000025664210,
                "SourceAgreementLineNumber": 1,
                "RequestedDeliveryDate": "2025-08-22",
                "distributions": [
                    {
                        "RequisitionDistributionId": 300000026061257,
                        "DistributionNumber": 1,
                        "ChargeAccount": "101.10.11101.000.000.000",
                        "Quantity": 4,
                        "BudgetDate": "2025-08-22",
                    }
                ],
            }
        ],
    }

    # Patch `get_oracle_fusion_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.create_requisition.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.side_effect = [test_user_prefs, test_item_search]
        mock_client.post_request.return_value = test_data

        # Create requisition
        response = oracle_fusion_create_requisition(
            preparer_email="Saurabh.Singh36@ibm.com",
            requisition_bu="US1 Business Unit",
            requisition_description="refining create requisition tool test",
            distribution_number=1,
            requested_date="2025-08-22",
            item_description="macbook",
            quantity=4,
        ).content

        print(response)

        # Ensure that create_requisition() executed and returned proper value
        assert response.requisition_number == "204259"
        assert response.requisitioning_business_unit == "US1 Business Unit"

        expected_calls = [
            call(
                resource_name="requisitionPreferences", params={"expand": "favoriteChargeAccounts"}
            ),
            call(
                resource_name="purchaseAgreementLines", params={"q": "Description LIKE '%macbook%'"}
            ),
        ]
        mock_client.get_request.assert_has_calls(expected_calls)

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name="purchaseRequisitions",
            payload={
                "Description": "refining create requisition tool test",
                "ExternallyManagedFlag": False,
                "PreparerEmail": "Saurabh.Singh36@ibm.com",
                "RequisitioningBU": "US1 Business Unit",
                "lines": [
                    {
                        "CurrencyCode": "USD",
                        "DeliverToLocationCode": "USLOC_CENT",
                        "DestinationOrganizationCode": "001",
                        "DestinationTypeCode": "EXPENSE",
                        "ItemId": 300000025339742,
                        "LineTypeId": 1,
                        "Price": 899,
                        "Quantity": 4,
                        "RequestedDeliveryDate": "2025-08-22",
                        "RequesterEmail": "Saurabh.Singh36@ibm.com",
                        "SourceAgreement": "52279",
                        "SourceAgreementHeaderId": 300000025664207,
                        "SourceAgreementLineId": 300000025664210,
                        "SourceAgreementLineNumber": 1,
                        "Supplier": "United Parcel Service",
                        "SupplierId": 300000010011003,
                        "SupplierSite": "UPS US1",
                        "SupplierSiteId": 300000010011025,
                        "UOM": "Ea",
                        "distributions": [
                            {
                                "BudgetDate": "2025-08-22",
                                "ChargeAccount": "101.10.11101.000.000.000",
                                "DistributionNumber": 1,
                                "Quantity": 4,
                            }
                        ],
                    }
                ],
            },
        )
