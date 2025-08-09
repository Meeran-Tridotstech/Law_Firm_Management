# Copyright (c) 2025, Meeran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class ClientBilling(Document):
    def before_insert(self):
        # Auto-generate invoice number
        last_invoice = frappe.db.get_value("Client Billing", {}, "invoice_no", order_by="creation desc")
        if last_invoice:
            last_num = int(last_invoice.split("-")[-1])
            self.invoice_no = f"INV-{last_num + 1:04d}"
        else:
            self.invoice_no = "INV-0001"

        # Default date
        if not self.billing_date:
            self.billing_date = nowdate()

    def validate(self):
        # Amount validation
        if self.amount <= 0:
            frappe.throw("Amount must be greater than zero.")

        # Auto calculate total with tax
        tax_percent = self.tax_percent or 0
        self.total_amount = self.amount + (self.amount * tax_percent / 100)

        # Status validation
        valid_status = ["Draft", "Paid", "Overdue"]
        if self.status not in valid_status:
            frappe.throw(f"Status must be one of: {', '.join(valid_status)}")

