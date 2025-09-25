from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    ErrorResponse,
    Opportunity,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_opportunity(
    account_id: str,
    name: str,
    amount: float,
    close_date: str,
    stage_name: str,
    description: Optional[str] = None,
    opportunity_type: Optional[str] = None,
    lead_source: Optional[str] = None,
) -> Opportunity | ErrorResponse:
    """
    Creates a new opportunity in Salesforce.

    Args:
        account_id: Unique Salesforce Account ID the Opportunity is associated with.
        name: Name of the Opportunity.
        amount: Expected revenue if the Opportunity is won.
        close_date: Expected or actual close date of the Opportunity.
        stage_name: The stage of the opportunity.
        description: Contextual background or notes about the Opportunity.
        opportunity_type: Opportunity type (e.g., "New Business", "Renewal").
        lead_source: Source of the Opportunity (e.g., "Web", "Referral").

    Returns:
        The created opportunity object.
    """
    client = get_salesforce_client()

    data = {
        "AccountId": account_id,
        "Name": name,
        "Amount": amount,
        "CloseDate": close_date,
        "StageName": stage_name,
        "Description": description,
        "Type": opportunity_type,
        "LeadSource": lead_source,
    }
    try:
        o = client.salesforce_object.Opportunity.create(data)  # type: ignore[operator]

        return Opportunity(
            id=o.get("id"),
            account_id=account_id,
            amount=amount,
            age_in_days=None,
            name=name,
            close_date=close_date,
            stage_name=stage_name,
            description=description,
            opportunity_type=opportunity_type,
            lead_source=lead_source,
            probability=0,
        )
    except SalesforceError as e:
        if e.content and len(e.content) > 0:
            first_error = e.content[0]
            assert isinstance(first_error, dict)
            error_code = first_error.get("errorCode")
            if error_code == "MALFORMED_ID":
                custom_message = "The ID provided for account_id is not valid. Please check the ID and try again."
                return ErrorResponse(
                    message=custom_message, status_code=e.status, payload={account_id}
                )

        return ErrorResponse(
            message=f"{str(e)}",
            status_code=e.status,
            payload={"raw_error_details": e.content},
        )
