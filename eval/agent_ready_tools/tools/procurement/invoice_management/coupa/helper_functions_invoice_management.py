from typing import Any, Dict

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoice,
    CoupaInvoiceAccount,
    CoupaInvoiceAccountType,
    CoupaInvoiceAddress,
    CoupaInvoiceCommodity,
    CoupaInvoiceCountry,
    CoupaInvoiceCurrency,
    CoupaInvoiceItem,
    CoupaInvoiceLine,
    CoupaInvoicePaymentTerm,
    CoupaInvoicePerson,
    CoupaInvoiceSupplier,
    CoupaInvoiceSupplierContact,
    CoupaInvoiceUOM,
    CoupaReceipt,
    CoupaReceiptHeader,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaOrderLine,
)


def coupa_convert_invoice_number_to_invoice_id(invoice_number: str) -> int:
    """
    Helper function to find an invoice ID using an invoice number.

    Args:
        invoice_number: an alphanumeric invoice number

    Returns:
        the corresponding invoice id or -1 if no such invoice found
    """
    params = {
        "fields": '["id"]',
        "invoice-number": invoice_number,
    }
    client = get_coupa_client()
    response = client.get_request_list(resource_name="invoices", params=params)
    return response[0]["id"] if response and isinstance(response, list) else -1


def coupa_build_receipt_from_response(response: Dict[str, Any]) -> CoupaReceipt:
    """Build a CoupaReceipt object from the API response."""
    receipt = CoupaReceipt(
        id=response["id"],
        created_at=response.get("created-at", ""),
        updated_at=response.get("updated-at", ""),
        barcode=response.get("barcode"),
        price=response.get("price"),
        quantity=response.get("quantity"),
        rfid_tag=response.get("rfid-tag"),
        total=response.get("total"),
        transaction_date=response.get("transaction-date"),
        type=response.get("type"),
        status=response.get("status"),
        exported=response.get("exported"),
        last_exported_at=response.get("last-exported-at"),
        receipts_batch_id=response.get("receipts-batch-id"),
        received_weight=response.get("received-weight"),
        match_reference=response.get("match-reference"),
        original_transaction_id=response.get("original-transaction-id"),
        voided_value=response.get("voided-value"),
        account_allocations=response.get("account-allocations"),
        order_line=response.get("order-line"),
        to_warehouse_location=response.get("to-warehouse-location"),
        asset_tags=response.get("asset-tags"),
        attachments=response.get("attachments"),
        inventory_transaction_valuations=response.get("inventory-transaction-valuations"),
        inventory_transaction_lots=response.get("inventory-transaction-lots"),
        current_integration_history_records=response.get("current-integration-history-records"),
    )
    item = response.get("item")
    if item:
        receipt.item = CoupaInvoiceItem(
            id=item["id"],
            created_at=item.get("created-at", ""),
            updated_at=item.get("updated-at", ""),
            description=item.get("description"),
            item_number=item.get("item-number"),
            name=item.get("name"),
            active=item.get("active"),
            storage_quantity=item.get("storage-quantity"),
            image_url=item.get("image-url"),
            manufacturer_name=item.get("manufacturer-name"),
            manufacturer_part_number=item.get("manufacturer-part-number"),
            item_type=item.get("item-type"),
            pack_qty=item.get("pack-qty"),
            pack_weight=item.get("pack-weight"),
            pack_uom_idy=item.get("pack-uom-idy"),
            receive_catch_weight=item.get("receive-catch-weight"),
            allow_partial_quantity=item.get("allow-partial-quantity"),
            inventory_lot_tracking_enabled=item.get("inventory-lot-tracking_enabled"),
            inventory_lot_expiration_type=item.get("inventory-lot-expiration_type"),
        )
        commodity = item.get("commodity")
        if commodity:
            receipt.item.commodity = CoupaInvoiceCommodity(
                commodity["id"],
                created_at=commodity.get("created-at", ""),
                updated_at=commodity.get("updated-at", ""),
                active=commodity.get("active"),
                name=commodity.get("name"),
                translated_name=commodity.get("translated-name"),
                deductibility=commodity.get("deductibility"),
                category=commodity.get("category"),
                subcategory=commodity.get("subcategory"),
                imported_from_taxonomy=commodity.get("imported-from-taxonomy"),
                gl=commodity.get("gl"),
                common_gl_acct=commodity.get("common-gl-acct"),
                parent=commodity.get("parent"),
            )
            created_by = commodity.get("created-by")
            if created_by:
                receipt.item.commodity.created_by = CoupaInvoicePerson(
                    id=created_by["id"],
                    login=created_by.get("login"),
                    email=created_by.get("email"),
                    employee_number=created_by.get("employee-number"),
                    firstname=created_by.get("firstname"),
                    lastname=created_by.get("lastname"),
                    fullname=created_by.get("fullname"),
                    salesforce_id=created_by.get("salesforce-id"),
                    avatar_thumb_url=created_by.get("avatar-thumb-url"),
                    assignee=created_by.get("assignee"),
                )
            updated_by = commodity.get("updated-by")
            if updated_by:
                receipt.item.commodity.updated_by = CoupaInvoicePerson(
                    id=updated_by["id"],
                    login=updated_by.get("login"),
                    email=updated_by.get("email"),
                    employee_number=updated_by.get("employee-number"),
                    firstname=updated_by.get("firstname"),
                    lastname=updated_by.get("lastname"),
                    fullname=updated_by.get("fullname"),
                    salesforce_id=updated_by.get("salesforce-id"),
                    avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                    assignee=updated_by.get("assignee"),
                )
    uom = response.get("uom")
    if uom:
        receipt.uom = CoupaInvoiceUOM(
            id=uom["id"],
            created_at=uom.get("created-at", ""),
            updated_at=uom.get("updated-at", ""),
            code=uom.get("code"),
            name=uom.get("name"),
            allowable_precision=uom.get("allowable_precision"),
            active=uom.get("active"),
        )
        updated_by = uom.get("updated-by")
        if updated_by:
            receipt.uom.updated_by = CoupaInvoicePerson(
                id=updated_by["id"],
                login=updated_by.get("login"),
                email=updated_by.get("email"),
                employee_number=updated_by.get("employee-number"),
                firstname=updated_by.get("firstname"),
                lastname=updated_by.get("lastname"),
                fullname=updated_by.get("fullname"),
                salesforce_id=updated_by.get("salesforce-id"),
                avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                assignee=updated_by.get("assignee"),
            )
    account = response.get("account")
    if account:
        receipt.account = CoupaInvoiceAccount(
            account["id"],
            created_at=account.get("created-at", ""),
            updated_at=account.get("updated-at", ""),
            name=account.get("name"),
            code=account.get("code"),
            active=account.get("active"),
            account_type_id=account.get("account-type-id"),
            # segment_1=account.get("segment-1"),
            # segment_2=account.get("segment-2"),
            # segment_3=account.get("segment-3"),
            # segment_4=account.get("segment-4"),
            # segment_5=account.get("segment-5"),
            # segment_6=account.get("segment-6"),
            # segment_7=account.get("segment-7"),
            # segment_8=account.get("segment-8"),
            # segment_9=account.get("segment-9"),
            # segment_10=account.get("segment-10"),
            # segment_11=account.get("segment-11"),
            # segment_12=account.get("segment-12"),
            # segment_13=account.get("segment-13"),
            # segment_14=account.get("segment-14"),
            # segment_15=account.get("segment-15"),
            # segment_16=account.get("segment-16"),
            # segment_17=account.get("segment-17"),
            # segment_18=account.get("segment-18"),
            # segment_19=account.get("segment-19"),
            # segment_20=account.get("segment-20"),
        )
        account_type = account.get("account-type")
        if account_type:
            receipt.account.account_type = CoupaInvoiceAccountType(
                account_type["id"],
                created_at=account_type.get("created-at", ""),
                updated_at=account_type.get("updated-at", ""),
                name=account_type.get("name"),
                active=account_type.get("active"),
                legal_entity_name=account_type.get("legal-entity-name"),
                dynamic_flag=account_type.get("dynamic-flag"),
            )
            currency = account_type.get("currency")
            if currency:
                receipt.account.account_type.currency = CoupaInvoiceCurrency(
                    id=currency["id"],
                    code=currency.get("code"),
                    decimals=currency.get("decimals"),
                )
                updated_by = currency.get("updated-by")
                if updated_by:
                    receipt.account.account_type.updated_by = CoupaInvoicePerson(
                        id=updated_by["id"],
                        login=updated_by.get("login"),
                        email=updated_by.get("email"),
                        employee_number=updated_by.get("employee-number"),
                        firstname=updated_by.get("firstname"),
                        lastname=updated_by.get("lastname"),
                        fullname=updated_by.get("fullname"),
                        salesforce_id=updated_by.get("salesforce-id"),
                        avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                        assignee=updated_by.get("assignee"),
                    )
            primary_address = account_type.get("primary_address")
            if primary_address:
                receipt.account.account_type.primary_address = CoupaInvoiceAddress(
                    id=primary_address["id"],
                    created_at=primary_address.get("created-at", ""),
                    updated_at=primary_address.get("updated-at", ""),
                    name=primary_address.get("name"),
                    location_code=primary_address.get("location-code"),
                    street1=primary_address.get("street1"),
                    street2=primary_address.get("street2"),
                    street3=primary_address.get("street3"),
                    street4=primary_address.get("street4"),
                    city=primary_address.get("city"),
                    state=primary_address.get("state"),
                    postal_code=primary_address.get("postal-code"),
                    attention=primary_address.get("attention"),
                    active=primary_address.get("active"),
                    business_group_name=primary_address.get("business-group-name"),
                    vat_number=primary_address.get("vat-number"),
                    local_tax_number=primary_address.get("local-tax-number"),
                    type=primary_address.get("type"),
                    address_type=primary_address.get("address-type"),
                    default=primary_address.get("default"),
                    custom_fields=primary_address.get("custom-fields"),
                )
                country = primary_address.get("country")
                if country:
                    receipt.account.account_type.primary_address.country = CoupaInvoiceCountry(
                        id=country["id"],
                        code=country.get("code"),
                        name=country.get("name"),
                    )
                vat_country = primary_address.get("vat_country")
                if vat_country:
                    receipt.account.account_type.primary_address.vat_country = CoupaInvoiceCountry(
                        id=country["id"],
                        code=country.get("code"),
                        name=country.get("name"),
                    )
            created_by = account_type.get("created-by")
            if created_by:
                receipt.account.account_type.created_by = CoupaInvoicePerson(
                    id=created_by["id"],
                    login=created_by.get("login"),
                    email=created_by.get("email"),
                    employee_number=created_by.get("employee-number"),
                    firstname=created_by.get("firstname"),
                    lastname=created_by.get("lastname"),
                    fullname=created_by.get("fullname"),
                    salesforce_id=created_by.get("salesforce-id"),
                    avatar_thumb_url=created_by.get("avatar-thumb-url"),
                    assignee=created_by.get("assignee"),
                )
            updated_by = account_type.get("updated-by")
            if updated_by:
                receipt.account.account_type.updated_by = CoupaInvoicePerson(
                    id=updated_by["id"],
                    login=updated_by.get("login"),
                    email=updated_by.get("email"),
                    employee_number=updated_by.get("employee-number"),
                    firstname=updated_by.get("firstname"),
                    lastname=updated_by.get("lastname"),
                    fullname=updated_by.get("fullname"),
                    salesforce_id=updated_by.get("salesforce-id"),
                    avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                    assignee=updated_by.get("assignee"),
                )
        created_by = account.get("created-by")
        if created_by:
            receipt.account.created_by = CoupaInvoicePerson(
                id=created_by["id"],
                login=created_by.get("login"),
                email=created_by.get("email"),
                employee_number=created_by.get("employee-number"),
                firstname=created_by.get("firstname"),
                lastname=created_by.get("lastname"),
                fullname=created_by.get("fullname"),
                salesforce_id=created_by.get("salesforce-id"),
                avatar_thumb_url=created_by.get("avatar-thumb-url"),
                assignee=created_by.get("assignee"),
            )
        updated_by = account.get("updated-by")
        if updated_by:
            receipt.account.updated_by = CoupaInvoicePerson(
                id=updated_by["id"],
                login=updated_by.get("login"),
                email=updated_by.get("email"),
                employee_number=updated_by.get("employee-number"),
                firstname=updated_by.get("firstname"),
                lastname=updated_by.get("lastname"),
                fullname=updated_by.get("fullname"),
                salesforce_id=updated_by.get("salesforce-id"),
                avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                assignee=updated_by.get("assignee"),
            )
    created_by = response.get("created-by")
    if created_by:
        receipt.created_by = CoupaInvoicePerson(
            id=created_by["id"],
            login=created_by.get("login"),
            email=created_by.get("email"),
            employee_number=created_by.get("employee-number"),
            firstname=created_by.get("firstname"),
            lastname=created_by.get("lastname"),
            fullname=created_by.get("fullname"),
            salesforce_id=created_by.get("salesforce-id"),
            avatar_thumb_url=created_by.get("avatar-thumb-url"),
            assignee=created_by.get("assignee"),
        )
    updated_by = response.get("updated-by")
    if updated_by:
        receipt.updated_by = CoupaInvoicePerson(
            id=updated_by["id"],
            login=updated_by.get("login"),
            email=updated_by.get("email"),
            employee_number=updated_by.get("employee-number"),
            firstname=updated_by.get("firstname"),
            lastname=updated_by.get("lastname"),
            fullname=updated_by.get("fullname"),
            salesforce_id=updated_by.get("salesforce-id"),
            avatar_thumb_url=updated_by.get("avatar-thumb-url"),
            assignee=updated_by.get("assignee"),
        )
    return receipt


