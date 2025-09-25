from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseRequisitionHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_all_purchase_requisitions(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    requisition_number: Optional[str] = None,
    preparer: Optional[str] = None,
    description: Optional[str] = None,
    document_status: Optional[str] = None,
    creation_date_start: Optional[str] = None,
    creation_date_end: Optional[str] = None,
) -> ToolResponse[List[OracleFusionPurchaseRequisitionHeader]]:
    """
    Get all purchase requisitions from Oracle Fusion.

    Args:
        limit: number of requisitions returned.
        offset: number of requisitions to skip for pagination.
        requisition_number: The number of the requisition.
        preparer: The person who initiated the purchase request.
        description: The description of the purchase requisition.
        document_status: The status of the purchase requisition.
        creation_date_start: The start of the date range for getting purchase requisitions in iso 8601 format(YYYY-MM-DD).
        creation_date_end: The end of the date range for getting purchase requisitions in iso 8601 format(YYYY-MM-DD).

    Returns:
        A list of purchase requisitions
    """
    filter_map = {
        "Requisition": requisition_number,
        "Preparer": preparer,
        "Description": description,
        "DocumentStatus": document_status,
    }

    expressions = [f"{field}={value}" for field, value in filter_map.items() if value is not None]

    # Handling creation date range

    if creation_date_start and creation_date_end:
        expressions.append(f'CreationDate >= "{creation_date_start}" and <= "{creation_date_end}"')
    elif creation_date_start:
        expressions.append(f'CreationDate >= "{creation_date_start}"')
    elif creation_date_end:
        expressions.append(f'CreationDate <= "{creation_date_end}"')

    query_string = ";".join(expressions) if expressions else None

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {
        "limit": limit,
        "offset": offset,
    }

    if query_string:
        params["q"] = query_string

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(resource_name="purchaseRequisitions", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No requisitions returned")

    requisition_list = []
    for purchase_requisition in response["items"]:
        requisition_list.append(
            OracleFusionPurchaseRequisitionHeader(
                purchase_requisition_id=purchase_requisition["RequisitionHeaderId"],
                requisition_number=purchase_requisition["Requisition"],
                preparer=purchase_requisition["Preparer"],
                description=purchase_requisition["Description"],
                document_status=purchase_requisition["DocumentStatus"],
                creation_date=purchase_requisition["CreationDate"],
                fund_status=purchase_requisition["FundsStatus"],
                justification=purchase_requisition["Justification"],
            )
        )

    return ToolResponse(
        success=True,
        message="Returned a list of requisitions from Oracle Fusion successfully",
        content=requisition_list,
    )
