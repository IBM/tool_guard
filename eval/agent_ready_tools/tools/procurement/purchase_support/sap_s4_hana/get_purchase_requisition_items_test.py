from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_requisition_items import (
    sap_s4_hana_get_purchase_requisition_items,
)


def test_get_purchase_requisition_by_id() -> None:
    """Test that the `sap_s4_hana_get_purchase_requisition_items` function returns the expected
    response."""

    test_data = {
        "purchase_requisition_id": "10000134",
        "purchase_requisition_description": "Test Description",
        "purchase_requisition_item_id": "10",
        "purchasing_group": "001",
        "purchasing_organization": "1010",
        "plant": "1010",
        "material": "2000000026",
        "material_group": "01",
        "creation_date": "/Date(1584835200000)/",
        "delivery_date": "/Date(1585180800000)/",
        "release_date": "/Date(1584921600000)/",
        "currency": "EUR",
        "requested_quantity": "100",
        "price": "18.65",
        "net_amount": "1865.00",
        "requisitioner_name": "MRP Controll",
        "base_unit": "PC",
        "postal_code": "69190",
        "city": "Walldorf",
        "country": "DE",
        "region": "BW",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_requisition_items.get_sap_s4_hana_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "PurchaseRequisition": test_data["purchase_requisition_id"],
                    "PurReqnDescription": test_data["purchase_requisition_description"],
                    "to_PurchaseReqnItem": {
                        "results": [
                            {
                                "PurchaseRequisitionItem": test_data[
                                    "purchase_requisition_item_id"
                                ],
                                "PurchasingGroup": test_data["purchasing_group"],
                                "PurchasingOrganization": test_data["purchasing_organization"],
                                "Plant": test_data["plant"],
                                "Material": test_data["material"],
                                "MaterialGroup": test_data["material_group"],
                                "CreationDate": test_data["creation_date"],
                                "DeliveryDate": test_data["delivery_date"],
                                "PurchaseRequisitionReleaseDate": test_data["release_date"],
                                "PurReqnItemCurrency": test_data["currency"],
                                "RequestedQuantity": test_data["requested_quantity"],
                                "PurchaseRequisitionPrice": test_data["price"],
                                "ItemNetAmount": test_data["net_amount"],
                                "RequisitionerName": test_data["requisitioner_name"],
                                "BaseUnit": test_data["base_unit"],
                                "to_PurchaseReqnDeliveryAddress": {
                                    "PostalCode": test_data["postal_code"],
                                    "CityName": test_data["city"],
                                    "Country": test_data["country"],
                                    "Region": test_data["region"],
                                },
                            }
                        ]
                    },
                }
            }
        }

        response = sap_s4_hana_get_purchase_requisition_items(
            purchase_requisition_id=test_data["purchase_requisition_id"]
        ).content

        assert response
        assert (
            response.purchase_requisition_items[0].purchase_requisition_item_id
            == test_data["purchase_requisition_item_id"]
        )
        assert response.purchase_requisition_items[0].city == test_data["city"]
        assert response.purchase_requisition_items[0].postal_code == test_data["postal_code"]

        mock_client.get_request.assert_any_call(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader('{test_data['purchase_requisition_id']}')",
            expand_expr="to_PurchaseReqnItem,to_PurchaseReqnItem/to_PurchaseReqnDeliveryAddress",
        )
