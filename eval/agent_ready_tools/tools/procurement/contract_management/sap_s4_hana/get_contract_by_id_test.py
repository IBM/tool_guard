from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.common_classes_contract_management import (
    SAPS4HANAContractTypes,
)
from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.get_contract_by_id import (
    sap_s4_hana_get_contract_by_id,
)


def test_sap_s4_hana_get_contract_details_success() -> None:
    """Verify that the `sap_s4_hana_get_contract_by_id` tool can successfully retrieve contract
    details from SAP S4 HANA."""

    test_data = {
        "contract_id": "4600000105",
        "contract_type": "MK",
        "purchasing_group": "001",
        "company_code": "1010",
        "purchasing_organization": "1010",
        "supplier_id": "10200001",
        "contract_start_date": "/Date(1747872000000)/",
        "contract_end_date": "/Date(1747872000000)/",
        "payment_terms": "0001",
        "target_amount": "0.00",
        "currency": "EUR",
        "exchange_rate": "1.00000",
        "status": "Active",
        "item_number": "00010",
        "item_description": "Contract item",
        "material": "51",
        "material_group": "L004",
        "net_price": "100.00",
        "net_price_quantity": "1",
        "target_quantity": "25",
        "price_unit": "PC",
        "production_plant": "1010",
        "product_type": "1",
        "address_id": "23384",
        "street_name": "Downtown",
        "house_number": "16",
        "postal_code": "69190",
        "city": "New York",
        "country": "US",
        "region": "NY",
        "time_zone": "EST",
        "payment_in_days1": "10",
        "cash_discount_percentage1": "3.5",
        "payment_in_days2": "15",
        "cash_discount_percentage2": "2",
        "net_payment_days": "20",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.get_contract_by_id.get_sap_s4_hana_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "PurchaseContract": test_data["contract_id"],
                    "PurchaseContractType": test_data["contract_type"],
                    "PurchasingGroup": test_data["purchasing_group"],
                    "CompanyCode": test_data["company_code"],
                    "PurchasingOrganization": test_data["purchasing_organization"],
                    "Supplier": test_data["supplier_id"],
                    "ValidityStartDate": test_data["contract_start_date"],
                    "ValidityEndDate": test_data["contract_end_date"],
                    "PaymentTerms": test_data["payment_terms"],
                    "CashDiscount1Days": test_data["payment_in_days1"],
                    "CashDiscount2Days": test_data["payment_in_days2"],
                    "NetPaymentDays": test_data["net_payment_days"],
                    "CashDiscount1Percent": test_data["cash_discount_percentage1"],
                    "CashDiscount2Percent": test_data["cash_discount_percentage2"],
                    "PurchaseContractTargetAmount": test_data["target_amount"],
                    "DocumentCurrency": test_data["currency"],
                    "ExchangeRate": test_data["exchange_rate"],
                    "PurchasingProcessingStatusName": test_data["status"],
                    "to_PurchaseContractItem": {
                        "results": [
                            {
                                "PurchaseContractItem": test_data["item_number"],
                                "PurchaseContractItemText": test_data["item_description"],
                                "Material": test_data["material"],
                                "MaterialGroup": test_data["material_group"],
                                "ContractNetPriceAmount": test_data["net_price"],
                                "NetPriceQuantity": test_data["net_price_quantity"],
                                "TargetQuantity": test_data["target_quantity"],
                                "OrderQuantityUnit": test_data["price_unit"],
                                "Plant": test_data["production_plant"],
                                "ProductType": test_data["product_type"],
                                "to_PurCtrAddress": {
                                    "results": [
                                        {
                                            "AddressID": test_data["address_id"],
                                            "StreetName": test_data["street_name"],
                                            "HouseNumber": test_data["house_number"],
                                            "PostalCode": test_data["postal_code"],
                                            "CityName": test_data["city"],
                                            "Country": test_data["country"],
                                            "Region": test_data["region"],
                                            "AddressTimeZone": test_data["time_zone"],
                                        }
                                    ]
                                },
                            }
                        ]
                    },
                }
            }
        }

        response = sap_s4_hana_get_contract_by_id(contract_id=test_data["contract_id"])

        assert isinstance(response, ToolResponse)
        assert response.success is True
        assert response.message == "The data was successfully retrieved"
        assert response.content is not None

        contract = response.content
        assert contract.contract_id == test_data["contract_id"]
        assert contract.supplier_id == test_data["supplier_id"]
        assert contract.contract_type == SAPS4HANAContractTypes(test_data["contract_type"]).name
        assert contract.item_details[0].item_number == test_data["item_number"]
        assert contract.supplier_address[0].address_id == test_data["address_id"]
        assert contract.supplier_address[0].city == test_data["city"]
        assert contract.payment_details[0].payment_terms == test_data["payment_terms"]
        assert contract.payment_details[0].payment_in_days1 == test_data["payment_in_days1"]
        assert (
            contract.payment_details[0].cash_discount_percentage1
            == test_data["cash_discount_percentage1"]
        )

        mock_client.get_request.assert_called_once_with(
            entity=f"100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract('{test_data['contract_id']}')",
            expand_expr="to_PurchaseContractItem/to_PurCtrAddress",
        )
