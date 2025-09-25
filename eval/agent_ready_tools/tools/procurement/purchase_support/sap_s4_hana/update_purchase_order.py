from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    S4HANAInternationalCommercialTermsTypes,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_purchase_order(
    purchase_order_id: str,
    payment_terms: Optional[str] = None,
    purchase_order_date: Optional[str] = None,
    document_currency: Optional[str] = None,
    exchange_rate: Optional[str] = None,
    supplier_phone_number: Optional[str] = None,
    incoterms_classification: Optional[S4HANAInternationalCommercialTermsTypes] = None,
    city_name: Optional[str] = None,
    fax_number: Optional[str] = None,
    house_number: Optional[str] = None,
    address_name: Optional[str] = None,
    postal_code: Optional[str] = None,
    street_name: Optional[str] = None,
    address_phone_number: Optional[str] = None,
    region: Optional[str] = None,
    country: Optional[str] = None,
) -> ToolResponse:
    """
    Updates the purchase order in SAP S4 HANA.

    Args:
        purchase_order_id: The id of the purchase order returned by `sap_s4_hana_get_purchase_orders` tool.
        payment_terms: The payment terms of the purchase order.
        purchase_order_date: The purchase order date in `YYYY-MM-DD` format.
        document_currency: The 3-digit currency code of the purchase order.
        exchange_rate: The exchange rate of the purchase order.
        supplier_phone_number: The supplier phone number of the purchase order.
        incoterms_classification: The international commercial terms agreed upon between buyer and seller.
        city_name: The address city name of the purchase order.
        fax_number: The address fax number of the purchase order.
        house_number: The address house number of the purchase order.
        address_name: The address name of the purchase order.
        postal_code: The address postal code of the purchase order.
        street_name: The address street name of the purchase order.
        address_phone_number: The address phone number of the purchase order.
        region: The address region of the purchase order.
        country: The address country of the purchase order.

    Returns:
        The http code of the update response.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "PaymentTerms": payment_terms,
        "PurchaseOrderDate": purchase_order_date,
        "DocumentCurrency": document_currency,
        "ExchangeRate": exchange_rate,
        "SupplierPhoneNumber": supplier_phone_number,
        "IncotermsClassification": incoterms_classification,
        "AddressCityName": city_name,
        "AddressFaxNumber": fax_number,
        "AddressHouseNumber": house_number,
        "AddressName": address_name,
        "AddressPostalCode": postal_code,
        "AddressStreetName": street_name,
        "AddressPhoneNumber": address_phone_number,
        "AddressRegion": region,
        "AddressCountry": country,
    }

    if incoterms_classification:
        payload["IncotermsClassification"] = S4HANAInternationalCommercialTermsTypes[
            incoterms_classification.upper()
        ].value

    if purchase_order_date:
        payload["PurchaseOrderDate"] = iso_8601_to_sap_date(purchase_order_date)

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(
        entity=f"API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder('{purchase_order_id}')",
        payload=payload,
    )
    if "error" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["error"]["message"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    result = response
    return ToolResponse(
        success=True,
        message="The data was successfully updated",
        content=result,
    )
