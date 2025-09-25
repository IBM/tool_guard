from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.ariba_soap_client import AribaSOAPClient
from agent_ready_tools.tools.procurement.purchase_support.sap_ariba.create_purchase_requisition import (
    ariba_create_requisition,
)

# Preparing sample test data
test_data = {
    "partition": "prealm_3841",
    "variant": "vrealm_3841",
    "OriginatingSystem": "API-test",
    "OriginatingSystemReferenceID": "643260a2-0ad0-4db3-adb4-8fb65b40353a",
    "StatusString": "Submitted",
    "UniqueName": "PR331",
    "description": "test description 112",
}


@patch(
    "agent_ready_tools.tools.procurement.purchase_support.sap_ariba.create_purchase_requisition.get_ariba_soap_client"
)
@patch.object(AribaSOAPClient, "create_purchase_requisition")
def test_ariba_create_requisition(
    mock_create_requisition: MagicMock,
    mock_ariba_soap_client: MagicMock,
) -> None:
    """Creates a test response and assert it with mocked response."""

    mock_client = AribaSOAPClient(
        base_url="abc.xyz",
        realm="test_realm",
        username="user",
        password="pass",
        requester_password="requester",
    )

    resp_data = {
        "requisition_import_pull_reply": {
            "partition": "prealm_3841",
            "variant": "vrealm_3841",
            "requisition_items": {
                "item": {
                    "originating_system": "API-test",
                    "originating_system_reference_id": "643260a2-0ad0-4db3-adb4-8fb65b40353a",
                    "status_string": "Submitted",
                    "unique_name": "PR331",
                }
            },
        }
    }
    # Configure return values
    mock_create_requisition.return_value = resp_data

    # mock the client
    mock_ariba_soap_client.return_value = mock_client

    # now invoke the test and assert
    response = ariba_create_requisition(
        description=test_data["description"],
        currency="USD",
        imported_deliver_to_staging=3000,
        item_name="Purchase Requisition for ITEM 007",
        originating_system="API-test",
        unique_name_val=4545,
        quantity=2,
        price=10.5,
        requester_uniq_name="puser1",
        need_by_date="2025-06-24",
    )

    assert response.partition == test_data["partition"]
    assert response.variant == test_data["variant"]
    assert response.variant != "vrealm_3841-invalid"

    if response.requisition_items and response.requisition_items.item:
        assert response.requisition_items.item.originating_system == test_data["OriginatingSystem"]
        assert response.requisition_items.item.unique_name == test_data["UniqueName"]
        assert response.requisition_items.item.status_string == test_data["StatusString"]
