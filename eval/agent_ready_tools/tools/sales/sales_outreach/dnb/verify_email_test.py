from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_outreach.dnb.verify_email import (
    EmailVerificationResponse,
    verify_email_address,
)


def test_verify_email_mm() -> None:
    """Test that passing a valid email address leads to email verification details."""

    # Define test data:
    test_data: Dict[str, Dict[str, Any]] = {
        "emailVerificationDetails": {
            "threatRisk": "Y",
            "disposition": "Successful Delivery",
            "deliverabilityScore": 93,
            "deliverabilityRating": "Good",
            "emailType": "Business",
            "isDarkWeb": False,
        }
    }

    resp = EmailVerificationResponse(**test_data["emailVerificationDetails"])
    parsed_fields = {
        k: v for k, v in test_data["emailVerificationDetails"].items() if k != "isRoleEmail"
    }
    assert EmailVerificationResponse.model_dump(resp, by_alias=True) == parsed_fields
    assert isinstance(resp.email_type, str)
    assert resp.email_type == "Business"


def test_verify_email() -> None:
    """Test that class ignores extra fields."""

    # Define test data:
    test_data: Dict[str, Dict[str, Any]] = {
        "emailVerificationDetails": {
            "threatRisk": "Y",
            "disposition": "Successful Delivery",
            "deliverabilityScore": 93,
            "deliverabilityRating": "Good",
            "emailType": "Business",
            "isRoleEmail": True,  # check ignored fields
            "isDarkWeb": False,
        }
    }

    # Patch the get_dnb_client function in the module where it's imported.
    with patch(
        "agent_ready_tools.tools.sales.sales_outreach.dnb.verify_email.get_dnb_client"
    ) as mock_get_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_client.get_request.return_value = test_data
        mock_get_dnb_client.return_value = mock_client

        # Call the function with a valid IBM's DUNS number.
        result = verify_email_address(email_address="anton.relin@ibm.com")

        # Verify that get_request was called exactly once.
        mock_client.get_request.assert_called_once()

        # Ensure that get_news_and_media() executed and returned proper values
        if result is not None:
            # Verify that the result is an instance of EmailVerificationResponse.
            assert isinstance(result, EmailVerificationResponse)
            # Assert that each attribute of the EmailVerificationResponse is not empty.
            assert result.threat_risk == test_data["emailVerificationDetails"]["threatRisk"]
            assert result.disposition == test_data["emailVerificationDetails"]["disposition"]
            assert (
                result.deliverability_score
                == test_data["emailVerificationDetails"]["deliverabilityScore"]
            )
            assert (
                result.deliverability_rating
                == test_data["emailVerificationDetails"]["deliverabilityRating"]
            )
            assert result.email_type == test_data["emailVerificationDetails"]["emailType"]
            assert result.is_dark_web == test_data["emailVerificationDetails"]["isDarkWeb"]
