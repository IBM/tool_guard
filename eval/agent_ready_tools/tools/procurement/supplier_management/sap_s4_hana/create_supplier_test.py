from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier import (
    sap_s4_hana_create_supplier,
)


def test_sap_s4_hana_create_supplier_person() -> None:
    """
    Test that the `sap_s4_hana_create_supplier` function returns the expected response.

    Tests the response when create supplier is person.
    """

    # Define test data:
    test_data = {
        "supplier_id": "1166",
        "supplier_name": "Schafer Office (Print)",
        "country_code": "US",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {"d": {"BusinessPartner": test_data["supplier_id"]}}

        response = sap_s4_hana_create_supplier(
            supplier_name=test_data["supplier_name"],
            supplier_category="PERSON",
            supplier_country=test_data["country_code"],
        ).content

        assert response
        assert response.supplier_id == test_data["supplier_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_BUSINESS_PARTNER/A_BusinessPartner",
            payload={
                "BusinessPartnerCategory": "1",
                "to_BusinessPartnerRole": [
                    {
                        "BusinessPartnerRole": "FLVN01",
                    }
                ],
                "to_BusinessPartnerAddress": [{"Country": test_data["country_code"]}],
                "LastName": test_data["supplier_name"],
            },
        )


def test_sap_s4_hana_create_supplier_organization() -> None:
    """
    Test that the `sap_s4_hana_create_supplier` function returns the expected response.

    Tests the response when create supplier is organization.
    """

    # Define test data:
    test_data = {
        "supplier_id": "1166",
        "supplier_name": "Schafer Office (Print)",
        "country_code": "US",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {"d": {"BusinessPartner": test_data["supplier_id"]}}

        response = sap_s4_hana_create_supplier(
            supplier_name=test_data["supplier_name"],
            supplier_category="ORGANIZATION",
            supplier_country=test_data["country_code"],
        ).content

        assert response
        assert response.supplier_id == test_data["supplier_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_BUSINESS_PARTNER/A_BusinessPartner",
            payload={
                "BusinessPartnerCategory": "2",
                "to_BusinessPartnerRole": [
                    {
                        "BusinessPartnerRole": "FLVN01",
                    }
                ],
                "to_BusinessPartnerAddress": [{"Country": test_data["country_code"]}],
                "OrganizationBPName1": test_data["supplier_name"],
            },
        )


def test_sap_s4_hana_create_supplier_group() -> None:
    """
    Test that the `sap_s4_hana_create_supplier` function returns the expected response.

    Tests the response when create supplier is group.
    """

    # Define test data:
    test_data = {
        "supplier_id": "1166",
        "supplier_name": "Schafer Office (Print)",
        "country_code": "US",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {"d": {"BusinessPartner": test_data["supplier_id"]}}

        response = sap_s4_hana_create_supplier(
            supplier_name=test_data["supplier_name"],
            supplier_category="GROUP",
            supplier_country=test_data["country_code"],
        ).content

        assert response
        assert response.supplier_id == test_data["supplier_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_BUSINESS_PARTNER/A_BusinessPartner",
            payload={
                "BusinessPartnerCategory": "3",
                "to_BusinessPartnerRole": [
                    {
                        "BusinessPartnerRole": "FLVN01",
                    }
                ],
                "to_BusinessPartnerAddress": [{"Country": test_data["country_code"]}],
                "GroupBusinessPartnerName1": test_data["supplier_name"],
            },
        )
