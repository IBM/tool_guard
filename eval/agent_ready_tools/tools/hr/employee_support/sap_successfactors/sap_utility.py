from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client


def user_exists(user_id: str) -> bool:
    """
    Checks if a user exists in SAP SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.

    Returns:
        True if the user exists, False otherwise.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(entity="User", filter_expr=f"userId eq '{user_id}'")
    results = response.get("d", {}).get("results", [])

    return bool(results)
