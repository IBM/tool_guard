from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    S4HANAInternationalCommercialTermsTypes,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.update_purchase_order import (
    sap_s4_hana_update_purchase_order,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_update_purchase_order() -> None:
    """Test that the sap_s4_hana_update_purchase_order tool updates purchase order successfully."""

    # Define test data
    test_data = {
        "purchase_order_id": "4500000123",
        "payment_terms": "0001",
        "purchase_order_date": "2018-03-28",
        "document_currency": "INR",
        "exchange_rate": "25",
        "supplier_phone_number": "123456789",
        "incoterms_classification": "costs_and_freight",
        "city_name": "Hyd",
        "fax_number": "1325",
        "house_number": "13",
        "address_name": "PO Transmission update sample",
        "postal_code": "52001",
        "street_name": "Alind colony",
        "address_phone_number": "7093398682",
        "region": "13",
        "country": "IN",
        "http_code": 204,
    }
    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.update_purchase_order.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": test_data["http_code"]}

        # Call the function under test
        response = sap_s4_hana_update_purchase_order(
            purchase_order_id=test_data["purchase_order_id"],
            payment_terms=test_data["payment_terms"],
            purchase_order_date=test_data["purchase_order_date"],
            document_currency=test_data["document_currency"],
            exchange_rate=test_data["exchange_rate"],
            supplier_phone_number=test_data["supplier_phone_number"],
            incoterms_classification=test_data["incoterms_classification"],
            city_name=test_data["city_name"],
            fax_number=test_data["fax_number"],
            house_number=test_data["house_number"],
            address_name=test_data["address_name"],
            postal_code=test_data["postal_code"],
            street_name=test_data["street_name"],
            address_phone_number=test_data["address_phone_number"],
            region=test_data["region"],
            country=test_data["country"],
        ).content

        # Ensure that update_purchase_order() executed and returned proper values
        assert response
        assert response["http_code"] == test_data["http_code"]

        mock_client.patch_request.assert_called_once_with(
            entity=f"API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder('{test_data["purchase_order_id"]}')",
            payload={
                "PaymentTerms": test_data["payment_terms"],
                "PurchaseOrderDate": iso_8601_to_sap_date(str(test_data["purchase_order_date"])),
                "DocumentCurrency": test_data["document_currency"],
                "ExchangeRate": test_data["exchange_rate"],
                "SupplierPhoneNumber": test_data["supplier_phone_number"],
                "IncotermsClassification": S4HANAInternationalCommercialTermsTypes[
                    str(test_data["incoterms_classification"]).upper()
                ].value,
                "AddressCityName": test_data["city_name"],
                "AddressFaxNumber": test_data["fax_number"],
                "AddressHouseNumber": test_data["house_number"],
                "AddressName": test_data["address_name"],
                "AddressPostalCode": test_data["postal_code"],
                "AddressStreetName": test_data["street_name"],
                "AddressPhoneNumber": test_data["address_phone_number"],
                "AddressRegion": test_data["region"],
                "AddressCountry": test_data["country"],
            },
        )
