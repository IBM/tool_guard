from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateIndividualResponse:
    """Represents the result of creating an individual in Salesforce."""

    individual_id: str


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def create_individual(
    last_name: str,
    first_name: Optional[str] = None,
    birth_date: Optional[str] = None,
    occupation: Optional[str] = None,
) -> CreateIndividualResponse:
    """
    Creates an individual in Salesforce.

    Args:
        last_name: The last name of the individual in Salesforce.
        first_name: The first name of the individual in Salesforce.
        birth_date: The birth date of the individual should be given in ISO 8601 format (e.g., YYYY-
            MM-DD) in Salesforce.
        occupation: The occupation of the individual in Salesforce.

    Returns:
        The result of performing the creation of an individual in Salesforce.
    """

    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "LastName": last_name,
        "FirstName": first_name,
        "BirthDate": birth_date,
        "Occupation": occupation,
    }

    response = client.salesforce_object.Individual.create(data=payload)  # type: ignore[operator]
    return CreateIndividualResponse(individual_id=response.get("id"))
