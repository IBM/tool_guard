from typing import Dict, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierDetails,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_all_suppliers(
    limit: int = 10,
    offset: int = 0,
    supplier_name: Optional[str] = None,
    supplier_number: Optional[str] = None,
    supplier_id: Optional[int] = None,
    supplier_type: Optional[str] = None,
    business_relationship: Optional[str] = None,
    creation_date: Optional[str] = None,
) -> ToolResponse[List[OracleFusionSupplierDetails]]:
    """
    Get all suppliers from Oracle Fusion. Fetches suppliers and dynamically builds the 'q' query
    parameter.

    Args:
        limit: number of suppliers returned
        offset: number of suppliers to skip for pagination
        supplier_name: Name of a Supplier
        supplier_number: String of Letters and Number representing a  Supplier
        supplier_id: Unique Int for a supplier
        supplier_type: Type of Supplier
        business_relationship: Relationship to Supplier
        creation_date: Date Created

    Returns:
        A list of suppliers
    """
    filter_map = {
        "Supplier": supplier_name,
        "SupplierNumber": supplier_number,
        "SupplierID": supplier_id,
        "SupplierTypeCode": supplier_type,
        "BusinessRelationshipCode": business_relationship,
        "CreationDate>": creation_date,
    }

    expressions = [f"{field}={value}" for field, value in filter_map.items() if value is not None]

    query_string = ";".join(expressions) if expressions else None

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Union[str, int]] = {
        "limit": limit,
        "offset": offset,
    }

    if query_string:
        params["q"] = query_string

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(resource_name="suppliers", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No suppliers returned")

    suppliers = []
    for supplier in response["items"]:
        suppliers.append(
            OracleFusionSupplierDetails(
                supplier_id=supplier["SupplierId"],
                supplier_name=supplier["Supplier"],
                supplier_status=supplier["Status"],
                supplier_type_code=supplier["SupplierTypeCode"],
                supplier_creation_date=supplier["CreationDate"],
            )
        )

    return ToolResponse(
        success=True,
        message="Returned a list of suppliers from Oracle Fusion successfully",
        content=suppliers,
    )
