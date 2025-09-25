from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DeleteContractResponse:
    """Represents the result of a contract delete operation in Salesforce."""

    http_code: int


@tool(expected_credentials=SALESFORCE_CONNECTIONS)
def delete_contract(contract_id: str) -> DeleteContractResponse:
    """
    Deletes a contract from Salesforce.

    Args:
        contract_id: The id of the contract, returned by the tool `get_all_contracts` in Salesforce.

    Returns:
        The result of performing delete operation on a contract.
    """

    client = get_salesforce_client()
    try:
        response = client.salesforce_object.Contract.delete(contract_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response
    except SalesforceError as err:
        http_code = err.status

    return DeleteContractResponse(http_code=http_code)
