from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.common_classes_contract_management import (
    SAPS4HANAContractItemDetails,
    SAPS4HANAContractPaymentDetails,
    SAPS4HANAContractTypes,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    S4HanaSupplierAddress,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class SAPS4HANAContractDetails:
    """Represents the details of a contract in SAP S4 HANA."""

    contract_id: str
    contract_type: str
    purchasing_group: str
    company_code: str
    purchasing_organization: str
    supplier_id: str
    contract_start_date: Optional[str] = None
    contract_end_date: Optional[str] = None
    status: Optional[str] = None
    item_details: Optional[List[SAPS4HANAContractItemDetails]] = None
    supplier_address: Optional[List[S4HanaSupplierAddress]] = None
    payment_details: Optional[List[SAPS4HANAContractPaymentDetails]] = None


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_contract_by_id(
    contract_id: str,
) -> ToolResponse[SAPS4HANAContractDetails]:
    """
    Gets the details of a contract from SAP S4 HANA.

    Args:
        contract_id: The id of the contract, returned by the sap_s4_hana_get_contracts tool.

    Returns:
        The response containing the details of a contract.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    response = client.get_request(
        entity=f"100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract('{contract_id}')",
        expand_expr=f"to_PurchaseContractItem/to_PurCtrAddress",
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    item = response.get("response", {}).get("d", {})

    contract_details = SAPS4HANAContractDetails(
        contract_id=item.get("PurchaseContract", ""),
        contract_type=SAPS4HANAContractTypes(item.get("PurchaseContractType", "")).name,
        purchasing_group=item.get("PurchasingGroup", ""),
        company_code=item.get("CompanyCode", ""),
        purchasing_organization=item.get("PurchasingOrganization", ""),
        supplier_id=item.get("Supplier", ""),
        contract_start_date=sap_date_to_iso_8601(item.get("ValidityStartDate", "")),
        contract_end_date=sap_date_to_iso_8601(item.get("ValidityEndDate", "")),
        status=item.get("PurchasingProcessingStatusName", ""),
        item_details=[
            SAPS4HANAContractItemDetails(
                item_number=item.get("PurchaseContractItem", ""),
                item_description=item.get("PurchaseContractItemText", ""),
                material=item.get("Material", ""),
                material_group=item.get("MaterialGroup", ""),
                net_price=item.get("ContractNetPriceAmount", ""),
                net_price_quantity=item.get("NetPriceQuantity", ""),
                target_quantity=item.get("TargetQuantity", ""),
                price_unit=item.get("OrderQuantityUnit", ""),
                production_plant=item.get("Plant", ""),
                product_type=item.get("ProductType", ""),
            )
            for item in item.get("to_PurchaseContractItem", {}).get("results", [])
        ],
        supplier_address=[
            S4HanaSupplierAddress(
                address_id=address.get("AddressID", ""),
                street_name=address.get("StreetName", ""),
                house_number=address.get("HouseNumber", ""),
                postal_code=address.get("PostalCode", ""),
                city=address.get("CityName", ""),
                country=address.get("Country", ""),
                region=address.get("Region", ""),
                time_zone=address.get("AddressTimeZone", ""),
            )
            for item in item.get("to_PurchaseContractItem", {}).get("results", [])
            for address in item.get("to_PurCtrAddress", {}).get("results", [])
        ],
        payment_details=[
            SAPS4HANAContractPaymentDetails(
                payment_terms=item.get("PaymentTerms", ""),
                payment_in_days1=item.get("CashDiscount1Days", ""),
                cash_discount_percentage1=item.get("CashDiscount1Percent", ""),
                payment_in_days2=item.get("CashDiscount2Days", ""),
                cash_discount_percentage2=item.get("CashDiscount2Percent", ""),
                net_payment_days=item.get("NetPaymentDays", ""),
                target_value=item.get("PurchaseContractTargetAmount", ""),
                currency=item.get("DocumentCurrency", ""),
                exchange_rate=item.get("ExchangeRate", ""),
                exchange_rate_fixed=item.get("ExchangeRateIsFixed") or False,
                total_net_value=str(
                    sum(
                        float(item.get("ContractNetPriceAmount", ""))
                        for item in item.get("to_PurchaseContractItem", {}).get("results", [])
                    )
                ),
            )
        ],
    )
    return ToolResponse(
        success=True, message="The data was successfully retrieved", content=contract_details
    )
