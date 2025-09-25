from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionCurrencyHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_currencies(
    currency: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionCurrencyHeader]]:
    """
    Gets all the currencies from Oracle Fusion.

    Args:
        currency: The name of the currency.
        limit: The maximum number of records returned per page.
        skip: The number of records to skip for pagination.

    Returns:
        A list of currencies.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip}

    if currency:
        params["q"] = f"Name='{currency}'"

    response = client.get_request(resource_name=f"currenciesLOV", params=params)

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No currencies returned.")

    currencies = []

    for currency_header in response["items"]:
        currencies.append(
            OracleFusionCurrencyHeader(
                currency=currency_header.get("Name", ""),
                currency_code=currency_header.get("CurrencyCode", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved the currencies from Oracle Fusion successfully.",
        content=currencies,
    )
