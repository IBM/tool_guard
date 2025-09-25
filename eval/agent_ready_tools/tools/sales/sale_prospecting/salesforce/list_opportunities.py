from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import SalesforceError, format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    ErrorResponse,
    Opportunity,
)
from agent_ready_tools.utils.sql_utils import format_select_clause_list, format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS

FALLBACK_FIELDS = [
    "Id",
    "AccountId",
    "Name",
    "Amount",
    "CloseDate",
    "StageName",
    "Description",
    "Type",
    "LeadSource",
    "Probability",
    "AgeInDays",
]


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_opportunities(
    default_fields: str = "",
    optional_fields: str = "",
    use_optional_fields: bool = False,
    search: Optional[str] = None,
) -> list[Opportunity] | ErrorResponse:
    """
    Search for opportunities in Salesforce using a search query with optional filters.

    Optional filters: ID, account ID, name, amount, probability, close date, stage, description,
    lead source, type, age.

    Args:
        default_fields: Default fields to query.
        optional_fields: Set of optional fields to query on request.
        use_optional_fields: A flag to use the optional fields in the query.
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Opportunity objects.
    """
    client = get_salesforce_client()

    select_fields_list = []

    if default_fields:
        select_fields_list.extend(default_fields.split(","))
    else:
        select_fields_list.extend(FALLBACK_FIELDS)

    if use_optional_fields:
        select_fields_list.extend(optional_fields.split(","))

    all_fields = format_select_clause_list(select_fields_list)
    cleaned_select_clause = ", ".join(all_fields)
    cleaned_where_clause = format_where_input_string(search or "")
    try:
        results: list[Opportunity] = []

        rs = client.salesforce_object.query_all_iter(
            format_soql(f"SELECT {cleaned_select_clause} FROM Opportunity {cleaned_where_clause}")
        )

        for obj in rs:
            additional_data = {
                key: value
                for key, value in obj.items()
                if key not in [*FALLBACK_FIELDS, "attributes"]
            }
            results.append(
                Opportunity(
                    id=obj.get("Id"),
                    account_id=obj.get("AccountId"),
                    name=obj.get("Name"),
                    amount=obj.get("Amount"),
                    probability=obj.get("Probability"),
                    close_date=obj.get("CloseDate"),
                    stage_name=obj.get("StageName"),
                    description=obj.get("Description", ""),
                    lead_source=obj.get("LeadSource", ""),
                    opportunity_type=obj.get("Type", ""),
                    age_in_days=obj.get("AgeInDays"),
                    additional_data=additional_data if additional_data else None,
                )
            )

        return results
    except SalesforceError as err:
        return ErrorResponse(
            message=str(err),
            payload={search},
            status_code=err.status,
        )
