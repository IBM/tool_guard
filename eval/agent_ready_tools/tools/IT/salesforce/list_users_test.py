from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_users import list_users
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import User


def test_list_users() -> None:
    """Tests that the `list_users` function returns the expected response."""

    # Defines test data
    test_data = [
        User(
            user_id="005gL000001aT2vQAE",
            name="OrgFarm EPIC",
            alias="OEPIC",
            email="epic.orgfarm@salesforce.com",
            phone_number=None,
            state=None,
        )
    ]

    expected: List[User] = test_data
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_users.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data[0].user_id,
                "Name": test_data[0].name,
                "Alias": test_data[0].alias,
                "Email": test_data[0].email,
                "Phone": test_data[0].phone_number,
                "State": test_data[0].state,
            }
        ]

        response = list_users(
            "UserType=STANDARD OR IsActive = true OR Email=epic.orgfarm@salesforce.com"
        )

        assert response == expected
