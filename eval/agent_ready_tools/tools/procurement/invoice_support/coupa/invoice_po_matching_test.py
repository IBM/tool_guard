from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoice,
    CoupaInvoiceAccount,
    CoupaInvoiceAccountType,
    CoupaInvoiceCurrency,
    CoupaInvoiceLine,
    CoupaInvoicePerson,
    CoupaInvoiceSupplier,
)
from agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching import (
    coupa_invoice_po_matching,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
    CoupaOrderLine,
    CoupaOrderLines,
    CoupaPurchaseOrder,
    CoupaRequisition,
)


def test_coupa_invoice_po_matching() -> None:
    """Test that the invoice_po_matching function returns the expected response."""

    test_invoice_id = "713906"
    test_po_id = "4187"
    expected_status = "APPROVED"

    invoice_instance = CoupaInvoice(
        id=713906,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa1",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(
            id=40,
            name="Biffco",
        ),
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
                po_number=4187,
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
                po_number=4187,
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

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=4187,
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="issued",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="50",
        total_with_estimated_tax="1550.00",
        requisition_number=5403,
        shipping_address=CoupaAddress(
            id=12,
            street1="555 Bailey Ave",
            city="San Jose",
            state="California",
            postal_code="95141",
            location_code="",
            country="US",
        ),
        supplier_id=38,
        supplier_name="Biffco",
        requisition=CoupaRequisition(
            id=5403,
            status="received",
            created_by="mjordan",
            updated_by="mjordan",
            created_at="2025-04-01T00:00:00Z",
            updated_at="2025-05-01T00:00:00Z",
            currency="USD",
            line_count=2,
            total_with_estimated_tax="1550.00",
            requested_by="Meg(CEO) Jordan",
        ),
        order_lines=CoupaOrderLines(
            order_lines=[
                CoupaOrderLine(
                    order_line_id=6105,
                    order_line_num="1",
                    order_line_description="macbook pro",
                    order_line_type="OrderQuantityLine",
                    quantity="1.0",
                    price="1050.00",
                    total="1050.00",
                    amount_received=0.00,
                    receipt_approval_required=False,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    amount_received=0.00,
                    receipt_approval_required=False,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
            ]
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = [
            {"id": test_invoice_id},
            {"id": test_po_id},
        ]

        mock_read_invoice.return_value = invoice_instance
        mock_get_po.return_value = po_instance

        response = coupa_invoice_po_matching(test_invoice_id, test_po_id)
        result = response.content
        assert response.success is True
        assert result.status == expected_status
        assert result.message == "All fields match, no action needed"
        assert result.total_amount_match is True
        assert result.quantity_match == {"6105": True, "6106": True}
        assert result.unit_price_match == {"6105": True, "6106": True}


def test_blocked_invoice_quantity_mismatch() -> None:
    """Test that the invoice_po_matching function returns BLOCKED when quantities don't match."""
    test_invoice_id = "713906"
    test_po_id = "4187"
    expected_status = "BLOCKED"
    invoice_instance = CoupaInvoice(
        id=713906,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa1",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(
            id=40,
            name="Biffco",
        ),
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
                po_number=4187,
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
                po_number=4187,
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

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=4187,
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="issued",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="50",
        total_with_estimated_tax="1300.00",
        requisition_number=5403,
        shipping_address=CoupaAddress(
            id=12,
            street1="555 Bailey Ave",
            city="San Jose",
            state="California",
            postal_code="95141",
            location_code="",
            country="US",
        ),
        supplier_id=38,
        supplier_name="Biffco",
        requisition=CoupaRequisition(
            id=5403,
            status="received",
            created_by="mjordan",
            updated_by="mjordan",
            created_at="2025-04-01T00:00:00Z",
            updated_at="2025-05-01T00:00:00Z",
            currency="USD",
            line_count=2,
            total_with_estimated_tax="1300.00",
            requested_by="Meg(CEO) Jordan",
        ),
        order_lines=CoupaOrderLines(
            order_lines=[
                CoupaOrderLine(
                    order_line_id=6105,
                    order_line_num="1",
                    order_line_description="macbook pro",
                    order_line_type="OrderQuantityLine",
                    quantity="1.0",
                    price="1050.00",
                    total="1050.00",
                    amount_received=0.00,
                    receipt_approval_required=True,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="1.0",
                    price="250.00",
                    total="250.00",
                    amount_received=0.00,
                    receipt_approval_required=True,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
            ]
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = [
            {"id": test_invoice_id},
            {"id": test_po_id},
        ]

        mock_read_invoice.return_value = invoice_instance
        mock_get_po.return_value = po_instance

        response = coupa_invoice_po_matching(test_invoice_id, test_po_id)
        result = response.content
        assert response.success is True

        assert result.status == expected_status
        assert "Discrepancies found requiring review" in result.message
        assert result.total_amount_match is False
        assert result.quantity_match == {"6105": True, "6106": False}
        assert result.unit_price_match == {"6105": True, "6106": True}
        assert result.line_total_match == {"6105": True, "6106": False}
        assert "6106" in result.line_item_discrepancies
        assert result.line_item_discrepancies["6106"]["quantity"] is not None
        assert result.line_item_discrepancies["6106"]["quantity"]["invoice"] == 2.0
        assert result.line_item_discrepancies["6106"]["quantity"]["po"] == 1.0


def test_blocked_invoice_unit_price_mismatch() -> None:
    """Test that the invoice_po_matching function returns BLOCKED when unit prices don't match."""
    test_invoice_id = "713906"
    test_po_id = "4187"
    expected_status = "BLOCKED"

    invoice_instance = CoupaInvoice(
        id=713906,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa1",
        status="pending_receipt",
        total_with_taxes="1650.00",
        supplier=CoupaInvoiceSupplier(
            id=40,
            name="Biffco",
        ),
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
                po_number=4187,
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
                price="300.00",
                total="600.00",
                po_number=4187,
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

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=4187,
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="issued",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="50",
        total_with_estimated_tax="1550.00",
        requisition_number=5403,
        shipping_address=CoupaAddress(
            id=12,
            street1="555 Bailey Ave",
            city="San Jose",
            state="California",
            postal_code="95141",
            location_code="",
            country="US",
        ),
        supplier_id=38,
        supplier_name="Biffco",
        requisition=CoupaRequisition(
            id=5403,
            status="received",
            created_by="mjordan",
            updated_by="mjordan",
            created_at="2025-04-01T00:00:00Z",
            updated_at="2025-05-01T00:00:00Z",
            currency="USD",
            line_count=2,
            total_with_estimated_tax="1550.00",
            requested_by="Meg(CEO) Jordan",
        ),
        order_lines=CoupaOrderLines(
            order_lines=[
                CoupaOrderLine(
                    order_line_id=6105,
                    order_line_num="1",
                    order_line_description="macbook pro",
                    order_line_type="OrderQuantityLine",
                    quantity="1.0",
                    price="1050.00",
                    total="1050.00",
                    amount_received=0.00,
                    receipt_approval_required=True,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    amount_received=0.00,
                    receipt_approval_required=True,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
            ]
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = [
            {"id": test_invoice_id},
            {"id": test_po_id},
        ]

        mock_read_invoice.return_value = invoice_instance
        mock_get_po.return_value = po_instance

        response = coupa_invoice_po_matching(test_invoice_id, test_po_id)
        result = response.content
        assert response.success is True

        assert result.status == expected_status
        assert "Discrepancies found requiring review" in result.message
        assert result.total_amount_match is False
        assert result.quantity_match == {"6105": True, "6106": True}
        assert result.unit_price_match == {"6105": True, "6106": False}
        assert result.line_total_match == {"6105": True, "6106": False}
        assert "6106" in result.line_item_discrepancies
        assert result.line_item_discrepancies["6106"]["unit_price"] is not None
        assert result.line_item_discrepancies["6106"]["unit_price"]["invoice"] == 300.00
        assert result.line_item_discrepancies["6106"]["unit_price"]["po"] == 250.00
        assert result.line_item_discrepancies["6106"]["line_total"] is not None
        assert result.line_item_discrepancies["6106"]["line_total"]["invoice"] == 600.00
        assert result.line_item_discrepancies["6106"]["line_total"]["po"] == 500.00


def test_blocked_invoice_line_total_mismatch() -> None:
    """Test that the invoice_po_matching function returns BLOCKED when line totals don't match."""
    test_invoice_id = "713906"
    test_po_id = "4187"
    expected_status = "BLOCKED"

    invoice_instance = CoupaInvoice(
        id=713906,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa1",
        status="pending_receipt",
        total_with_taxes="1650.00",
        supplier=CoupaInvoiceSupplier(
            id=40,
            name="Biffco",
        ),
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
                po_number=4187,
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
                total="600.00",
                po_number=4187,
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

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=4187,
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="issued",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="50",
        total_with_estimated_tax="1550.00",
        requisition_number=5403,
        shipping_address=CoupaAddress(
            id=12,
            street1="555 Bailey Ave",
            city="San Jose",
            state="California",
            postal_code="95141",
            location_code="",
            country="US",
        ),
        supplier_id=38,
        supplier_name="Biffco",
        requisition=CoupaRequisition(
            id=5403,
            status="received",
            created_by="mjordan",
            updated_by="mjordan",
            created_at="2025-04-01T00:00:00Z",
            updated_at="2025-05-01T00:00:00Z",
            currency="USD",
            line_count=2,
            total_with_estimated_tax="1550.00",
            requested_by="Meg(CEO) Jordan",
        ),
        order_lines=CoupaOrderLines(
            order_lines=[
                CoupaOrderLine(
                    order_line_id=6105,
                    order_line_num="1",
                    order_line_description="macbook pro",
                    order_line_type="OrderQuantityLine",
                    quantity="1.0",
                    price="1050.00",
                    total="1050.00",
                    amount_received=0.00,
                    receipt_approval_required=True,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    amount_received=0.00,
                    receipt_approval_required=True,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                    account_id=1,
                    account_type_id=2,
                    uom_code="EA",
                    estimated_tax_amount="100",
                    total_with_estimated_tax="100",
                ),
            ]
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = [
            {"id": test_invoice_id},
            {"id": test_po_id},
        ]

        mock_read_invoice.return_value = invoice_instance
        mock_get_po.return_value = po_instance

        response = coupa_invoice_po_matching(test_invoice_id, test_po_id)
        result = response.content
        assert response.success is True
        assert result.status == expected_status
        assert "Discrepancies found requiring review" in result.message
        assert result.total_amount_match is False
        assert result.quantity_match == {"6105": True, "6106": True}
        assert result.unit_price_match == {"6105": True, "6106": True}
        assert result.line_total_match == {"6105": True, "6106": False}
        assert "6106" in result.line_item_discrepancies
        assert result.line_item_discrepancies["6106"]["line_total"] is not None
        assert result.line_item_discrepancies["6106"]["line_total"]["invoice"] == 600.00
        assert result.line_item_discrepancies["6106"]["line_total"]["po"] == 500.00


def test_missing_po() -> None:
    """Test that the invoice_po_matching function returns error status when PO is not found."""
    test_invoice_id = 713906
    test_po_id = 999999
    expected_status = "error"

    invoice_instance = CoupaInvoice(
        id=713906,
        invoice_date="2025-04-29T00:00:00-07:00",
        invoice_number="test_coupa1",
        status="pending_receipt",
        total_with_taxes="1550.00",
        supplier=CoupaInvoiceSupplier(
            id=40,
            name="Biffco",
        ),
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
                po_number=4187,
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
                po_number=4187,
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

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_invoice_from_response"
    ) as mock_read_invoice, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.invoice_po_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = [
            {"id": test_invoice_id},
            {"id": test_po_id},
        ]

        mock_read_invoice.return_value = invoice_instance
        mock_get_po.return_value = None
        response = coupa_invoice_po_matching(test_invoice_id, test_po_id)
        result = response.content
        assert response.success is False

        assert result.status == expected_status
        assert f"Purchase Order with ID {test_po_id} not found" in result.message
        assert result.invoice_id == test_invoice_id
        assert result.po_id == test_po_id
        assert result.total_amount_match is False
        assert not result.line_items_match
        assert not result.quantity_match
        assert not result.unit_price_match
        assert not result.line_total_match
        assert not result.line_item_discrepancies
