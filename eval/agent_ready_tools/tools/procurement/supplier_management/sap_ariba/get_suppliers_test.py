from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_ariba.get_suppliers import (
    RegistrationStatus,
    ariba_get_suppliers,
)


def test_ariba_get_suppliers() -> None:
    """Test that the `get_suppliers` function returns the expected response."""

    # Define test data:
    test_data = {
        "supplier_name": "Schafer Office (Print)",
        "sm_vendor_id": "S20042550",
        "erp_vendor_id": "1000000001",
        "registration_status": "Invited",
        "supplier_an_id": "",
        "qualification_status": "NotQualified",
        "address_line1": "14235 Maximo Avenue",
        "city": "Dallas",
        "postal_code": "75244",
        "country_code": "US",
        "limit": 20,
        "skip": 0,
    }

    # Patch `get_ariba_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_ariba.get_suppliers.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.post_request_list.return_value = [
            {
                "Supplier Name": test_data["supplier_name"],
                "SM Vendor ID": test_data["sm_vendor_id"],
                "ERP Vendor ID": test_data["erp_vendor_id"],
                "Registration Status": test_data["registration_status"],
                "Qualification Status": test_data["qualification_status"],
                "Address - Line1": test_data["address_line1"],
                "An Id": test_data["supplier_an_id"],
                "Address - City": test_data["city"],
                "Address - Postal Code": test_data["postal_code"],
                "Address - Country Code": test_data["country_code"],
            }
        ]

        response = ariba_get_suppliers().content.suppliers

        assert response
        assert response[0].supplier_name == test_data["supplier_name"]
        assert response[0].sm_vendor_id == test_data["sm_vendor_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request_list.assert_called_once_with(
            endpoint="supplierdatapagination/v4/prod/vendorDataRequests",
            payload={"outputFormat": "JSON"},
            params={"$top": test_data["limit"], "$skip": test_data["skip"]},
        )


def test_ariba_get_suppliers_with_id() -> None:
    """
    Test that the `get_suppliers` function returns the expected response.

    Tests the response when filtering with one supplier's sm vendor id.
    """

    test_data = {
        "supplier_name": "Syntech Incorporated (Email)",
        "sm_vendor_id": "S20043642",
        "erp_vendor_id": "1000003745",
        "supplier_an_id": "",
        "registration_status": "NotInvited",
        "qualification_status": "Unknown",
        "address_line1": "",
        "city": "",
        "postal_code": "",
        "country_code": "",
        "limit": 20,
        "skip": 0,
    }

    test_response = [
        {
            "Supplier Name": test_data["supplier_name"],
            "SM Vendor ID": test_data["sm_vendor_id"],
            "ERP Vendor ID": test_data["erp_vendor_id"],
            "An Id": test_data["supplier_an_id"],
            "Registration Status": test_data["registration_status"],
            "Qualification Status": test_data["qualification_status"],
            "Address - Line1": test_data["address_line1"],
            "Address - City": test_data["city"],
            "Address - Postal Code": test_data["postal_code"],
            "Address - Country Code": test_data["country_code"],
        }
    ]

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_ariba.get_suppliers.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.post_request_list.return_value = test_response

        response = ariba_get_suppliers(sm_vendor_id=test_data["sm_vendor_id"]).content.suppliers

        assert response
        assert response[0].supplier_name == test_data["supplier_name"]
        assert response[0].sm_vendor_id == test_data["sm_vendor_id"]
        assert response[0].address_line1 == test_data["address_line1"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request_list.assert_called_once_with(
            endpoint="supplierdatapagination/v4/prod/vendorDataRequests",
            payload={
                "outputFormat": "JSON",
                "smVendorIds": ["S20043642"],
            },
            params={"$top": test_data["limit"], "$skip": test_data["skip"]},
        )


def test_ariba_get_suppliers_with_status() -> None:
    """
    Test that the `get_suppliers` function returns the expected response.

    Tests the response when filtering with supplier's registration status.
    """

    # Define test data:
    test_data = {
        "supplier_name": "Schafer Office (Print)",
        "sm_vendor_id": "S20042550",
        "erp_vendor_id": "1000000001",
        "supplier_an_id": "",
        "registration_status": "Invited",
        "qualification_status": "NotQualified",
        "address_line1": "14235 Maximo Avenue",
        "city": "Dallas",
        "postal_code": "75244",
        "country_code": "US",
        "limit": 20,
        "skip": 0,
    }

    # Patch `get_ariba_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_ariba.get_suppliers.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.post_request_list.return_value = [
            {
                "Supplier Name": test_data["supplier_name"],
                "SM Vendor ID": test_data["sm_vendor_id"],
                "ERP Vendor ID": test_data["erp_vendor_id"],
                "An Id": test_data["supplier_an_id"],
                "Registration Status": test_data["registration_status"],
                "Qualification Status": test_data["qualification_status"],
                "Address - Line1": test_data["address_line1"],
                "Address - City": test_data["city"],
                "Address - Postal Code": test_data["postal_code"],
                "Address - Country Code": test_data["country_code"],
            }
        ]

        response = ariba_get_suppliers(
            registration_status=RegistrationStatus.INVITED
        ).content.suppliers

        assert response
        assert response[0].supplier_name == test_data["supplier_name"]
        assert response[0].sm_vendor_id == test_data["sm_vendor_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request_list.assert_called_once_with(
            endpoint="supplierdatapagination/v4/prod/vendorDataRequests",
            payload={"outputFormat": "JSON", "registrationStatusList": ["Invited"]},
            params={"$top": test_data["limit"], "$skip": test_data["skip"]},
        )
