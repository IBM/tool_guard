from dataclasses import asdict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoiceAccount,
    CoupaInvoiceAccountType,
    CoupaInvoiceCurrency,
    CoupaReceipt,
)
from agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching import (
    coupa_po_all_receipts_matching,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
    CoupaOrderLine,
    CoupaOrderLines,
    CoupaPurchaseOrder,
    CoupaRequisition,
)


def test_coupa_po_all_receipts_matching() -> None:
    """Test that po_all_receipts_matching runs full po_receipt_matching logic and returns
    APPROVED."""

    test_data = {"purchase_order_id": 4187}

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=test_data["purchase_order_id"],
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
        estimated_tax_amount="",
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
        supplier_id=0,
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
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                ),
            ]
        ),
    )

    receipt_instance_1 = CoupaReceipt(
        id=10596,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6105},
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
        order_line={"id": 6106},
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
        order_line={"id": 6106},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(id=1, code="USD", decimals=2),
            ),
        ),
    )

    receipt_ids_mock = MagicMock()
    receipt_ids_mock.receipt_ids = [10596, 10597, 10598]

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(po_instance)
            if resource_name == f"purchase_orders/{po_instance.purchase_order_id}"
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

        mock_client.get_request_list.return_value = [
            asdict(receipt_instance_1),
            asdict(receipt_instance_2),
            asdict(receipt_instance_3),
        ]

        mock_get_po.return_value = po_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_po_all_receipts_matching(test_data["purchase_order_id"])
        result = response.content

        assert response.success is True

        assert result.overall_status == "APPROVED"
        assert result.message == "All receipts match with PO"


def test_blocked_po_with_2_receipts() -> None:
    """Test that po_all_receipts_matching returns BLOCKED when one receipt is missing."""

    test_data = {"purchase_order_id": 4187}

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=test_data["purchase_order_id"],
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="blocked",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="",
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
        supplier_id=0,
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
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                ),
            ]
        ),
    )

    receipt_instance_1 = CoupaReceipt(
        id=10596,
        price="1050.00",
        quantity="1.0",
        total="1050.00",
        order_line={"id": 6105},
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
        order_line={"id": 6106},
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

    receipt_ids_mock = MagicMock()
    receipt_ids_mock.receipt_ids = [10596, 10597]  # Only 2 receipts instead of 3

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(po_instance)
            if resource_name == f"purchase_orders/{po_instance.purchase_order_id}"
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

        mock_client.get_request_list.return_value = [
            asdict(receipt_instance_1),
            asdict(receipt_instance_2),
        ]

        mock_get_po.return_value = po_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2]

        response = coupa_po_all_receipts_matching(test_data["purchase_order_id"])

        result = response.content

        assert response.success is True

        assert result.overall_status == "BLOCKED"
        print(result.overall_status)
        assert (
            result.message == "Quantity mismatch on line 6106\nTotal amount mismatch on line 6106"
        )


def test_blocked_po_with_no_receipts() -> None:
    """Test that po_all_receipts_matching returns BLOCKED when there are no receipts."""

    test_data = {"purchase_order_id": 4187}

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=test_data["purchase_order_id"],
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="blocked",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="",
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
        supplier_id=0,
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
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                ),
            ]
        ),
    )

    receipt_ids_mock = MagicMock()
    receipt_ids_mock.receipt_ids = []

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(po_instance)
            if resource_name == f"purchase_orders/{po_instance.purchase_order_id}"
            else {}
        )

        mock_client.get_request_list.return_value = []

        mock_get_po.return_value = po_instance
        mock_view_receipt.side_effect = []
        response = coupa_po_all_receipts_matching(test_data["purchase_order_id"])
        result = response.content

        assert response.success is False
        assert result.overall_status == "BLOCKED"
        assert result.message == "No receipts found for PO 4187"


