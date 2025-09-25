from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.get_supplier_by_id import (
    coupa_get_supplier_by_id,
)


def test_coupa_get_supplier_by_id() -> None:
    """Test get supplier by id."""
    test_supplier = {
        "id": 1234,
        "number": "5678",
        "status": "active",
        "name": "test-supplier",
        "primary-contact": {"email": "test-supplier@gmail.com"},
        "supplier-addresses": [
            {
                "id": "4",
                "name": "Amazon.com",
                "street1": "1516 2nd Ave",
                "street2": "Cotton County",
                "city": "Seattle",
                "state": "WA",
                "country": {"name": "United States"},
                "postal_code": "98112",
                "purposes": [{"name": "warehouse"}],
            }
        ],
        "contacts": [
            {
                "id": "200069",
                "email": "agent1@test.com",
                "reference-code": "10",
                "name-given": "Agent",
                "name-family": "Agent-Test",
            },
            {
                "id": "200070",
                "email": "agent2@test.com",
                "reference-code": "20",
                "name-given": "Agent2",
                "name-family": "Agent-Test2",
            },
        ],
        "purposes": [
            {
                "id": 7,
                "created-at": "2018-09-09T17:00:00-07:00",
                "updated-at": "2018-09-09T17:00:00-07:00",
                "kind": "Contact",
                "name": "other_contact",
            },
            {
                "id": 6,
                "created-at": "2018-09-09T17:00:00-07:00",
                "updated-at": "2018-09-09T17:00:00-07:00",
                "kind": "Contact",
                "name": "executive_contact",
            },
        ],
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.get_supplier_by_id.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = test_supplier

        response = coupa_get_supplier_by_id(supplier_id=test_supplier["id"]).content

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name=f"suppliers/{test_supplier['id']}",
            params={
                "fields": '["id","number","status","name",{"primary_contact":["email"]},{"contacts":["id","email","name_given","name_family","reference_code"]},{"supplier_addresses":["id","name","street1","street2","city","state","postal-code",{"country":["name"]},{"purposes":["name"]}]}]'
            },
        )
