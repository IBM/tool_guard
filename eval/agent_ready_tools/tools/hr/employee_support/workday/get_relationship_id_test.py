from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_relationship_id import (
    _get_relationship_id_payload,
    get_relationship_id,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_relationship_id() -> None:
    """Test that the `get_relationship_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "relation": "Parent",
        "id": "262f8cd97d424539b1f7d30b9221788a",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_relationship_id.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_related_person_relationships.return_value = Obj(
            {
                "body": {
                    "get_related_person_relationships_response": {
                        "response_data": {
                            "related_person_relationship": [
                                Obj(
                                    {
                                        "related_person_relationship_reference": {
                                            "id": [Obj({"value": test_data["id"]})]
                                        },
                                        "related_person_relationship_data": [
                                            Obj({"relationship_name": test_data["relation"]})
                                        ],
                                    }
                                )
                            ]
                        }
                    },
                },
            }
        )

        # Get Employee passport and visa
        response = get_relationship_id(relation=test_data["relation"])

        # Ensure that get_relationship_id() executed and returned proper values
        assert response == test_data["id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_related_person_relationships.assert_called_once_with(
            _get_relationship_id_payload()
        )
