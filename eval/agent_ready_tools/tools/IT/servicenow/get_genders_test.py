from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_genders import get_genders


def test_get_genders() -> None:
    """Tests that the `get_genders` function returns the expected response."""

    # Define test data:
    test_data = {
        "gender_1": "Male",
        "gender_2": "Female",
        "gender_3": "Not Specified",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_genders.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {"label": test_data["gender_1"]},
                {"label": test_data["gender_2"]},
                {"label": test_data["gender_3"]},
            ],
        }

        # Get genders
        response = get_genders(gender_label="")

        # Ensure that get_genders() executed and returned proper values
        assert response
        assert len(response.gender)
        assert response.gender[0].gender_label == test_data["gender_1"]
        assert response.gender[1].gender_label == test_data["gender_2"]
        assert response.gender[2].gender_label == test_data["gender_3"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "sys_user", "element": "gender"}
        )