def coupa_build_invoice_from_response(response: Dict[str, Any]) -> CoupaInvoice:
    """Build a CoupaInvoice object from the response of the API."""
    invoice = CoupaInvoice(
        id=int(response["id"]),
        invoice_lines=[],
        created_at=response.get("created-at", ""),
        updated_at=response.get("updated-at", ""),
        invoice_date=response.get("invoice-date"),
        net_due_date=response.get("net-due-date"),
        invoice_number=response.get("invoice-number"),
        status=response.get("status"),
        shipping_amount=response.get("shipping-amount"),
        handling_amount=response.get("handling-amount"),
        misc_amount=response.get("misc-amount"),
        tax_amount=response.get("tax-amount"),
        total_with_taxes=response.get("total-with-taxes"),
        gross_total=response.get("gross-total"),
        paid=response.get("paid"),
        payment_date=response.get("payment-date"),
        payment_notes=response.get("payment-notes"),
    )
    supplier = response.get("supplier")
    if supplier:
        invoice.supplier = CoupaInvoiceSupplier(
            supplier["id"],
            supplier.get("name"),
            supplier.get("display-name"),
            supplier.get("number"),
            supplier.get("risk-level"),
            supplier.get("custom-fields"),
        )
        primary_contact = supplier.get("primary-contact")
        if primary_contact:
            invoice.supplier.primary_contact = CoupaInvoiceSupplierContact(
                id=primary_contact["id"],
                created_at=primary_contact.get("created-at", ""),
                updated_at=primary_contact.get("updated-at", ""),
                email=primary_contact.get("email"),
                name_prefix=primary_contact.get("name-prefix"),
                name_suffix=primary_contact.get("name-suffix"),
                name_additional=primary_contact.get("name-additional"),
                name_given=primary_contact.get("name-given"),
                name_family=primary_contact.get("name-family"),
                name_fullname=primary_contact.get("name-fullname"),
                notes=primary_contact.get("notes"),
                active=primary_contact.get("active"),
                business_group_name=primary_contact.get("business-group-name"),
                vat_number=primary_contact.get("vat-number"),
                local_tax_number=primary_contact.get("local-tax-number"),
                type=primary_contact.get("type"),
            )
            # person1 = primary_contact.get("created-by")
            # if person1:
            #     invoice.supplier.primary_contact.created_by = CoupaInvoicePerson(
            #         id=person1["id"],
            #         login=person1.get("login"),
            #         email=person1.get("email"),
            #         employee_number=person1.get("employee-number"),
            #         firstname=person1.get("firstname"),
            #         lastname=person1.get("lastname"),
            #         fullname=person1.get("fullname"),
            #         salesforce_id=person1.get("salesforce-id"),
            #         avatar_thumb_url=person1.get("avatar-thumb-url"),
            #         assignee=person1.get("assignee"),
            #     )
            # person2 = primary_contact.get("updated-by")
            # if person2:
            #     invoice.supplier.primary_contact.updated_by = CoupaInvoicePerson(
            #         id=person2["id"],
            #         login=person2.get("login"),
            #         email=person2.get("email"),
            #         employee_number=person2.get("employee-number"),
            #         firstname=person2.get("firstname"),
            #         lastname=person2.get("lastname"),
            #         fullname=person2.get("fullname"),
            #         salesforce_id=person2.get("salesforce-id"),
            #         avatar_thumb_url=person2.get("avatar-thumb-url"),
            #         assignee=person2.get("assignee"),
            #     )
        primary_address = supplier.get("primary-address")
        if primary_address:
            invoice.supplier.primary_address = CoupaInvoiceAddress(
                id=primary_address["id"],
                created_at=primary_address.get("created-at", ""),
                updated_at=primary_address.get("updated-at", ""),
                name=primary_address.get("name"),
                location_code=primary_address.get("location-code"),
                street1=primary_address.get("street1"),
                street2=primary_address.get("street2"),
                street3=primary_address.get("street3"),
                street4=primary_address.get("street4"),
                city=primary_address.get("city"),
                state=primary_address.get("state"),
                postal_code=primary_address.get("postal-code"),
                attention=primary_address.get("attention"),
                active=primary_address.get("active"),
                business_group_name=primary_address.get("business-group-name"),
                vat_number=primary_address.get("vat-number"),
                local_tax_number=primary_address.get("local-tax-number"),
                type=primary_address.get("type"),
                address_type=primary_address.get("address-type"),
                default=primary_address.get("default"),
                custom_fields=primary_address.get("custom-fields"),
            )
    currency = response.get("currency")
    if currency:
        invoice.currency = CoupaInvoiceCurrency(
            id=currency["id"],
            code=currency.get("code"),
            decimals=currency.get("decimals"),
        )
        # updated_by = currency.get("updated-by")
        # if updated_by:
        #     invoice.currency.updated_by = CoupaInvoicePerson(
        #         id=updated_by["id"],
        #         login=updated_by.get("login"),  # pylint: disable=too-many-nested-blocks
        #         email=updated_by.get("email"),
        #         employee_number=updated_by.get("employee-number"),
        #         firstname=updated_by.get("firstname"),
        #         lastname=updated_by.get("lastname"),
        #         fullname=updated_by.get("fullname"),
        #         salesforce_id=updated_by.get("salesforce-id"),
        #         avatar_thumb_url=updated_by.get("avatar-thumb-url"),
        #         assignee=updated_by.get("assignee"),
        #     )
    payment_term = response.get("payment-term")
    if payment_term:
        invoice.payment_term = CoupaInvoicePaymentTerm(
            id=payment_term["id"],
            created_at=payment_term.get("created-at", ""),
            updated_at=payment_term.get("updated-at", ""),
            code=payment_term.get("code"),
            description=payment_term.get("description"),
            days_for_net_payment=payment_term.get("days-for-net-payment"),
            days_for_discount_payment=payment_term.get("days-for-discount-payment"),
            discount_rate=payment_term.get("discount-rate"),
            active=payment_term.get("active"),
            type=payment_term.get("type"),
            net_cutoff_day=payment_term.get("net-cutoff-day"),
            net_due_month=payment_term.get("net-due-month"),
            net_due_day=payment_term.get("net-due-day"),
            discount_cutoff_day=payment_term.get("discount-cutoff-day"),
            discount_due_month=payment_term.get("discount-due-month"),
            discount_due_day=payment_term.get("discount-due-day"),
            # content_groups=payment_term.get("content-groups"),
            remit_to_address=payment_term.get("remit-to-address"),
        )
        # updated_by = payment_term.get("updated-by")
        # if updated_by:
        #     invoice.payment_term.updated_by = CoupaInvoicePerson(
        #         id=updated_by["id"],
        #         login=updated_by.get("login"),  # pylint: disable=too-many-nested-blocks
        #         email=updated_by.get("email"),
        #         employee_number=updated_by.get("employee-number"),
        #         firstname=updated_by.get("firstname"),
        #         lastname=updated_by.get("lastname"),
        #         fullname=updated_by.get("fullname"),
        #         salesforce_id=updated_by.get("salesforce-id"),
        #         avatar_thumb_url=updated_by.get("avatar-thumb-url"),
        #         assignee=updated_by.get("assignee"),
        #     )
    remit_to_address = response.get("remit-to-address")
    if remit_to_address:
        invoice.remit_to_address = CoupaInvoiceAddress(
            id=remit_to_address["id"],
            created_at=remit_to_address.get("created-at", ""),
            updated_at=remit_to_address.get("updated-at", ""),
            name=remit_to_address.get("name"),
            location_code=remit_to_address.get("location-code"),
            street1=remit_to_address.get("street1"),
            street2=remit_to_address.get("street2"),
            street3=remit_to_address.get("street3"),
            street4=remit_to_address.get("street4"),
            city=remit_to_address.get("city"),
            state=remit_to_address.get("state"),
            postal_code=remit_to_address.get("postal-code"),
            attention=remit_to_address.get("attention"),
            active=remit_to_address.get("active"),
            business_group_name=remit_to_address.get("business-group-name"),
            vat_number=remit_to_address.get("vat-number"),
            local_tax_number=remit_to_address.get("local-tax-number"),
            type=remit_to_address.get("type"),
            address_type=remit_to_address.get("address-type"),
            default=remit_to_address.get("default"),
            custom_fields=remit_to_address.get("custom-fields"),
        )
        country = remit_to_address.get("country")
        if country:
            invoice.remit_to_address.country = CoupaInvoiceCountry(
                id=country["id"],
                code=country.get("code"),
                name=country.get("name"),
            )
    invoice_lines = response.get("invoice-lines")
    if invoice_lines:  # pylint: disable=too-many-nested-blocks
        for invoice_line in invoice_lines:
            invoice_line_instance = CoupaInvoiceLine(
                invoice_line["id"],
                account_allocations=invoice_line.get("account-allocations"),
                created_at=invoice_line.get("created-at", ""),
                updated_at=invoice_line.get("updated-at", ""),
                accounting_total=invoice_line.get("accounting-total"),
                description=invoice_line.get("description"),
                line_num=invoice_line.get("line-num"),
                order_header_num=invoice_line.get("order-header-num"),
                po_number=invoice_line.get("po-number"),
                order_line_id=invoice_line.get("order-line-id"),
                order_line_num=invoice_line.get("order-line-num"),
                price=invoice_line.get("price"),
                net_weight=invoice_line.get("net-weight"),
                price_per_uom=invoice_line.get("price-per-uom"),
                quantity=invoice_line.get("quantity"),
                adjustment_type=invoice_line.get("adjustment-type"),
                status=invoice_line.get("status"),
                tax_rate=invoice_line.get("tax-rate"),
                tax_location=invoice_line.get("tax-location"),
                tax_amount=invoice_line.get("tax-amount"),
                tax_description=invoice_line.get("tax-description"),
                tax_supply_date=invoice_line.get("tax-supply-date"),
                total=invoice_line.get("total"),
                type=invoice_line.get("type"),
                tax_amount_engine=invoice_line.get("tax-amount-engine"),
                tax_code_engine=invoice_line.get("tax-code-engine"),
                tax_rate_engine=invoice_line.get("tax-rate-engine"),
                tax_distribution_total=invoice_line.get("tax-distribution-total"),
                shipping_distribution_total=invoice_line.get("shipping-distribution-total"),
                handling_distribution_total=invoice_line.get("handling-distribution-total"),
                misc_distribution_total=invoice_line.get("misc-distribution-total"),
                match_reference=invoice_line.get("match-reference"),
                original_date_of_supply=invoice_line.get("original-date-of-supply"),
                delivery_note_number=invoice_line.get("delivery-note-number"),
                discount_amount=invoice_line.get("discount-amount"),
                company_uom=invoice_line.get("company-uom"),
                property_tax_account=invoice_line.get("property-tax-account"),
                source_part_num=invoice_line.get("source-part-num"),
                supp_aux_part_num=invoice_line.get("supp-aux-part-num"),
                customs_declaration_number=invoice_line.get("customs-declaration-number"),
                hsn_sac_code=invoice_line.get("hsn-sac-code"),
                unspsc=invoice_line.get("unspsc"),
                billing_note=invoice_line.get("billing-note"),
                fiscal_code=invoice_line.get("fiscal-code"),
                classification_of_goods=invoice_line.get("classification-of-goods"),
                municipality_taxation_code=invoice_line.get("municipality-taxation-code"),
                item_barcode=invoice_line.get("item-barcode"),
                category=invoice_line.get("category"),
                subcategory=invoice_line.get("subcategory"),
                deductibility=invoice_line.get("deductibility"),
                custom_fields=invoice_line.get("custom-fields"),
                order_line_commodity=invoice_line.get("order-line-commodity"),
                order_line_custom_fields=invoice_line.get("order-line-custom-fields"),
                period=invoice_line.get("period"),
                contract=invoice_line.get("contract"),
                tax_lines=invoice_line.get("tax-lines"),
                withholding_tax_lines=invoice_line.get("withholding-tax-lines"),
                tags=invoice_line.get("tags"),
                taggings=invoice_line.get("taggings"),
                failed_tolerances=invoice_line.get("failed-tolerances"),
            )
            account = invoice_line.get("account")
            if account:
                invoice_line_instance.account = CoupaInvoiceAccount(
                    account["id"],
                    created_at=account.get("created-at", ""),
                    updated_at=account.get("updated-at", ""),
                    name=account.get("name"),
                    code=account.get("code"),
                    active=account.get("active"),
                    account_type_id=account.get("account-type-id"),
                    # segment_1=account.get("segment-1"),
                    # segment_2=account.get("segment-2"),
                    # segment_3=account.get("segment-3"),
                    # segment_4=account.get("segment-4"),
                    # segment_5=account.get("segment-5"),
                    # segment_6=account.get("segment-6"),
                    # segment_7=account.get("segment-7"),
                    # segment_8=account.get("segment-8"),
                    # segment_9=account.get("segment-9"),
                    # segment_10=account.get("segment-10"),
                    # segment_11=account.get("segment-11"),
                    # segment_12=account.get("segment-12"),
                    # segment_13=account.get("segment-13"),
                    # segment_14=account.get("segment-14"),
                    # segment_15=account.get("segment-15"),
                    # segment_16=account.get("segment-16"),
                    # segment_17=account.get("segment-17"),
                    # segment_18=account.get("segment-18"),
                    # segment_19=account.get("segment-19"),
                    # segment_20=account.get("segment-20"),
                )
                account_type = account.get("account-type")
                if account_type:
                    invoice_line_instance.account.account_type = CoupaInvoiceAccountType(
                        account_type["id"],
                        created_at=account_type.get("created-at", ""),
                        updated_at=account_type.get("updated-at", ""),
                        name=account_type.get("name"),
                        active=account_type.get("active"),
                        legal_entity_name=account_type.get("legal-entity-name"),
                        dynamic_flag=account_type.get("dynamic-flag"),
                    )
                    currency = account_type.get("currency")
                    if currency:
                        invoice_line_instance.account.account_type.currency = CoupaInvoiceCurrency(
                            id=currency["id"],
                            code=currency.get("code"),
                            decimals=currency.get("decimals"),
                        )
                        # updated_by = currency.get("updated-by")
                        # if updated_by:
                        #     invoice_line_instance.account.account_type.updated_by = (
                        #         CoupaInvoicePerson(
                        #             id=updated_by["id"],
                        #             login=updated_by.get("login"),
                        #             email=updated_by.get("email"),
                        #             employee_number=updated_by.get("employee-number"),
                        #             firstname=updated_by.get("firstname"),
                        #             lastname=updated_by.get("lastname"),
                        #             fullname=updated_by.get("fullname"),
                        #             salesforce_id=updated_by.get("salesforce-id"),
                        #             avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                        #             assignee=updated_by.get("assignee"),
                        #         )
                        #     )
                    primary_address = account_type.get("primary_address")
                    if primary_address:
                        invoice_line_instance.account.account_type.primary_address = (
                            CoupaInvoiceAddress(
                                id=primary_address["id"],
                                created_at=primary_address.get("created-at", ""),
                                updated_at=primary_address.get("updated-at", ""),
                                name=primary_address.get("name"),
                                location_code=primary_address.get("location-code"),
                                street1=primary_address.get("street1"),
                                street2=primary_address.get("street2"),
                                street3=primary_address.get("street3"),
                                street4=primary_address.get("street4"),
                                city=primary_address.get("city"),
                                state=primary_address.get("state"),
                                postal_code=primary_address.get("postal-code"),
                                attention=primary_address.get("attention"),
                                active=primary_address.get("active"),
                                business_group_name=primary_address.get("business-group-name"),
                                vat_number=primary_address.get("vat-number"),
                                local_tax_number=primary_address.get("local-tax-number"),
                                type=primary_address.get("type"),
                                address_type=primary_address.get("address-type"),
                                default=primary_address.get("default"),
                                custom_fields=primary_address.get("custom-fields"),
                            )
                        )
                    # person1 = account_type.get("created-by")
                    # if person1:
                    #     invoice_line_instance.account.account_type.created_by = CoupaInvoicePerson(
                    #         id=person1["id"],
                    #         login=person1.get("login"),
                    #         email=person1.get("email"),
                    #         employee_number=person1.get("employee-number"),
                    #         firstname=person1.get("firstname"),
                    #         lastname=person1.get("lastname"),
                    #         fullname=person1.get("fullname"),
                    #         salesforce_id=person1.get("salesforce-id"),
                    #         avatar_thumb_url=person1.get("avatar-thumb-url"),
                    #         assignee=person1.get("assignee"),
                    #     )
                    # person2 = account_type.get("updated-by")
                    # if person2:
                    #     invoice_line_instance.account.account_type.updated_by = CoupaInvoicePerson(
                    #         id=person2["id"],
                    #         login=person2.get("login"),
                    #         email=person2.get("email"),
                    #         employee_number=person2.get("employee-number"),
                    #         firstname=person2.get("firstname"),
                    #         lastname=person2.get("lastname"),
                    #         fullname=person2.get("fullname"),
                    #         salesforce_id=person2.get("salesforce-id"),
                    #         avatar_thumb_url=person2.get("avatar-thumb-url"),
                    #         assignee=person2.get("assignee"),
                    #     )
                # person1 = account.get("created-by")
                # if person1:
                #     invoice_line_instance.account.created_by = CoupaInvoicePerson(
                #         id=person1["id"],
                #         login=person1.get("login"),
                #         email=person1.get("email"),
                #         employee_number=person1.get("employee-number"),
                #         firstname=person1.get("firstname"),
                #         lastname=person1.get("lastname"),
                #         fullname=person1.get("fullname"),
                #         salesforce_id=person1.get("salesforce-id"),
                #         avatar_thumb_url=person1.get("avatar-thumb-url"),
                #         assignee=person1.get("assignee"),
                #     )
                # person2 = account.get("updated-by")
                # if person2:
                #     invoice_line_instance.account.updated_by = CoupaInvoicePerson(
                #         id=person2["id"],
                #         login=person2.get("login"),
                #         email=person2.get("email"),
                #         employee_number=person2.get("employee-number"),
                #         firstname=person2.get("firstname"),
                #         lastname=person2.get("lastname"),
                #         fullname=person2.get("fullname"),
                #         salesforce_id=person2.get("salesforce-id"),
                #         avatar_thumb_url=person2.get("avatar-thumb-url"),
                #         assignee=person2.get("assignee"),
                #     )
            commodity = invoice_line.get("commodity")
            if commodity:
                invoice_line_instance.commodity = CoupaInvoiceCommodity(
                    commodity["id"],
                    created_at=commodity.get("created-at", ""),
                    updated_at=commodity.get("updated-at", ""),
                    active=commodity.get("active"),
                    name=commodity.get("name"),
                    translated_name=commodity.get("translated-name"),
                    deductibility=commodity.get("deductibility"),
                    category=commodity.get("category"),
                    subcategory=commodity.get("subcategory"),
                    imported_from_taxonomy=commodity.get("imported-from-taxonomy"),
                    gl=commodity.get("gl"),
                    common_gl_acct=commodity.get("common-gl-acct"),
                    parent=commodity.get("parent"),
                )
                # person1 = commodity.get("created-by")
                # if person1:
                #     invoice_line_instance.commodity.created_by = CoupaInvoicePerson(
                #         id=person1["id"],
                #         login=person1.get("login"),
                #         email=person1.get("email"),
                #         employee_number=person1.get("employee-number"),
                #         firstname=person1.get("firstname"),
                #         lastname=person1.get("lastname"),
                #         fullname=person1.get("fullname"),
                #         salesforce_id=person1.get("salesforce-id"),
                #         avatar_thumb_url=person1.get("avatar-thumb-url"),
                #         assignee=person1.get("assignee"),
                #     )
                # person2 = commodity.get("updated-by")
                # if person2:
                #     invoice_line_instance.commodity.updated_by = CoupaInvoicePerson(
                #         id=person2["id"],
                #         login=person2.get("login"),
                #         email=person2.get("email"),
                #         employee_number=person2.get("employee-number"),
                #         firstname=person2.get("firstname"),
                #         lastname=person2.get("lastname"),
                #         fullname=person2.get("fullname"),
                #         salesforce_id=person2.get("salesforce-id"),
                #         avatar_thumb_url=person2.get("avatar-thumb-url"),
                #         assignee=person2.get("assignee"),
                #     )
            # person1 = invoice_line.get("created-by")
            # if person1:
            #     invoice_line_instance.created_by = CoupaInvoicePerson(
            #         id=person1["id"],
            #         login=person1.get("login"),
            #         email=person1.get("email"),
            #         employee_number=person1.get("employee-number"),
            #         firstname=person1.get("firstname"),
            #         lastname=person1.get("lastname"),
            #         fullname=person1.get("fullname"),
            #         salesforce_id=person1.get("salesforce-id"),
            #         avatar_thumb_url=person1.get("avatar-thumb-url"),
            #         assignee=person1.get("assignee"),
            #     )
            # person2 = invoice_line.get("updated-by")
            # if person2:
            #     invoice_line_instance.updated_by = CoupaInvoicePerson(
            #         id=person2["id"],
            #         login=person2.get("login"),
            #         email=person2.get("email"),
            #         employee_number=person2.get("employee-number"),
            #         firstname=person2.get("firstname"),
            #         lastname=person2.get("lastname"),
            #         fullname=person2.get("fullname"),
            #         salesforce_id=person2.get("salesforce-id"),
            #         avatar_thumb_url=person2.get("avatar-thumb-url"),
            #         assignee=person2.get("assignee"),
            #     )
            item = invoice_line.get("item")
            if item:
                invoice_line_instance.item = CoupaInvoiceItem(
                    id=item["id"],
                    created_at=item.get("created-at", ""),
                    updated_at=item.get("updated-at", ""),
                    description=item.get("description"),
                    item_number=item.get("item-number"),
                    name=item.get("name"),
                    active=item.get("active"),
                    storage_quantity=item.get("storage-quantity"),
                    image_url=item.get("image-url"),
                    manufacturer_name=item.get("manufacturer-name"),
                    manufacturer_part_number=item.get("manufacturer-part-number"),
                    item_type=item.get("item-type"),
                    pack_qty=item.get("pack-qty"),
                    pack_weight=item.get("pack-weight"),
                    pack_uom_idy=item.get("pack-uom-idy"),
                    receive_catch_weight=item.get("receive-catch-weight"),
                    allow_partial_quantity=item.get("allow-partial-quantity"),
                    inventory_lot_tracking_enabled=item.get("inventory-lot-tracking-enabled"),
                    inventory_lot_expiration_type=item.get("inventory-lot-expiration-type"),
                )
                commodity = item.get("commodity")
                if commodity:
                    invoice_line_instance.item.commodity = CoupaInvoiceCommodity(
                        commodity["id"],
                        created_at=commodity.get("created-at", ""),
                        updated_at=commodity.get("updated-at", ""),
                        active=commodity.get("active"),
                        name=commodity.get("name"),
                        translated_name=commodity.get("translated-name"),
                        deductibility=commodity.get("deductibility"),
                        category=commodity.get("category"),
                        subcategory=commodity.get("subcategory"),
                        imported_from_taxonomy=commodity.get("imported-from-taxonomy"),
                        gl=commodity.get("gl"),
                        common_gl_acct=commodity.get("common-gl-acct"),
                        parent=commodity.get("parent"),
                    )
                    # person1 = commodity.get("created-by")
                    # if person1:
                    #     invoice_line_instance.item.commodity.created_by = CoupaInvoicePerson(
                    #         id=person1["id"],
                    #         login=person1.get("login"),
                    #         email=person1.get("email"),
                    #         employee_number=person1.get("employee-number"),
                    #         firstname=person1.get("firstname"),
                    #         lastname=person1.get("lastname"),
                    #         fullname=person1.get("fullname"),
                    #         salesforce_id=person1.get("salesforce-id"),
                    #         avatar_thumb_url=person1.get("avatar-thumb-url"),
                    #         assignee=person1.get("assignee"),
                    #     )
                    # person2 = commodity.get("updated-by")
                    # if person2:
                    #     invoice_line_instance.item.commodity.updated_by = CoupaInvoicePerson(
                    #         id=person2["id"],
                    #         login=person2.get("login"),
                    #         email=person2.get("email"),
                    #         employee_number=person2.get("employee-number"),
                    #         firstname=person2.get("firstname"),
                    #         lastname=person2.get("lastname"),
                    #         fullname=person2.get("fullname"),
                    #         salesforce_id=person2.get("salesforce-id"),
                    #         avatar_thumb_url=person2.get("avatar-thumb-url"),
                    #         assignee=person2.get("assignee"),
                    #     )
            uom = invoice_line.get("uom")
            if uom:
                invoice_line_instance.uom = CoupaInvoiceUOM(
                    id=uom["id"],
                    created_at=uom.get("created-at", ""),
                    updated_at=uom.get("updated-at", ""),
                    code=uom.get("code"),
                    name=uom.get("name"),
                    allowable_precision=uom.get("allowable-precision"),
                    active=uom.get("active"),
                )
                # updated_by = uom.get("updated-by")
                # if updated_by:
                #     invoice_line_instance.uom.updated_by = CoupaInvoicePerson(
                #         id=updated_by["id"],
                #         login=updated_by.get("login"),
                #         email=updated_by.get("email"),
                #         employee_number=updated_by.get("employee-number"),
                #         firstname=updated_by.get("firstname"),
                #         lastname=updated_by.get("lastname"),
                #         fullname=updated_by.get("fullname"),
                #         salesforce_id=updated_by.get("salesforce-id"),
                #         avatar_thumb_url=updated_by.get("avatar-thumb-url"),
                #         assignee=updated_by.get("assignee"),
                #     )
            invoice.invoice_lines.append(invoice_line_instance)
        currency = response.get("currency")
        if currency:
            invoice.currency = CoupaInvoiceCurrency(
                id=currency["id"],
                code=currency.get("code"),
                decimals=currency.get("decimals"),
            )
            # updated_by = currency.get("updated-by")
            # if updated_by:
            #     invoice.currency.updated_by = CoupaInvoicePerson(
            #         id=updated_by["id"],
            #         login=updated_by.get("login"),
            #         email=updated_by.get("email"),
            #         employee_number=updated_by.get("employee-number"),
            #         firstname=updated_by.get("firstname"),
            #         lastname=updated_by.get("lastname"),
            #         fullname=updated_by.get("fullname"),
            #         salesforce_id=updated_by.get("salesforce-id"),
            #         avatar_thumb_url=updated_by.get("avatar-thumb-url"),
            #         assignee=updated_by.get("assignee"),
            #     )
    return invoice


