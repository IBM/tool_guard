from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import SalesforceError, format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    ErrorResponse,
    Lead,
)
from agent_ready_tools.utils.sql_utils import format_select_clause_list, format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS

FALLBACK_FIELDS = [
    "Id",
    "FirstName",
    "LastName",
    "Email",
    "Company",
    "Description",
    "Title",
    "Industry",
    "AnnualRevenue",
    "NumberOfEmployees",
    "City",
    "State",
    "Country",
    "PostalCode",
    "Rating",
    "Status",
]


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_leads(
    default_fields: str = "",
    optional_fields: str = "",
    use_optional_fields: bool = False,
    search: Optional[str] = None,
) -> list[Lead] | ErrorResponse:
    """
    Searches for leads in Salesforce with a search querying using optional filters.

    Optional filters: lead ID, name, email, company, description, title, industry, revenue,
    number of employees, rating, status, location.

    Args:
        default_fields: Default fields to query.
        optional_fields: Set of optional fields to query on request.
        use_optional_fields: A flag to use the optional fields in the query.
        search: The SQL where clause from LLM (to clean up).


    Returns:
        A list of Lead objects.
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
        rs = client.salesforce_object.query_all_iter(
            format_soql(f"SELECT {cleaned_select_clause} FROM Lead {cleaned_where_clause}")
        )

        results: list[Lead] = []
        for row in rs:
            additional_data = {
                key: value
                for key, value in row.items()
                if key not in [*FALLBACK_FIELDS, "attributes"]
            }

            lead_id = row.get("Id")
            lead_first_name = row.get("FirstName")
            lead_last_name = row.get("LastName")
            lead_email = row.get("Email")
            lead_company = row.get("Company")
            lead_description = row.get("Description") or ""
            lead_title = row.get("Title")
            lead_industry = row.get("Industry")
            lead_annual_revenue = row.get("AnnualRevenue")
            lead_no_of_employees = row.get("NumberOfEmployees")
            lead_city = row.get("City")
            lead_state = row.get("State")
            lead_country = row.get("Country")
            lead_postal_code = row.get("PostalCode")
            lead_rating = row.get("Rating")
            lead_status = row.get("Status")

            results.append(
                Lead(
                    id=lead_id,
                    first_name=lead_first_name,
                    last_name=lead_last_name,
                    email=lead_email,
                    company=lead_company,
                    description=lead_description,
                    title=lead_title,
                    industry=lead_industry,
                    annual_revenue=lead_annual_revenue,
                    number_of_employees=lead_no_of_employees,
                    city=lead_city,
                    state=lead_state,
                    country=lead_country,
                    zip_code=lead_postal_code,
                    rating=lead_rating,
                    status=lead_status,
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
