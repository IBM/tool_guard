from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_outreach.salesloft.dataclasses import StepResponse
from agent_ready_tools.tools.sales.sales_outreach.salesloft.list_step import salesloft_list_step


def test_list_step_with_id() -> None:
    """Test list_cadence tool returns correct result for a given ID."""

    # add the data as a list
    mock_response = {
        "data": [
            {
                "id": 10668444,
                "name": "Linkedin research discovery",
                "display_name": "Day 3 - Step 4 - Phone",
                "created_at": "2023-06-05T08:08:03.288160-04:00",
                "updated_at": "2024-05-04T03:07:03.288160-04:00",
                "type": "phone",
                "day": 3,
                "step_number": 4,
            },
            {
                "id": 10668445,
                "name": "Email outreach",
                "display_name": "Day 4 - Step 1 - Email",
                "created_at": "2023-06-06T09:15:03.288160-04:00",
                "updated_at": "2024-05-05T04:12:03.288160-04:00",
                "type": "email",
                "day": 4,
                "step_number": 1,
            },
        ]
    }

    with patch(
        "agent_ready_tools.tools.sales.sales_outreach.salesloft.list_step.get_salesloft_client"
    ) as mock_get_client:
        mock_client_instance = MagicMock()
        mock_client_instance.get_request.return_value = mock_response
        mock_get_client.return_value = mock_client_instance

        result = salesloft_list_step(step_id=10668444)

        # assertion for the first item in the list
        assert isinstance(result[0], StepResponse)
        assert result[0].id == 10668444
        assert result[0].name == "Linkedin research discovery"
        assert result[0].display_name == "Day 3 - Step 4 - Phone"
        assert result[0].created_at == "06/05/2023 08:08am"
        assert result[0].updated_at == "05/04/2024 03:07am"
        assert result[0].type == "phone"
        assert result[0].day == 3
        assert result[0].step_number == 4

        # assertion for the second item in the list
        assert result[1].id == 10668445
        assert result[1].name == "Email outreach"
        assert result[1].display_name == "Day 4 - Step 1 - Email"

        mock_client_instance.get_request.assert_called_once_with(
            version="v2", endpoint="steps", path_parameter=10668444
        )
