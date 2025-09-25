from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.finance.ibm_planning_analytics.get_sandbox_by_name import (
    get_sandbox_by_name,
)


@patch(
    "agent_ready_tools.tools.finance.ibm_planning_analytics.get_sandbox_by_name.get_ibm_pa_client"
)
def test_ibm_pa_get_sandbox_by_name(mock_pa_client: MagicMock) -> None:
    """Verifies the get_sandbox_by_name tool in IBM PA."""

    # define test data
    test_data = {
        "Name": "domains-test",
        "IsLoaded": True,
        "IsActive": False,
        "IsQueued": False,
        "IncludeInSandboxDimension": True,
    }
    # Create a mock client instance
    mock_client = MagicMock()
    mock_get_response = MagicMock()
    mock_pa_client.return_value = mock_client
    mock_client.get_request.return_value = mock_get_response
    mock_get_response.status_code = 200
    mock_get_response.raise_for_status = MagicMock()
    mock_get_response.json.return_value = test_data
    mock_get_response.ok.return_value = True

    sandbox_exists = get_sandbox_by_name(sandbox_name="domains-test")
    assert sandbox_exists
