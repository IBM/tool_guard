from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAContract:
    """Represents a contract in SAP S4 HANA."""

    contract_id: str
    company_code: str
    creation_date: str
    created_by_user: str
    supplier: str
    purchasing_processing_status_name: Optional[str] = None


@dataclass
class S4HANAContractsResponse:
    """Represents the response from retrieving a list of contracts in SAP S4 HANA."""

    contracts: List[S4HANAContract]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_contracts(
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    created_by: Optional[str] = None,
    supplier: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAContractsResponse]:
    """
    Gets the list of the contracts from SAP S4 HANA.

    Args:
        created_after: The start date of the range for creation date given by user in ISO 8601
            format (e.g., YYYY-MM-DD).
        created_before: The end date of the range for creation date given by user in ISO 8601 format
            (e.g., YYYY-MM-DD).
        created_by: The user name of the person who created the contract.
        supplier: The supplier associated to the contract, returned by `sap_s4_hana_get_suppliers`
            tool.
        limit: The number of contracts returned.
        skip: The number of contracts to skip for pagination.

    Returns:
        A list of contracts.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filters = []
    if created_after:
        filters.append(f"CreationDate ge datetime'{(created_after)}T00:00:00'")
    if created_before:
        filters.append(f"CreationDate le datetime'{(created_before)}T00:00:00'")
    if supplier:
        filters.append(f"Supplier eq '{supplier}'")
    if created_by:
        filters.append(f"CreatedByUser eq '{created_by}'")

    filter_expr = " and ".join(filters) if filters else None
    params = {"$top": limit, "$skip": skip}

    response = (
        client.get_request(
            entity="100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract",
            filter_expr=filter_expr,
            params=params,
        )
        if filter_expr
        else client.get_request(
            entity="100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract",
            params=params,
        )
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    results = response.get("response", {}).get("d", {}).get("results", [])
    contracts: List[S4HANAContract] = []

    for result in results:
        contracts.append(
            S4HANAContract(
                contract_id=result.get("PurchaseContract", ""),
                company_code=result.get("CompanyCode", ""),
                creation_date=(sap_date_to_iso_8601(result.get("CreationDate", ""))),
                created_by_user=result.get("CreatedByUser", ""),
                supplier=result.get("Supplier", ""),
                purchasing_processing_status_name=result.get("PurchasingProcessingStatusName", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved.",
        content=S4HANAContractsResponse(contracts=contracts),
    )
