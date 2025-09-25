from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaDisputedInvoiceIdList:
    """
    Dataclass to hold a list of disputed invoice IDs.

    Attributes:
        disputed_invoice_ids (List[int]): A list of integer IDs representing Coupa invoice IDs.
    """

    disputed_invoice_ids: List[int]


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_disputed_invoice_id_list() -> CoupaDisputedInvoiceIdList:
    """
    Returns a list of disputed invoice IDs from Coupa.

    Returns:
        DisputedInvoiceIdList containing list of disputed invoice IDs.

    Raises:
        ValueError: If the API response is not a valid JSON or does not match the expected data
            structure.
    """
    client = get_coupa_client()
    response = client.get_request(resource_name='invoices?status=Disputed&fields=["id"]')

    disputed_invoice_ids: List[int] = []
    for item in response:
        if isinstance(item, dict) and "id" in item:
            disputed_invoice_ids.append(int(item["id"]))
        else:
            raise ValueError(
                f"Unexpected item format in Coupa API response. Expected a dictionary with 'id' key, got: {item}\nFull response: {response}"
            )

    return CoupaDisputedInvoiceIdList(disputed_invoice_ids=disputed_invoice_ids)
