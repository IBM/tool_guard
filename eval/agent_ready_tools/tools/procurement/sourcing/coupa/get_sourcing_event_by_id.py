from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.sourcing.coupa.common_classes_sourcing import (
    CoupaCommodity,
    CoupaCurrency,
    CoupaQuoteRequestLines,
    CoupaQuoteRequests,
    CoupaQuoteSupplier,
    CoupaUser,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_sourcing_event_by_id(
    quote_request_id: int, event_type: str = "rfp"
) -> ToolResponse[CoupaQuoteRequests]:
    """
    Fetch a Quote Request by ID from Coupa API and validate its event type.

    Args:
        quote_request_id: id of quote requests
        event_type: event type for sourcing

    Returns:
        CoupaQuoteRequests
    """

    params = {
        "event-type": event_type  # Pass event_type as query parameter (even if server may or may not use it)
    }

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(resource_name=f"quote_requests/{quote_request_id}", params=params)

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    raw_currency = response.get("currency", {})
    currency = CoupaCurrency(code=raw_currency.get("code")) if raw_currency else None

    raw_commodity = response.get("commodity", {})
    commodity = (
        CoupaCommodity(id=raw_commodity.get("id"), name=raw_commodity.get("name"))
        if raw_commodity
        else None
    )

    raw_suppliers = response.get("quote-suppliers", [])
    suppliers = (
        [
            CoupaQuoteSupplier(id=s.get("id"), name=s.get("name"), email=s.get("email"))
            for s in raw_suppliers
        ]
        if raw_suppliers
        else []
    )
    created_user = response.get("created-by", {})
    updated_user = response.get("updated-by", {})
    created_by = (
        CoupaUser(
            id=created_user.get("id"),
            fullname=created_user.get("fullname"),
            email=created_user.get("email"),
        )
        if created_user
        else None
    )
    updated_by = (
        CoupaUser(
            id=updated_user.get("id"),
            fullname=updated_user.get("fullname"),
            email=updated_user.get("email"),
        )
        if updated_user
        else None
    )
    raw_lines = response.get("lines", [])
    lines: List[CoupaQuoteRequestLines] = []
    for line in raw_lines:
        price_currency = line.get("price-currency", {})
        line_currency = CoupaCurrency(code=price_currency.get("code")) if price_currency else None
        l_commodity = line.get("commodity", {})
        line_commodity = (
            CoupaCommodity(id=l_commodity.get("id"), name=l_commodity.get("name"))
            if l_commodity
            else None
        )

        lines.append(
            CoupaQuoteRequestLines(
                line_id=line.get("id"),
                quantity=line.get("quantity"),
                need_by_date=line.get("need-by-date"),
                created_at=line.get("created-at"),
                updated_at=line.get("updated-at"),
                price_amount=line.get("price-amount"),
                description=line.get("description"),
                type=line.get("type"),
                price_currency=line_currency,
                commodity=line_commodity,
            )
        )

    return ToolResponse(
        success=True,
        message="The sourcing event was retrieved by the provided ID",
        content=CoupaQuoteRequests(
            id=response.get("id", 0),
            event_type=response.get("event-type", ""),
            description=response.get("description", ""),
            state=response.get("state", ""),
            start_time=response.get("start-time", ""),
            end_time=response.get("end-time", ""),
            submit_time=response.get("submit-time", ""),
            quote_message=response.get("quote-message", ""),
            currency=currency,
            created_by=created_by,
            updated_by=updated_by,
            quote_suppliers=suppliers,
            commodity=commodity,
            lines=lines,
        ),
    )
