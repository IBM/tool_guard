from dataclasses import asdict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoice,
    CoupaInvoiceAccount,
    CoupaInvoiceAccountType,
    CoupaInvoiceCurrency,
    CoupaInvoiceLine,
    CoupaInvoicePerson,
    CoupaInvoiceSupplier,
    CoupaReceipt,
)
from agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching import (
    coupa_invoice_receipt_matching,
)


def test_coupa_invoice_receipt_matching() -> None:
    """Test that the invoice_receipt_matching function returns the expected response."""

    test_invoice_id = "713906"
    expected_status = "APPROVED"

    invoice_instance = CoupaInvoice(
        id=713906,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa1",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(id=40, name="Biffco"),
        currency=CoupaInvoiceCurrency(
            id=1,
            code="USD",
            decimals=2,
            updated_by=CoupaInvoicePerson(
                id=350,
                login="cnye",
                email="upgrade+cnye@coupa.com",
                firstname="Carroll",
                lastname="Nye",
                fullname="Carroll Nye",
            ),
        ),
        invoice_lines=[
            CoupaInvoiceLine(
                id=4909,
                description="macbook pro",
                quantity="1.0",
                price="1050.00",
                total="1050.00",
                po_number=4186,
                order_line_id=6105,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
            CoupaInvoiceLine(
                id=4910,
                description="mouse",
                quantity="2.0",
                price="250.00",
                total="500.00",
                po_number=4186,
                order_line_id=6106,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
        ],
    )
    receipt_instance_1 = CoupaReceipt(
        id=10596,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6105, "description": "macbook pro"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_2 = CoupaReceipt(
        id=10597,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6106, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_3 = CoupaReceipt(
        id=10598,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6106, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = {"id": test_invoice_id}

        mock_client.get_request_list.return_value = [
            {"id": receipt_instance_1.id},
            {"id": receipt_instance_2.id},
            {"id": receipt_instance_3.id},
        ]

        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(invoice_instance)
            if resource_name == f"invoices/{invoice_instance.id}"
            else (
                asdict(receipt_instance_1)
                if resource_name == f"receiving_transactions/{receipt_instance_1.id}"
                else (
                    asdict(receipt_instance_2)
                    if resource_name == f"receiving_transactions/{receipt_instance_2.id}"
                    else (
                        asdict(receipt_instance_3)
                        if resource_name == f"receiving_transactions/{receipt_instance_3.id}"
                        else {}
                    )
                )
            )
        )

        mock_read_invoice.return_value = invoice_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_invoice_receipt_matching(test_invoice_id)
        result = response.content

        assert response.success is True
        assert result.status == expected_status
        assert result.message == "All fields match, no action needed"
        assert result.total_amount_match is True
        assert result.quantity_match == {"6105": True, "6106": True}
        assert result.unit_price_match == {"6105": True, "6106": True}


def test_coupa_invoice_receipt_matching_price_mismatch() -> None:
    """Test that the invoice_receipt_matching function correctly identifies price mismatches."""

    test_invoice_id = "713907"
    expected_status = "BLOCKED"

    invoice_instance = CoupaInvoice(
        id=713907,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa2",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(id=40, name="Biffco"),
        currency=CoupaInvoiceCurrency(
            id=1,
            code="USD",
            decimals=2,
            updated_by=CoupaInvoicePerson(
                id=350,
                login="cnye",
                email="upgrade+cnye@coupa.com",
                firstname="Carroll",
                lastname="Nye",
                fullname="Carroll Nye",
            ),
        ),
        invoice_lines=[
            CoupaInvoiceLine(
                id=4911,
                description="macbook pro",
                quantity="1.0",
                price="1200.00",
                total="1200.00",
                po_number=4187,
                order_line_id=6107,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
            CoupaInvoiceLine(
                id=4912,
                description="mouse",
                quantity="2.0",
                price="250.00",
                total="500.00",
                po_number=4187,
                order_line_id=6108,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
        ],
    )

    receipt_instance_1 = CoupaReceipt(
        id=10599,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6107, "description": "macbook pro"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_2 = CoupaReceipt(
        id=10600,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6108, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_3 = CoupaReceipt(
        id=10601,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6108, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = {"id": test_invoice_id}

        mock_client.get_request_list.return_value = [
            {"id": receipt_instance_1.id},
            {"id": receipt_instance_2.id},
            {"id": receipt_instance_3.id},
        ]

        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(invoice_instance)
            if resource_name == f"invoices/{invoice_instance.id}"
            else (
                asdict(receipt_instance_1)
                if resource_name == f"receiving_transactions/{receipt_instance_1.id}"
                else (
                    asdict(receipt_instance_2)
                    if resource_name == f"receiving_transactions/{receipt_instance_2.id}"
                    else (
                        asdict(receipt_instance_3)
                        if resource_name == f"receiving_transactions/{receipt_instance_3.id}"
                        else {}
                    )
                )
            )
        )
        mock_read_invoice.return_value = invoice_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_invoice_receipt_matching(test_invoice_id)
        result = response.content

        assert response.success is True
        assert result.status == expected_status
        assert result.message == "Unit price mismatch on line 6107"
        assert result.total_amount_match is False
        assert result.quantity_match == {"6107": True, "6108": True}
        assert result.unit_price_match == {"6108": True}


def test_coupa_invoice_receipt_matching_quantity_mismatch() -> None:
    """Test that the invoice_receipt_matching function correctly identifies quantity mismatches."""

    test_invoice_id = "713908"
    expected_status = "BLOCKED"

    invoice_instance = CoupaInvoice(
        id=713908,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa3",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(id=40, name="Biffco"),
        currency=CoupaInvoiceCurrency(
            id=1,
            code="USD",
            decimals=2,
            updated_by=CoupaInvoicePerson(
                id=350,
                login="cnye",
                email="upgrade+cnye@coupa.com",
                firstname="Carroll",
                lastname="Nye",
                fullname="Carroll Nye",
            ),
        ),
        invoice_lines=[
            CoupaInvoiceLine(
                id=4913,
                description="macbook pro",
                quantity="2.0",
                price="1050.00",
                total="2100.00",
                po_number=4188,
                order_line_id=6109,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
            CoupaInvoiceLine(
                id=4914,
                description="mouse",
                quantity="2.0",
                price="250.00",
                total="500.00",
                po_number=4188,
                order_line_id=6110,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
        ],
    )

    receipt_instance_1 = CoupaReceipt(
        id=10602,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6109, "description": "macbook pro"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_2 = CoupaReceipt(
        id=10603,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6110, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_3 = CoupaReceipt(
        id=10604,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6110, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = {"id": test_invoice_id}

        mock_client.get_request_list.return_value = [
            {"id": receipt_instance_1.id},
            {"id": receipt_instance_2.id},
            {"id": receipt_instance_3.id},
        ]

        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(invoice_instance)
            if resource_name == f"invoices/{invoice_instance.id}"
            else (
                asdict(receipt_instance_1)
                if resource_name == f"receiving_transactions/{receipt_instance_1.id}"
                else (
                    asdict(receipt_instance_2)
                    if resource_name == f"receiving_transactions/{receipt_instance_2.id}"
                    else (
                        asdict(receipt_instance_3)
                        if resource_name == f"receiving_transactions/{receipt_instance_3.id}"
                        else {}
                    )
                )
            )
        )
        mock_read_invoice.return_value = invoice_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_invoice_receipt_matching(test_invoice_id)
        result = response.content

        assert response.success is True
        assert result.status == expected_status
        assert result.message == "Quantity mismatch on line 6109"
        assert result.total_amount_match is False
        assert result.quantity_match == {"6110": True}
        assert result.unit_price_match == {"6109": True, "6110": True}


def test_coupa_invoice_receipt_matching_missing_receipt() -> None:
    """Test that the invoice_receipt_matching function correctly identifies missing receipts."""

    test_invoice_id = "713909"
    expected_status = "BLOCKED"

    invoice_instance = CoupaInvoice(
        id=713909,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa4",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(id=40, name="Biffco"),
        currency=CoupaInvoiceCurrency(
            id=1,
            code="USD",
            decimals=2,
            updated_by=CoupaInvoicePerson(
                id=350,
                login="cnye",
                email="upgrade+cnye@coupa.com",
                firstname="Carroll",
                lastname="Nye",
                fullname="Carroll Nye",
            ),
        ),
        invoice_lines=[
            CoupaInvoiceLine(
                id=4915,
                description="macbook pro",
                quantity="1.0",
                price="1050.00",
                total="1050.00",
                po_number=4189,
                order_line_id=6111,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
            CoupaInvoiceLine(
                id=4916,
                description="mouse",
                quantity="2.0",
                price="250.00",
                total="500.00",
                po_number=4189,
                order_line_id=6112,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
        ],
    )

    receipt_instance_1 = CoupaReceipt(
        id=10605,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6111, "description": "macbook pro"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_2 = CoupaReceipt(
        id=10606,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6112, "description": "mouse"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = {"id": test_invoice_id}
        mock_client.get_request_list.return_value = [
            {"id": receipt_instance_1.id},
            {"id": receipt_instance_2.id},
        ]

        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(invoice_instance)
            if resource_name == f"invoices/{invoice_instance.id}"
            else (
                asdict(receipt_instance_1)
                if resource_name == f"receiving_transactions/{receipt_instance_1.id}"
                else (
                    asdict(receipt_instance_2)
                    if resource_name == f"receiving_transactions/{receipt_instance_2.id}"
                    else {}
                )
            )
        )
        mock_read_invoice.return_value = invoice_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2]

        response = coupa_invoice_receipt_matching(test_invoice_id)
        result = response.content

        assert response.success is True
        assert result.status == expected_status
        assert result.message == "Quantity mismatch on line 6112"
        assert result.total_amount_match is False
        assert result.quantity_match == {"6111": True}
        assert result.unit_price_match == {"6111": True, "6112": True}


def test_coupa_invoice_receipt_matching_description_mismatch() -> None:
    """Test that the invoice_receipt_matching function correctly identifies description
    mismatches."""

    test_invoice_id = "713910"
    expected_status = "BLOCKED"

    invoice_instance = CoupaInvoice(
        id=713910,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa5",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(id=40, name="Biffco"),
        currency=CoupaInvoiceCurrency(
            id=1,
            code="USD",
            decimals=2,
            updated_by=CoupaInvoicePerson(
                id=350,
                login="cnye",
                email="upgrade+cnye@coupa.com",
                firstname="Carroll",
                lastname="Nye",
                fullname="Carroll Nye",
            ),
        ),
        invoice_lines=[
            CoupaInvoiceLine(
                id=4917,
                description="MacBook Pro 16-inch M2",
                quantity="1.0",
                price="1050.00",
                total="1050.00",
                po_number=4190,
                order_line_id=6113,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
            CoupaInvoiceLine(
                id=4918,
                description="Wireless Mouse MX Master 3",
                quantity="2.0",
                price="250.00",
                total="500.00",
                po_number=4190,
                order_line_id=6114,
                account=CoupaInvoiceAccount(
                    id=1,
                    account_type=CoupaInvoiceAccountType(
                        id=1,
                        name="PREV ERP 1",
                        active=True,
                    ),
                ),
            ),
        ],
    )

    receipt_instance_1 = CoupaReceipt(
        id=10607,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6113, "description": "MacBook Pro 16-inch"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_2 = CoupaReceipt(
        id=10608,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6114, "description": "Wireless Mouse MX Master 3"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    receipt_instance_3 = CoupaReceipt(
        id=10609,
        price="250.00",
        quantity="1.0",
        total="250.00",
        order_line={"id": 6114, "description": "Wireless Mouse MX Master 3"},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(
                    id=1,
                    code="USD",
                    decimals=2,
                ),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_receipt_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = {"id": test_invoice_id}

        mock_client.get_request_list.return_value = [
            {"id": receipt_instance_1.id},
            {"id": receipt_instance_2.id},
            {"id": receipt_instance_3.id},
        ]

        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(invoice_instance)
            if resource_name == f"invoices/{invoice_instance.id}"
            else (
                asdict(receipt_instance_1)
                if resource_name == f"receiving_transactions/{receipt_instance_1.id}"
                else (
                    asdict(receipt_instance_2)
                    if resource_name == f"receiving_transactions/{receipt_instance_2.id}"
                    else (
                        asdict(receipt_instance_3)
                        if resource_name == f"receiving_transactions/{receipt_instance_3.id}"
                        else {}
                    )
                )
            )
        )
        mock_read_invoice.return_value = invoice_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_invoice_receipt_matching(test_invoice_id)
        result = response.content

        assert response.success is True
        assert result.status == expected_status
        assert result.message == "Description mismatch on line 6113"
        assert result.total_amount_match is False
        assert result.quantity_match == {"6113": True, "6114": True}
        assert result.unit_price_match == {"6113": True, "6114": True}