def test_blocked_po_with_excess_quantity() -> None:
    """Test that po_all_receipts_matching returns BLOCKED when receipt quantity exceeds PO
    quantity."""

    test_data = {"purchase_order_id": 4187}

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=test_data["purchase_order_id"],
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="blocked",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="",
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
        supplier_id=0,
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
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                ),
            ]
        ),
    )

    receipt_instance_1 = CoupaReceipt(
        id=10596,
        price="1050.00",
        quantity="2.0",
        total="2100.00",
        order_line={"id": 6105},
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
        order_line={"id": 6106},
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
        order_line={"id": 6106},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(id=1, code="USD", decimals=2),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(po_instance)
            if resource_name == f"purchase_orders/{po_instance.purchase_order_id}"
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
        mock_client.get_request_list.return_value = [
            asdict(receipt_instance_1),
            asdict(receipt_instance_2),
            asdict(receipt_instance_3),
        ]

        mock_get_po.return_value = po_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_po_all_receipts_matching(test_data["purchase_order_id"])
        result = response.content

        assert response.success is True
        assert result.overall_status == "BLOCKED"
        assert (
            result.message == "Quantity mismatch on line 6105\nTotal amount mismatch on line 6105"
        )


def test_blocked_po_with_price_mismatch() -> None:
    """Test that po_all_receipts_matching returns BLOCKED when receipt unit price doesn't match
    PO."""

    test_data = {"purchase_order_id": 4187}

    po_instance = CoupaPurchaseOrder(
        purchase_order_id=test_data["purchase_order_id"],
        po_number="4187",
        created_by="mjordan",
        updated_by="mjordan",
        created_at="2025-04-01T00:00:00Z",
        updated_at="2025-05-01T00:00:00Z",
        status="blocked",
        transmission_status="sent",
        exported=False,
        ship_to_attention="Meg(CEO) Jordan",
        requested_by="Meg(CEO) Jordan",
        payment_method="invoice",
        currency="USD",
        estimated_tax_amount="",
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
        supplier_id=0,
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
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="macbook pro",
                    unit="Each",
                    supplier_part_number="MBP-001",
                    supplier_auxiliary_part_number="",
                    commodity="Computers",
                    manufacturer_name="Apple",
                    manufacturer_part_number="10101",
                ),
                CoupaOrderLine(
                    order_line_id=6106,
                    order_line_num="2",
                    order_line_description="mouse",
                    order_line_type="OrderQuantityLine",
                    quantity="2.0",
                    price="250.00",
                    total="500.00",
                    account_id=0,
                    account_type_id=0,
                    uom_code="",
                    estimated_tax_amount="",
                    total_with_estimated_tax="",
                    amount_received=float(0.00),
                    receipt_approval_required=False,
                    item_description="mouse",
                    unit="Each",
                    supplier_part_number="MSE-002",
                    supplier_auxiliary_part_number="",
                    commodity="Peripherals",
                    manufacturer_name="Logitech",
                    manufacturer_part_number="20202",
                ),
            ]
        ),
    )

    receipt_instance_1 = CoupaReceipt(
        id=10596,
        price="1200.00",
        quantity="1.0",
        total="1200.00",
        order_line={"id": 6105},
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
        order_line={"id": 6106},
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
        order_line={"id": 6106},
        account=CoupaInvoiceAccount(
            id=1001,
            account_type=CoupaInvoiceAccountType(
                id=99,
                currency=CoupaInvoiceCurrency(id=1, code="USD", decimals=2),
            ),
        ),
    )

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.get_coupa_client"
    ) as mock_coupa_client, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_purchase_order_from_response"
    ) as mock_get_po, patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.po_all_receipts_matching.coupa_build_receipt_from_response"
    ) as mock_view_receipt:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.side_effect = lambda resource_name, **kwargs: (
            asdict(po_instance)
            if resource_name == f"purchase_orders/{po_instance.purchase_order_id}"
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

        mock_client.get_request_list.return_value = [
            asdict(receipt_instance_1),
            asdict(receipt_instance_2),
            asdict(receipt_instance_3),
        ]

        mock_get_po.return_value = po_instance
        mock_view_receipt.side_effect = [receipt_instance_1, receipt_instance_2, receipt_instance_3]

        response = coupa_po_all_receipts_matching(test_data["purchase_order_id"])
        result = response.content

        assert response.success is True
        assert result.overall_status == "BLOCKED"
        assert (
            result.message == "Unit price mismatch on line 6105\nTotal amount mismatch on line 6105"
        )
