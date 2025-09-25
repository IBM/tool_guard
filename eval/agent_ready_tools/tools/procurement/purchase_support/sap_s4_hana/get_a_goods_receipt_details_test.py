from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_a_goods_receipt_details import (
    sap_s4_hana_get_a_goods_receipt_details,
)


def test_get_a_goods_receipt_details() -> None:
    """Test that the `sap_s4_hana_get_a_goods_receipt_details` function returns the expected
    response."""

    test_data = {
        "document_date": "2024-02-10",
        "posting_date": "2024-02-12",
        "material_slip": "0080003161",
        "print_version": "",
        "material_document_header_text": "",
        "material_document_item": "1",
        "material_short_text": "N1-CERIALS",
        "quantity_in_unit_of_entry": "100",
        "entry_unit": "CAR",
        "storage_location": "0001",
        "gl_account": "893010",
        "stock_segment": "",
        "batch": "0000000170",
        "movement_type": "601",
        "plant": "MUM",
        "customer": "11",
        "supplier": "",
        "sales_order": "",
        "sales_order_item": "0",
        "purchase_order": "",
        "purchase_order_item": "0",
        "wbs_element": "",
        "quantity": "600.000",
        "base_unit": "KG",
        "material_number": "N1-CERIALS",
        "currency_code": "INR",
    }

    input_data = {"goods_receipt_id": "4900001653", "goods_receipt_year": "2024"}

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_a_goods_receipt_details.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "DocumentDate": test_data["document_date"],
                    "PostingDate": test_data["posting_date"],
                    "ReferenceDocument": test_data["material_slip"],
                    "VersionForPrintingSlip": test_data["print_version"],
                    "MaterialDocumentHeaderText": test_data["material_document_header_text"],
                    "to_MaterialDocumentItem": {
                        "results": [
                            {
                                "MaterialDocumentItem": test_data["material_document_item"],
                                "QuantityInEntryUnit": test_data["quantity_in_unit_of_entry"],
                                "EntryUnit": test_data["entry_unit"],
                                "StorageLocation": test_data["storage_location"],
                                "GLAccount": test_data["gl_account"],
                                "StockSegment": test_data["stock_segment"],
                                "Batch": test_data["batch"],
                                "GoodsMovementType": test_data["movement_type"],
                                "Plant": test_data["plant"],
                                "Customer": test_data["customer"],
                                "GoodsRecipientName": test_data["customer"],
                                "Supplier": test_data["supplier"],
                                "SalesOrder": test_data["sales_order"],
                                "SalesOrderItem": test_data["sales_order_item"],
                                "PurchaseOrder": test_data["purchase_order"],
                                "PurchaseOrderItem": test_data["purchase_order_item"],
                                "WBSElement": test_data["wbs_element"],
                                "QuantityInBaseUnit": test_data["quantity"],
                                "MaterialBaseUnit": test_data["base_unit"],
                                "Material": test_data["material_number"],
                                "CompanyCodeCurrency": test_data["currency_code"],
                            }
                        ]
                    },
                }
            }
        }

        response = sap_s4_hana_get_a_goods_receipt_details(
            goods_receipt_id=input_data["goods_receipt_id"],
            goods_receipt_year=input_data["goods_receipt_year"],
        ).content

        assert response
        assert response.document_date == test_data["document_date"]
        assert response.posting_date == test_data["posting_date"]
        assert response.material_slip == test_data["material_slip"]
        assert response.print_version == test_data["print_version"]
        assert response.material_document_header_text == test_data["material_document_header_text"]
        assert response.item_details[0].material_number == test_data["material_number"]
        assert (
            response.item_details[0].quantity_in_unit_of_entry
            == test_data["quantity_in_unit_of_entry"]
        )
        assert response.item_details[0].base_unit == test_data["base_unit"]
        assert response.item_details[0].currency_code == test_data["currency_code"]
        assert response.item_details[0].plant == test_data["plant"]
        assert response.item_details[0].storage_location == test_data["storage_location"]

    mock_client.get_request.assert_called_once_with(
        entity=f"API_MATERIAL_DOCUMENT_SRV1/A_MaterialDocumentHeader(MaterialDocumentYear='{input_data["goods_receipt_year"]}',MaterialDocument='{input_data["goods_receipt_id"]}')",
        expand_expr="to_MaterialDocumentItem",
    )
