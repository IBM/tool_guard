from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_contract(
    contract_id: str,
    status: Optional[str] = None,
    account_id: Optional[str] = None,
    start_date: Optional[str] = None,
    contract_term: Optional[int] = None,
    owner_expiration_notice: Optional[str] = None,
    pricebook2_id: Optional[str] = None,
    billing_street: Optional[str] = None,
    billing_city: Optional[str] = None,
    billing_state_code: Optional[str] = None,
    billing_postal_code: Optional[str] = None,
    billing_country_code: Optional[str] = None,
    description: Optional[str] = None,
    owner_id: Optional[str] = None,
) -> int:
    """
    Update a contract in Salesforce. Confirm your parameters with the user before creating the
    contract.

    Args:
        contract_id: The contract unique identifier in Salesforce.
        status: The contract status, returned by the tool `get_contract_status` in Salesforce.
        account_id: The account id, returned by the tool `list_accounts` in Salesforce.
        start_date: The start date of the contract in Salesforce.
        contract_term: Number of months that the contract is valid in Salesforce.
        owner_expiration_notice: Number of days ahead of the contract end date (15, 30, 45, 60, 90,
            and 120). Used to notify the owner in advance that the contract is ending, returned by
            the tool `get_contract_owner_expiration_notice` in Salesforce.
        pricebook2_id: The price book, returned by the tool `list_pricebooks` in Salesforce, with
            the IsActive = true search criteria.
        billing_street: Street address for the billing address.
        billing_city: Details for the billing address. The maximum size is 40 characters.
        billing_state_code: The ISO state code for the contract's billing address.
        billing_postal_code: Details for the billing address of this account. The maximum size is 20
            characters.
        billing_country_code: The ISO country code for the contract's billing address.
        description: Description of the contract.
        owner_id: The order owner, returned by the tool `list_users`, with the IsActive = true
            search criteria. in Salesforce.

    Returns:
        The status of the update operation performed on the contract.
    """
    client = get_salesforce_client()

    data = {}

    if account_id is not None:
        data["AccountId"] = account_id
    if contract_term is not None:
        data["ContractTerm"] = contract_term  # type: ignore
    if start_date is not None:
        data["StartDate"] = start_date
    if status is not None:
        data["Status"] = status
    if owner_expiration_notice is not None:
        data["OwnerExpirationNotice"] = owner_expiration_notice
    if billing_street is not None:
        data["BillingStreet"] = billing_street
    if billing_city is not None:
        data["BillingCity"] = billing_city
    if billing_state_code is not None:
        data["BillingStateCode"] = billing_state_code
    if billing_postal_code is not None:
        data["BillingPostalCode"] = billing_postal_code
    if billing_country_code is not None:
        data["BillingCountryCode"] = billing_country_code
    if description is not None:
        data["Description"] = description
    if owner_id is not None:
        data["OwnerId"] = owner_id
    if pricebook2_id is not None:
        data["Pricebook2Id"] = pricebook2_id

    response = client.salesforce_object.Contract.update(contract_id, data)  # type: ignore[operator]
    return response
