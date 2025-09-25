from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Lead
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_lead(
    first_name: str,
    last_name: str,
    email: str,
    company: str,
    description: str,
    title: Optional[str] = None,
    industry: Optional[str] = None,
    annual_revenue: Optional[float] = None,
    number_of_employees: Optional[float] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    zip_code: Optional[str] = None,
    rating: Optional[str] = None,
    status: Optional[str] = None,
) -> Lead:
    """
    Creates a new lead in Salesforce.

    Args:
        first_name: The first name of the lead.
        last_name: The last name of the lead.
        email: The email of the lead.
        company: The company of the lead.
        description: The description of the lead.
        title: The title of the lead.
        industry: The industry of the lead.
        annual_revenue: The annual revenue associated with the lead.
        number_of_employees: Number of employees at the lead's company.
        city: The city where the lead is located.
        state: The state where the lead is located.
        country: The country where the lead is located.
        zip_code: The zip code where the lead is located.
        rating: The rating of the lead.
        status: The status of the lead.

    Returns:
        The created lead object.
    """
    client = get_salesforce_client()

    data = {
        "FirstName": first_name,
        "LastName": last_name,
        "Email": email,
        "Company": company,
        "Description": description,
        "Title": title,
        "Industry": industry,
        "AnnualRevenue": annual_revenue,
        "NumberOfEmployees": number_of_employees,
        "City": city,
        "State": state,
        "Country": country,
        "PostalCode": zip_code,
        "Rating": rating,
        "Status": status,
    }
    lead_obj = client.salesforce_object.Lead.create(data)  # type: ignore[operator]

    lead = {
        "id": lead_obj.get("id"),
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "company": company,
        "description": description,
        "title": title,
        "industry": industry,
        "annual_revenue": annual_revenue,
        "number_of_employees": number_of_employees,
        "city": city,
        "state": state,
        "country": country,
        "zip_code": zip_code,
        "rating": rating,
        "status": status,
    }

    return Lead(**lead)
