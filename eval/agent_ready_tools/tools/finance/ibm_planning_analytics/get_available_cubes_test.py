from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.finance.ibm_planning_analytics.get_available_cubes import (
    get_available_cubes,
)


@patch(
    "agent_ready_tools.tools.finance.ibm_planning_analytics.get_available_cubes.get_ibm_pa_client"
)
def test_ibm_pa_get_available_cubes(mock_pa_client: MagicMock) -> None:
    """Verifies the get_available_cubes tool in IBM PA."""

    # define test data
    test_data = {
        "@odata.context": "$metadata#Cubes",
        "value": [
            {
                "@odata.etag": 'W/"41cd5e4770d2b9ad8cdad9870e0330064200e8d0"',
                "Name": "Allocation Calculation",
            },
            {
                "@odata.etag": 'W/"41cd5e4770d2b9ad8cdad9870e0330064200e8d0"',
                "Name": "Allocation Source Definition",
            },
        ],
    }
    # Create a mock client instance
    mock_client = MagicMock()
    mock_get_response = MagicMock()
    mock_pa_client.return_value = mock_client
    mock_client.get_request.return_value = mock_get_response
    mock_get_response.status_code = 200
    mock_get_response.raise_for_status = MagicMock()
    mock_get_response.json.return_value = test_data
    expected_cube_names = set(["Allocation Calculation", "Allocation Source Definition"])
    cube_names = get_available_cubes()
    assert set(cube_names) == expected_cube_names