def coupa_build_receipt_header_from_response(response: Dict[str, Any]) -> CoupaReceiptHeader:
    """
    Utility function to build a receipt header given a receipt response object.

    Args:
        response: Receipt JSON response.

    Returns:
        Coupa Receipt header object
    """

    receipt_header = CoupaReceiptHeader(
        id=response["id"],
        created_by=response["created-by"]["login"],
        created_at=response.get("created-at", ""),
        updated_at=response.get("updated-at", ""),
        price=response.get("price"),
        quantity=response.get("quantity"),
        total=response.get("total"),
        transaction_date=response.get("transaction-date"),
        type=response.get("type"),
        status=response.get("status"),
    )

    order_line = response.get("order-line")
    if order_line:
        receipt_header.order_line = CoupaOrderLine(
            order_line_id=order_line.get("id", 0),
            order_line_description=order_line.get("description", ""),
            order_line_type=order_line.get("type", ""),
            order_line_num=order_line.get("line-num", ""),
            item_description=order_line.get("item", {}).get("description", None),
            quantity=order_line.get("quantity", None),
            unit=order_line.get("item", {}).get("uom", {}).get("name", None),
            price=order_line.get("price", ""),
            total=order_line.get("total", ""),
            account_id=order_line.get("account", {}).get("id", 0),
            account_type_id=order_line.get("account", {}).get("account-type", {}).get("id", 0),
            uom_code=order_line.get("uom", {}).get("code", ""),
            estimated_tax_amount=order_line.get("estimated-tax-amount", ""),
            total_with_estimated_tax=order_line.get("total-with-estimated-tax", ""),
            amount_received=order_line.get("received", 0),
            supplier_part_number=order_line.get("source-part-num", ""),
            supplier_auxiliary_part_number=order_line.get("supp-aux-part-num", ""),
            commodity=order_line.get("commodity", {}).get("name"),
            manufacturer_name=order_line.get("manufacturer-name", ""),
            manufacturer_part_number=order_line.get("manufacturer-part-number", ""),
            receipt_approval_required=order_line.get("receipt-approval-required", False),
            need_by_date=order_line.get("need-by-date", None),
            savings_percent=order_line.get("savings-pct", ""),
            billing_account_id=order_line.get("account", {}).get("id"),
            period=order_line.get("period", {}).get("name"),
        )
        receipt_header.purchase_order_id = order_line.get("order-header-id", 0)

    uom = response.get("uom")
    if uom:
        receipt_header.uom = CoupaInvoiceUOM(
            id=uom["id"],
            created_at=uom.get("created-at", ""),
            updated_at=uom.get("updated-at", ""),
            code=uom.get("code"),
            name=uom.get("name"),
            allowable_precision=uom.get("allowable_precision"),
            active=uom.get("active"),
        )

    account = response.get("account")
    if account:
        receipt_header.account = CoupaInvoiceAccount(
            id=account["id"],
            created_at=account.get("created-at", ""),
            updated_at=account.get("updated-at", ""),
            name=account.get("name"),
            code=account.get("code"),
            active=account.get("active"),
            account_type_id=account.get("account-type-id"),
        )

    item = response.get("item")
    if item:
        receipt_header.item = CoupaInvoiceItem(
            id=item["id"],
            created_at=item.get("created-at", ""),
            updated_at=item.get("updated-at", ""),
            description=item.get("description"),
            item_number=item.get("item-number"),
            name=item.get("name"),
            active=item.get("active"),
            storage_quantity=item.get("storage-quantity"),
            image_url=item.get("image-url"),
            manufacturer_name=item.get("manufacturer-name"),
            manufacturer_part_number=item.get("manufacturer-part-number"),
            item_type=item.get("item-type"),
            pack_qty=item.get("pack-qty"),
            pack_weight=item.get("pack-weight"),
            pack_uom_idy=item.get("pack-uom-idy"),
            receive_catch_weight=item.get("receive-catch-weight"),
            allow_partial_quantity=item.get("allow-partial-quantity"),
            inventory_lot_tracking_enabled=item.get("inventory-lot-tracking_enabled"),
            inventory_lot_expiration_type=item.get("inventory-lot-expiration_type"),
        )

    return receipt_header
