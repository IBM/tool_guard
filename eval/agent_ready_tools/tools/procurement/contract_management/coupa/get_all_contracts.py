from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContract,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_contracts(
    name: Optional[str] = None,
    supplier_name: Optional[str] = None,
    supplier_id: Optional[int] = None,
    status: Optional[str] = None,
    offset: int = 0,
    start_date_start: Optional[str] = None,
    start_date_end: Optional[str] = None,
    end_date_start: Optional[str] = None,
    end_date_end: Optional[str] = None,
) -> ToolResponse[List[CoupaContract]]:
    """
    Get all contracts from Coupa.

    Args:
        name: A contract name filter, defaults to None
        supplier_name: str, defaults to None
        supplier_id: int, defaults to None
        status: A status filter, defaults to None
        offset: Offset multiplier for pagination
        start_date_start: The start of the date range for getting contracts start date. (YYYY-MM-DD)
        start_date_end: The end of the date range for getting contracts start date. (YYYY-MM-DD)
        end_date_start: The start of the date range for getting contracts end date. (YYYY-MM-DD)
        end_date_end: The end of the date range for getting contracts end date. (YYYY-MM-DD)

    Returns:
        A list of contracts
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: dict[str, Any] = {
        key: value
        for key, value in {
            "fields": '["id","name","no-of-renewals","number","reason-insight-events","renewal-length-unit","renewal-length-value","status","start-date","end-date",{"supplier": ["name","number","id","status"]},{"department": ["name","id","active"]}]',
            "name[contains]": name,
            "supplier[name][contains]": supplier_name,
            "supplier[id]": supplier_id,
            "status": status,
            "start-date[gt_or_eq]": start_date_start,
            "start-date[lt_or_eq]": start_date_end,
            "end-date[gt_or_eq]": end_date_start,
            "end-date[lt_or_eq]": end_date_end,
            "limit": 10,
            "offset": offset * 10,
        }.items()
        if value is not None
    }

    response = client.get_request_list(
        resource_name="contracts",
        params=params,
    )

    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response[0]), content=None
        )

    contracts = []
    for contract in response:
        contracts.append(
            CoupaContract.from_fields(
                contract_id=contract.get("id", 0),
                name=contract.get("name", ""),
                no_of_renewals=contract.get("no-of-renewals", 0),
                number=contract.get("number", ""),
                reason_insight_events=contract.get("reason-insight-events", []),
                renewal_length_unit=contract.get("renewal-length-unit", ""),
                renewal_length_value=contract.get("renewal-length-value", 0),
                status=contract.get("status", ""),
                start_date=contract.get("start-date", ""),
                end_date=contract.get("end-date", ""),
                supplier_name=(contract.get("supplier") or {}).get("name", ""),
                supplier_number=(contract.get("supplier") or {}).get("number", ""),
                supplier_id=(contract.get("supplier") or {}).get("id"),
                supplier_status=(contract.get("supplier") or {}).get("status", ""),
                supplier_contact_email=(contract.get("supplier") or {})
                .get("primary-contact", {})
                .get("email", ""),
                payment_term_id=(contract.get("payment-term") or {}).get("id"),
                payment_term_code=(contract.get("payment-term") or {}).get("code", ""),
                coupa_contract_department_id=(contract.get("department") or {}).get("id"),
                coupa_contract_department_name=(contract.get("department") or {}).get("name", ""),
                coupa_contract_department_status=(contract.get("department") or {}).get(
                    "active", False
                ),
            )
        )
    return ToolResponse(
        success=True, message="The contract data was successfully retrieved", content=contracts
    )
