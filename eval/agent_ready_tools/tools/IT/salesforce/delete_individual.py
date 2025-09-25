from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DeleteIndividualResponse:
    """Represents the result of delete an individual operation in Salesforce."""

    http_code: int


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def delete_individual(
    individual_id: str,
) -> DeleteIndividualResponse:
    """
    Delete an individual in Salesforce.

    Args:
        individual_id: The id of the individual, returned by the `get_all_individuals` tool.

    Returns:
        The status of the delete operation.
    """
    client = get_salesforce_client()

    http_code = None

    try:
        response = client.salesforce_object.Individual.delete(individual_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response
    except SalesforceError as err:
        http_code = err.status

    return DeleteIndividualResponse(http_code)
