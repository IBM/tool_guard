from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_outreach.salesloft.list_cadence import (
    CadenceResponse,
    salesloft_list_cadence,
)


def test_list_cadence_with_id() -> None:
    """Test list_cadence tool returns correct result for a given ID."""

    mock_response = {
        "data": {
            "id": 1417731,
            "name": "Example@2",
            "created_at": "2023-06-05T08:08:03.288160-04:00",
            "updated_at": "2024-05-04T03:07:03.288160-04:00",
            "current_state": "active",
            "cadence_priority": None,
            "cadence_people": None,
        }
    }

    with patch(
        "agent_ready_tools.tools.sales.sales_outreach.salesloft.list_cadence.get_salesloft_client"
    ) as mock_get_client:
        mock_client_instance = MagicMock()
        mock_client_instance.get_request.return_value = mock_response
        mock_get_client.return_value = mock_client_instance

        result = salesloft_list_cadence(cadence_id="1417731")

        assert isinstance(result[0], CadenceResponse)
        assert result[0].id == 1417731
        assert result[0].name == "Example@2"
        assert result[0].created_at == "06/05/2023 08:08am"
        assert result[0].updated_at == "05/04/2024 03:07am"
        assert result[0].current_state == "active"
        assert result[0].cadence_priority is None
        assert result[0].cadence_people is None

        mock_client_instance.get_request.assert_called_once_with(
            version="v2", endpoint="cadences", path_parameter="1417731"
        )
