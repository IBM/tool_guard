from typing import Any, Dict, List

from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
    CoupaApproval,
    CoupaApprover,
    CoupaComment,
    CoupaOrderLine,
    CoupaOrderLines,
    CoupaPurchaseOrder,
    CoupaRequisition,
    CoupaRequisitionLine,
)


def coupa_build_address(address: Dict[str, Any]) -> CoupaAddress:
    """
    Helper function for building a shipping address.

    Args:
        address: The ship to address response from the requisition response.

    Returns:
        The resulting shipping address object.
    """
    return CoupaAddress(
        id=address.get("id", 0),
        location_code=address.get("location-code", ""),
        street1=address.get("street1", ""),
        city=address.get("city", ""),
        postal_code=address.get("postal-code", ""),
        state=address.get("state", ""),
        country=address.get("country", {}).get("name", ""),
    )


def coupa_build_purchase_order_from_response(
    response: Dict[str, Any],
) -> CoupaPurchaseOrder:
    """
    Utility function to build a purchase order from a purchase order response.

    Args:
        response: The purchase order response from calling a purchase order endpoint.

    Returns:
        The resulting purchase order after building it.
    """
    order_lines = CoupaOrderLines(
        order_lines=[
            CoupaOrderLine(
                order_line_id=order_line.get("id", 0),
                order_line_description=order_line.get("description", ""),
                order_line_type=order_line.get("type", ""),
                order_line_num=order_line.get("line-num", ""),
                item_description=order_line.get("item", {}).get("description", None),
                quantity=order_line.get("quantity", None),
                unit=order_line.get("item", {}).get("uom", {}).get("name", None),
                price=order_line.get("price", ""),
                total=order_line.get("total", ""),
                account_id=order_line.get("account", {}).get("id", 0),
                account_type_id=order_line.get("account", {}).get("account-type", {}).get("id", 0),
                uom_code=order_line.get("uom", {}).get("code", ""),
                estimated_tax_amount=order_line.get("estimated-tax-amount", ""),
                total_with_estimated_tax=order_line.get("total-with-estimated-tax", ""),
                amount_received=order_line.get("received", 0),
                supplier_part_number=order_line.get("source-part-num", ""),
                supplier_auxiliary_part_number=order_line.get("supp-aux-part-num", ""),
                commodity=order_line.get("commodity", {}).get("name"),
                manufacturer_name=order_line.get("manufacturer-name", ""),
                manufacturer_part_number=order_line.get("manufacturer-part-number", ""),
                receipt_approval_required=order_line.get("receipt-approval-required", False),
                need_by_date=order_line.get("need-by-date", None),
                savings_percent=order_line.get("savings-pct", ""),
                billing_account_id=order_line.get("account", {}).get("id"),
                period=order_line.get("period", {}).get("name"),
            )
            for order_line in response.get("order-lines", [])
        ]
    )

    shipping_address = coupa_build_address(response["ship-to-address"])

    purchase_order = CoupaPurchaseOrder(
        purchase_order_id=response.get("id", 0),
        po_number=response.get("po-number", ""),
        created_by=response["created-by"]["login"],
        updated_by=response["updated-by"]["login"],
        created_at=response.get("created-at", ""),
        updated_at=response.get("updated-at", ""),
        status=response.get("status", ""),
        transmission_status=response.get("transmission-status", ""),
        exported=response.get("exported", False),
        ship_to_attention=response.get("ship-to-attention", ""),
        requested_by=response["requisition-header"]["requested-by"].get("fullname", ""),
        payment_method=response.get("payment-method", ""),
        currency=response["currency"].get("code"),
        estimated_tax_amount=response.get("estimated-tax-amount", ""),
        total_with_estimated_tax=response.get("total-with-estimated-tax", ""),
        requisition_number=response["requisition-header"].get("id", 0),
        shipping_address=shipping_address,
        supplier_id=response["supplier"].get("id", 0),
        supplier_name=response["supplier"].get("name", ""),
        requisition=coupa_build_requisition_from_response(response["requisition-header"]),
        order_lines=order_lines,
        shipping_terms=response.get("shipping-term", {}).get("code"),
        payment_terms=response.get("payment-term", {}).get("code"),
        department=response["order-lines"][0].get("department", {}).get("name"),
    )

    return purchase_order


