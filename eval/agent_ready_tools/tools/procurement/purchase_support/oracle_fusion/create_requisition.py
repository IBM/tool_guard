from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseRequisitionDetails,
)
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_helper_functions import (
    oracle_fusion_build_requisition_from_response,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_create_requisition(
    preparer_email: str,
    requisition_bu: str,
    requisition_description: str,
    quantity: int,
    requested_date: str,
    distribution_number: int = 1,
    item_description: Optional[str] = None,
    item_number: Optional[str] = None,
    justification: Optional[str] = None,
) -> ToolResponse[OracleFusionPurchaseRequisitionDetails]:
    """
    Create a purchase requisition in Oracle Fusion.

    Args:
        preparer_email: Email of the person who is creating the requisition
        requisition_bu: Requisition business unit name
        requisition_description: Description of what the requisition has
        quantity: Quantity of the specified item for the requisition
        requested_date: The requested budget and delivery date for the requisition in ISO 8601 format (e.g., YYYY-MM-DD).
        distribution_number: Distribution number for the billing of the requisition, default 1
        item_description: Description of the initial item being added to the requisition
        item_number: Display number of the initial item being added to the requisition
        justification: Justification of what the requisition is for

    Returns:
        The created purchase requisition.
    """
    if not (item_description or item_number):
        return ToolResponse(
            success=False, message="Requisition needs item_description and/or item_number."
        )

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # Part 1: get user defaults - returns current user based on credentials
    user_pref_response = client.get_request(
        resource_name="requisitionPreferences", params={"expand": "favoriteChargeAccounts"}
    )
    if "errors" in user_pref_response:
        return ToolResponse(success=False, message=user_pref_response["errors"])

    if "items" not in user_pref_response or not user_pref_response["items"]:
        return ToolResponse(
            success=False, message="No requisition preferences found for current user."
        )

    # pick the first default user preferences if there are multiple
    user_defaults = user_pref_response["items"][0]

    favorite_accounts = user_defaults.get("favoriteChargeAccounts", [])

    # default use the charge account that is tagged as primary if there are multiple
    # if primary charge acc is None the user will just have to update it using the update item tool
    primary_charge_acc = None
    for account in favorite_accounts:
        if account.get("PrimaryFlag") is True:
            primary_charge_acc = account["ChargeAccount"]
            break

    # Part 2: Get the item details for the provided item_number and/or item_description
    filter_map = {"Item": item_number, "Description": item_description}

    expressions = []
    for field, value in filter_map.items():
        if value:
            if str(value).isdigit():
                # isdigit for ids, adk tends to still have strings as input regardless
                expressions.append(f"{field} = {value}")
            else:
                # partial/lenient match on strings
                expressions.append(f"{field} LIKE '%{value}%'")

    query_string = "; ".join(expressions) if expressions else None

    item_response = client.get_request(
        resource_name="purchaseAgreementLines", params={"q": query_string}
    )

    if "errors" in item_response:
        return ToolResponse(success=False, message=item_response["errors"])

    if "items" not in item_response or not item_response["items"]:
        return ToolResponse(
            success=False, message="No purchase agreement items matched the search criteria."
        )

    # pick the first item that shows up in the results
    item_properties = item_response["items"][0]

    # Part 3: Payload construction - requisition general details + 1 line
    requisition_payload: dict[str, Any] = {
        key: value
        for key, value in {
            "RequisitioningBU": requisition_bu,
            "PreparerEmail": preparer_email,
            "ExternallyManagedFlag": False,
            "Description": requisition_description,
            "Justification": justification,
            # not including procurement card id yet because currently it's optional and I don't have the values for it
        }.items()
        if value not in (None, "")  # include values like 0 still
    }

    lines = {
        "lines": [
            {
                "ItemId": item_properties.get("ItemId"),
                "Quantity": quantity,
                "DestinationOrganizationCode": user_defaults.get("DestinationOrganizationCode"),
                "DeliverToLocationCode": user_defaults.get("DeliverToLocationCode"),
                "LineTypeId": item_properties.get("LineTypeId"),
                "SupplierId": item_properties.get("SupplierId"),
                "Supplier": item_properties.get("Supplier"),
                "SupplierSiteId": item_properties.get("SupplierSiteId"),
                "SupplierSite": item_properties.get("SupplierSite"),
                "SourceAgreement": item_properties.get("AgreementNumber"),
                "SourceAgreementHeaderId": item_properties.get("AgreementHeaderId"),
                "SourceAgreementLineNumber": item_properties.get("LineNumber"),
                "SourceAgreementLineId": item_properties.get("AgreementLineId"),
                "Price": item_properties.get("Price"),
                "UOM": item_properties.get("UOM"),
                "CurrencyCode": item_properties.get("CurrencyCode"),
                # default to requisition prefs
                "DestinationTypeCode": user_defaults.get("DestinationTypeCode"),
                "RequesterEmail": preparer_email,
                "RequestedDeliveryDate": requested_date,
                "distributions": [
                    {
                        "DistributionNumber": distribution_number,
                        "ChargeAccount": primary_charge_acc,
                        "Quantity": quantity,
                        "BudgetDate": requested_date,
                    }
                ],
            }
        ]
    }

    requisition_payload.update(lines)

    response = client.post_request(
        resource_name="purchaseRequisitions",
        payload=requisition_payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    purchase_requisition = oracle_fusion_build_requisition_from_response(response)

    return ToolResponse(
        success=True,
        message="Requisition created successfully.",
        content=purchase_requisition,
    )
