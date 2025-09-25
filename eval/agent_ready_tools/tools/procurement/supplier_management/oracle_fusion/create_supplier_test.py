from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.create_supplier import (
    oracle_fusion_create_supplier,
)


def test_oracle_fusion_update_single_supplier_success() -> None:
    """Test the successful creation of a single supplier in Oracle Fusion."""
    # 1. Define the input data for the function
    supplier_name = "Test Corp"
    tax_organization_type = "Corporation"
    business_relationship = "Prospective"
    supplier_number = "TC-001"

    # 2. Define the expected successful response from the mock API client
    mock_api_response = {
        "SupplierId": 12345,
        "Supplier": "Test Corp",
        "TaxOrganizationType": "Corporation",
        "BusinessRelationship": "Prospective",
        "SupplierNumber": "TC-001",  # <-- Add this to the expectation
    }

    # 3. Patch the client factory to inject our mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.create_supplier.get_oracle_fusion_client"
    ) as mock_get_client:
        # Configure the mock client and its post_request method
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = mock_api_response

        # 4. Call the function with the test data
        response = oracle_fusion_create_supplier(
            supplier_name,
            tax_organization_type,
            business_relationship,
            supplier_number,
        )
        assert response

        # 5. Assert the results
        assert response.success is True

        # 6. Assert that the client was called correctly
        expected_payload = {
            "Supplier": supplier_name,
            "TaxOrganizationType": "Corporation",
            "BusinessRelationship": "Prospective",
            "SupplierNumber": "TC-001",
        }
        mock_client.post_request.assert_called_once_with(
            resource_name="suppliers", payload=expected_payload
        )
