from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.finance.ibm_planning_analytics.get_dimensions_of_cube import (
    get_dimensions_of_cube,
)


@patch(
    "agent_ready_tools.tools.finance.ibm_planning_analytics.get_dimensions_of_cube.get_ibm_pa_client"
)
def test_ibm_pa_get_dimensions_of_cube(mock_pa_client: MagicMock) -> None:
    """Verifies the get_dimensions_of_cube tool in IBM PA."""

    # define test data
    test_data = {
        "value": [
            {
                "@odata.etag": 'W/"3f7087f6a92c13fc3e6059fd661a3172453a9e52"',
                "Name": "Sandboxes",
            },
            {
                "@odata.etag": 'W/"99e7d7e127483d3af20a22b8bbed09a1d5172667"',
                "Name": "organization",
            },
            {
                "@odata.etag": 'W/"3e34d1d4dcf5a44ee9addf7033711f8af5ac8f82"',
                "Name": "Year",
            },
        ]
    }
    # Create a mock client instance
    mock_client = MagicMock()
    mock_get_response = MagicMock()
    mock_pa_client.return_value = mock_client
    mock_client.get_request.return_value = mock_get_response
    mock_get_response.status_code = 200
    mock_get_response.raise_for_status = MagicMock()
    mock_get_response.json.return_value = test_data
    expected_dimensions = set(["organization", "Year"])
    dimensions: List[str] = get_dimensions_of_cube(cube_name="Item Allocations")
    assert set(dimensions) == expected_dimensions
