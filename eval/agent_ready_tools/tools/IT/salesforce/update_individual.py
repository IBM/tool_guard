from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_individual(
    individual_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    occupation: Optional[str] = None,
    birth_date: Optional[str] = None,
    owner_id: Optional[str] = None,
    website: Optional[str] = None,
) -> int:
    """
    Updates an individual record in Salesforce.

    Args:
        individual_id: The unique identifier of an individual in Salesforce.
        first_name: The first name of an individual in Salesforce.
        last_name: The last name of an individual in Salesforce.
        occupation: The occupation of an individual in Salesforce.
        birth_date: The date of birth of an individual in Salesforce, in ISO 8601 format (eg., YYYY-
            MM-DD)
        owner_id: The id of the owner of the account associated with this individual, returned by
            the tool `list_users`.
        website: The URL of the individual's website.

    Returns:
        The result of performing an update operation.
    """

    client = get_salesforce_client()

    data = {
        "FirstName": first_name,
        "LastName": last_name,
        "Occupation": occupation,
        "BirthDate": birth_date,
        "OwnerId": owner_id,
        "Website": website,
    }

    # Filter out the parameters that are None/Blank.
    data = {key: value for key, value in data.items() if value}

    status_code = client.salesforce_object.Individual.update(individual_id, data)  # type: ignore[operator]

    return status_code
