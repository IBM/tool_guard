from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.get_all_individuals import get_all_individuals
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Individual


def test_get_all_individuals() -> None:
    """Test that the `get_all_individuals` function returns the expected response."""
    test_data = [
        Individual(id="001Ind000002ABCDE", name="John Doe", owner_id="005User00001FGHIJ"),
        Individual(id="001Ind000002KLMNO", name="Jane Smith", owner_id="005User00001PQRST"),
    ]

    expected: list[Individual] = test_data
    with patch(
        "agent_ready_tools.tools.IT.salesforce.get_all_individuals.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {"Id": test_data[0].id, "Name": test_data[0].name, "OwnerId": test_data[0].owner_id},
            {"Id": test_data[1].id, "Name": test_data[1].name, "OwnerId": test_data[1].owner_id},
        ]

        response = get_all_individuals("LastModifiedDate > 2023-01-01")

        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Name, OwnerId FROM Individual WHERE LastModifiedDate > 2023-01-01"
        )
