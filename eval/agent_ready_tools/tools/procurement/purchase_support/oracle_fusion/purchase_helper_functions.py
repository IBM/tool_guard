from typing import Any, Dict, List

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseRequisitionDetails,
    OracleFusionPurchaseRequisitionItemBilling,
    OracleFusionPurchaseRequisitionLineDetails,
)


def oracle_fusion_build_requisition_line_from_response(
    response: Dict[str, Any],
) -> OracleFusionPurchaseRequisitionLineDetails:
    """
    Utility function to build a requisition line from a requisition response.

    Args:
        response: The requisition line response from calling a requisition/req_line endpoint.

    Returns:
        The resulting requisition line after building it.
    """

    return OracleFusionPurchaseRequisitionLineDetails(
        requisition_line_id=response.get("RequisitionLineId", -1),
        line_number=response.get("LineNumber", -1),
        category_name=response.get("CategoryName", ""),
        item_description=response.get("ItemDescription", ""),
        item_id=response.get("ItemId", -1),
        item=response.get("Item", ""),
        quantity=response.get("Quantity", 0),
        requester=response.get("RequesterDisplayName", ""),
        unit_price=response.get("UnitPrice", 0),
        unit_of_measure=response.get("UOM", ""),
        price=response.get("Price", 0),
        line_status=response.get("LineStatusDisplayValue", ""),
        purchase_order=response.get("PurchaseOrder", ""),
        deliver_to_location_code=response.get("DeliverToLocationCode", ""),
        destination_type=response.get("DestinationType", ""),
        buyer=response.get("BuyerOnPurchaseOrder", ""),
        supplier_on_purchase_order=response.get("SupplierOnPurchaseOrder", ""),
        supplier_item_number=response.get("SupplierItemNumber", 0),
        source_agreement=response.get("SourceAgreement", ""),
        requested_delivery_date=response.get("RequestedDeliveryDate", ""),
        billing_details=[
            OracleFusionPurchaseRequisitionItemBilling(
                requisition_distribution_id=item.get("RequisitionDistributionId", -1),
                distribution_number=item.get("DistributionNumber", -1),
                billing_quantity=item.get("Quantity", 0),
                charge_account_id=item.get("ChargeAccountId", -1),
                charge_account=item.get("ChargeAccount", ""),
                billing_amount=item.get("CurrencyAmount", 0),
                budget_date=item.get("BudgetDate", ""),
            )
            for item in response.get("distributions", [])
        ],
    )


def oracle_fusion_add_requisition_lines(
    response: List[Dict[str, Any]],
) -> List[OracleFusionPurchaseRequisitionLineDetails]:
    """
    Utility function to build requisition lines from a requisition response.

    Args:
        response: Requisition lines response object

    Returns:
        List of requisition line objects
    """
    requisition_lines = []
    for req_line in response:
        requisition_lines.append(oracle_fusion_build_requisition_line_from_response(req_line))

    return requisition_lines


def oracle_fusion_build_requisition_from_response(
    response: Dict[str, Any],
) -> OracleFusionPurchaseRequisitionDetails:
    """
    Utility function to build a requisition from a requisition response.

    Args:
        response: The requisition response from calling a requisition endpoint.

    Returns:
        The resulting requisition after building it.
    """
    return OracleFusionPurchaseRequisitionDetails(
        purchase_requisition_id=response.get("RequisitionHeaderId", -1),
        preparer=response.get("Preparer", ""),
        description=response.get("Description", ""),
        document_status=response.get("DocumentStatus", ""),
        creation_date=response.get("CreationDate", ""),
        fund_status=response.get("FundsStatus", ""),
        justification=response.get("Justification", ""),
        requisition_number=response.get("Requisition", ""),
        requisitioning_business_unit_id=response.get("RequisitioningBUId", -1),
        requisitioning_business_unit=response.get("RequisitioningBU", ""),
        preparer_id=response.get("PreparerId", -1),
        identification_key=response.get("IdentificationKey", ""),
        requisition_line_group=response.get("RequisitionLineGroup", ""),
        taxation_country=response.get("TaxationCountry", ""),
        purchase_requisition_items=oracle_fusion_add_requisition_lines(response.get("lines", [])),
    )