def coupa_build_requisition_line_from_response(response: Dict[str, Any]) -> CoupaRequisitionLine:
    """
    Utility function to build a requisition from a requisition line response.

    Args:
        response: The requisition line response from calling a requisition/req_line endpoint.

    Returns:
        The resulting requisition line after building it.
    """

    return CoupaRequisitionLine(
        id=response["id"],
        description=response["description"],
        unit_price=float(response["unit-price"]),
        currency=response["currency"].get("code"),
        line_type=response["line-type"],
        line_num=response["line-num"],
        total_with_estimated_tax=response["total-with-estimated-tax"],
        supplier_id=(response["supplier"]["id"] if response.get("supplier") else None),
        billing_account_id=(response["account"]["id"] if response.get("account") else None),
        # EXTRA THINGS REQUISITION QUANTITY LINE
        quantity=response.get("quantity"),
        uom=(response.get("uom") or {}).get("name"),
        # EXTRA THINGS REQUISITION AMOUNT LINE
        commodity=(response.get("commodity") or {}).get("name"),
        supplier_part_number=response.get("source-part-num"),
        shipping_terms=(response.get("shipping-term") or {}).get("code"),
        payment_terms=(response.get("payment-term") or {}).get("code"),
        need_by_date=response.get("need-by-date"),
        transmission_method=response.get("transmission-method-override"),
        manufacturer_name=response.get("manufacturer-name"),
        manufacturer_part_number=response.get("manufacturer-part-number"),
        item_id=(response["item"]["id"] if response.get("item") else None),
        item_name=(response["item"]["name"] if response.get("item") else None),
        item_description=(response["item"]["description"] if response.get("item") else None),
        item_number=(response["item"]["item-number"] if response.get("item") else None),
        item_manufacturer_name=(
            response["item"]["manufacturer-name"] if response.get("item") else None
        ),
        item_manufacturer_part_number=(
            response["item"]["manufacturer-part-number"] if response.get("item") else None
        ),
    )


def coupa_add_requisition_lines(response: List[Dict[str, Any]]) -> List[CoupaRequisitionLine]:
    """
    Utility function to build a requisition lines from a requisition response.

    Args:
        response: Requisition lines response object

    Returns:
        List of requisition line objects
    """
    requisition_lines = []
    for req_line in response:
        requisition_lines.append(coupa_build_requisition_line_from_response(req_line))

    return requisition_lines


def coupa_build_requisition_from_response(response: Dict[str, Any]) -> CoupaRequisition:
    """
    Utility function to build a requisition from a requisition response.

    Args:
        response: The requisition response from calling a requisition endpoint.

    Returns:
        The resulting requisition after building it.
    """

    # get approvals and store their ids in a list to preserve the approval chain
    # approvals can contain multiple or be empty if the requisition status is not pending approval so we need to check
    # helpful for seeing if we need to approve more than just the current approval
    approvals_dict = response.get("approvals")
    approval_id_list = (
        [approval.get("id") for approval in approvals_dict if approval] if approvals_dict else None
    )

    current_approval_dict = response.get("current-approval")
    current_approval = (
        coupa_build_approval_from_response(current_approval_dict) if current_approval_dict else None
    )

    result_requisition = CoupaRequisition(
        id=response["id"],
        created_at=response["created-at"],
        updated_at=response["updated-at"],
        created_by=response["created-by"]["login"],
        updated_by=response["updated-by"]["login"],
        requested_by=response["requested-by"]["login"],
        status=response["status"],
        currency=response["currency"]["code"],
        line_count=response["line-count"],
        total_with_estimated_tax=response["total-with-estimated-tax"],
        need_by_date=response.get("need-by-date"),
        business_unit=(response.get("department", {}).get("name")),
        business_purpose=response.get("justification"),
        ship_to_address=(
            coupa_build_address(response["ship-to-address"])
            if response.get("ship-to-address")
            else None
        ),
        ship_to_attention=response.get("ship-to-attention"),
        current_approval=current_approval,
        approval_id_list=approval_id_list,
        requisition_lines=coupa_add_requisition_lines(response["requisition-lines"]),
    )

    return result_requisition


def coupa_build_comment_from_response(response: Dict[str, Any]) -> CoupaComment:
    """
    Utility function to build comments given an individual comment response in the list.

    Args:
        response: The response of a comment

    Returns:
        The constructed comment
    """
    return CoupaComment(
        comment_id=response["id"],
        created_at=response["created-at"],
        updated_at=response["updated-at"],
        commentable_id=response["commentable-id"],
        commentable_type=response["commentable-type"],
        comment_text=response["comments"],
        created_by=response["created-by"]["login"],
        updated_by=response["updated-by"]["login"],
    )


def coupa_build_approval_from_response(response: Dict[str, Any]) -> CoupaApproval:
    """
    Utility function which builds an approval object in Coupa.

    Args:
        response: The response from calling the approval endpoint.

    Returns:
        The resulting approval after approving.
    """
    approver_dict = response.get("approver")
    approver = (
        CoupaApprover(
            approver_id=approver_dict.get("id", 0),
            approver_login=approver_dict.get("login", ""),
            approver_fullname=approver_dict.get("fullname", ""),
        )
        if approver_dict
        else None
    )

    approved_by_dict = response.get("approved-by")
    approved_by = (
        CoupaApprover(
            approver_id=approved_by_dict.get("id", 0),
            approver_login=approved_by_dict.get("login", ""),
            approver_fullname=approved_by_dict.get("fullname", ""),
        )
        if approved_by_dict
        else None
    )

    return CoupaApproval(
        approval_id=response.get("id", 0),
        created_at=response.get("created-at", ""),
        updated_at=response.get("updated-at", ""),
        status=response.get("status", ""),
        approval_date=response.get("approval-date", None),
        approvable_type=response.get("approvable-type", ""),
        approver_type=response.get("approver-type", ""),
        approvable_id=response.get("approvable-id", 0),
        approver=approver,
        approved_by=approved_by,
    )
