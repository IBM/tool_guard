from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    OwnerExpirationNotice,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def get_contract_owner_expiration_notice() -> List[OwnerExpirationNotice]:
    """
    Returns a list of owner expiration notice objects for the contract in the Salesforce org.

    Returns:
        A list of owner expiration notice objects.
    """
    client = get_salesforce_client()

    rs = client.salesforce_object.Contract.describe()  # type: ignore[operator]

    owner_expiration_notice_field = next(
        field for field in rs.get("fields", "") if field.get("name", "") == "OwnerExpirationNotice"
    )
    picklist_values = owner_expiration_notice_field["picklistValues"]

    owner_expiration_notice_list: List[OwnerExpirationNotice] = [
        OwnerExpirationNotice(
            value=entry.get("value", ""),
            label=entry.get("label", ""),
            active=entry.get("active", ""),
        )
        for entry in picklist_values
    ]

    return owner_expiration_notice_list
