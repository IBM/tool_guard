from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.finance.ibm_planning_analytics.delete_sandbox import delete_sandbox


@patch("agent_ready_tools.tools.finance.ibm_planning_analytics.delete_sandbox.get_ibm_pa_client")
def test_ibm_pa_delete_sandbox(mock_pa_client: MagicMock) -> None:
    """Verifies the delete_sandbox tool in IBM PA."""

    # define test data
    test_data = {
        "status_code": 204,
        "Name": "domains-test-delete",
        "IncludeInSandboxDimension": True,
    }
    # Create a mock client instance
    mock_client = MagicMock()
    mock_pa_client.return_value = mock_client
    mock_client.delete_request.return_value = test_data["status_code"]

    sandbox_deleted = delete_sandbox(sandbox_name="domains-test")
    assert sandbox_deleted
