from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.finance.ibm_planning_analytics.create_sandbox import create_sandbox


@patch("agent_ready_tools.tools.finance.ibm_planning_analytics.create_sandbox.get_ibm_pa_client")
def test_ibm_pa_create_sandbox(mock_pa_client: MagicMock) -> None:
    """Verifies the create_sandbox tool in IBM PA."""

    # define test data
    test_data = {
        "status_code": 201,
        "Name": "domains-test",
        "IncludeInSandboxDimension": True,
    }
    # Create a mock client instance
    mock_client = MagicMock()
    mock_pa_client.return_value = mock_client
    mock_client.post_request.return_value = test_data

    sandbox_created = create_sandbox(sandbox_name="domains-test")
    assert sandbox_created
