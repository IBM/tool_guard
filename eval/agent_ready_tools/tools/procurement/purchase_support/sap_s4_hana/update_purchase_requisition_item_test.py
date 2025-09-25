from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.update_purchase_requisition_item import (
    sap_s4_hana_update_purchase_requisition_item,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_update_purchase_requisition_item_success() -> None:
    """Test that the sap_s4_hana_update_purchase_requisition_item tool updates successfully."""

    test_data = {
        "purchase_requisition_id": "10000329",
        "purchase_requisition_item_id": "10",
        "item_text": "Updated item description",
        "requested_quantity": "150",
        "price": "2.75",
        "delivery_date": "/Date(1750000000000)/",
        "material": "MAT12345",
        "material_group": "A002",
        "plant": "0001",
        "company_code": "0001",
        "purchasing_group": "001",
        "purchasing_organization": "1000",
        "currency": "EUR",
        "requisitioner_name": "WATSONXUSER1",
        "supplier": "SUPP001",
        "http_code": 204,
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.update_purchase_requisition_item.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana:

        mock_client = MagicMock()
        mock_sap_s4_hana.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": test_data["http_code"]}

        response = sap_s4_hana_update_purchase_requisition_item(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
            item_text=test_data["item_text"],
            requested_quantity=test_data["requested_quantity"],
            price=test_data["price"],
            delivery_date=test_data["delivery_date"],
            material=test_data["material"],
            material_group=test_data["material_group"],
            plant=test_data["plant"],
            company_code=test_data["company_code"],
            purchasing_group=test_data["purchasing_group"],
            purchasing_organization=test_data["purchasing_organization"],
            currency=test_data["currency"],
            requisitioner_name=test_data["requisitioner_name"],
            supplier=test_data["supplier"],
        ).content

        assert response["http_code"] == test_data["http_code"]

        mock_client.patch_request.assert_called_once_with(
            entity=(
                f"API_PURCHASEREQ_PROCESS_SRV/"
                f"A_PurchaseRequisitionItem(PurchaseRequisition='{test_data['purchase_requisition_id']}',"
                f"PurchaseRequisitionItem='{test_data['purchase_requisition_item_id']}')"
            ),
            payload={
                "PurchaseRequisitionItemText": test_data["item_text"],
                "RequestedQuantity": test_data["requested_quantity"],
                "PurchaseRequisitionPrice": test_data["price"],
                "DeliveryDate": sap_date_to_iso_8601(str(test_data["delivery_date"])),
                "Material": test_data["material"],
                "MaterialGroup": test_data["material_group"],
                "Plant": test_data["plant"],
                "CompanyCode": test_data["company_code"],
                "PurchasingGroup": test_data["purchasing_group"],
                "PurchasingOrganization": test_data["purchasing_organization"],
                "PurReqnItemCurrency": test_data["currency"],
                "RequisitionerName": test_data["requisitioner_name"],
                "Supplier": test_data["supplier"],
            },
        )
