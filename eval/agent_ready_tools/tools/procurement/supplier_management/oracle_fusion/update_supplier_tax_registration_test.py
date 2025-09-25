from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.update_supplier_tax_registration import (
    oracle_fusion_update_supplier_tax_registration,
)


def test_oracle_fusion_update_supplier_tax_registration() -> None:
    """Test that the `oracle_fusion_update_supplier_tax_registration` function updates supplier tax
    registration details."""

    # Define test data
    test_data = {
        "registration_id": "300000025229352",
        "tax_point_basis": "INVOICE",
        "registration_type_code": "CNPJ",
        "registration_status_code": "EC_REG(NON FR)",
        "registration_reason_code": "MINIMUM_PRESENCE",
        "registration_source_code": "EXPLICIT",
        "rounding_rule_code": "NEAREST",
        "tax_authority_id": "300000025295659",
        "legal_location_id": "300000015729683",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.update_supplier_tax_registration.get_oracle_fusion_client"
    ) as mock_oracle_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.patch_request.return_value = {
            "TaxPointBasis": test_data["tax_point_basis"],
            "RegistrationTypeCode": test_data["registration_type_code"],
            "RegistrationStatusCode": test_data["registration_status_code"],
            "RegistrationReasonCode": test_data["registration_reason_code"],
            "RegistrationSourceCode": test_data["registration_source_code"],
            "RoundingRuleCode": test_data["rounding_rule_code"],
            "TaxAuthorityId": test_data["tax_authority_id"],
            "LegalLocationId": test_data["legal_location_id"],
        }

        # Call the function
        response = oracle_fusion_update_supplier_tax_registration(
            registration_id=test_data["registration_id"],
            tax_point_basis=test_data["tax_point_basis"],
            registration_type_code=test_data["registration_type_code"],
            registration_status_code=test_data["registration_status_code"],
            registration_reason_code=test_data["registration_reason_code"],
            registration_source_code=test_data["registration_source_code"],
            rounding_rule_code=test_data["rounding_rule_code"],
            tax_authority_id=test_data["tax_authority_id"],
            legal_location_id=test_data["legal_location_id"],
        ).content

        assert response
        assert response.tax_point_basis == test_data["tax_point_basis"]
        assert response.registration_type_code == test_data["registration_type_code"]
        assert response.registration_status_code == test_data["registration_status_code"]
        assert response.registration_reason_code == test_data["registration_reason_code"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            resource_name=f"taxRegistrations/{test_data["registration_id"]}",
            payload={
                "TaxPointBasis": test_data["tax_point_basis"],
                "RegistrationTypeCode": test_data["registration_type_code"],
                "RegistrationStatusCode": test_data["registration_status_code"],
                "RegistrationReasonCode": test_data["registration_reason_code"],
                "RegistrationSourceCode": test_data["registration_source_code"],
                "RoundingRuleCode": test_data["rounding_rule_code"],
                "TaxAuthorityId": test_data["tax_authority_id"],
                "LegalLocationId": test_data["legal_location_id"],
            },
        )
