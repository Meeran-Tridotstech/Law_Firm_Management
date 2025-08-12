# Copyright (c) 2025, Meeran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class ClientConsultation(Document):

    def validate(self):
        # 1. Validate Client Name
        if not self.client_name or len(self.client_name.strip()) < 3:
            frappe.throw("Client Name must be at least 3 characters long.")

        if self.consultation_fee is not None and self.consultation_fee < 0:
            frappe.throw("Consultation Fee cannot be negative.")

        if self.consultation_fee and not self.payment_status:
            frappe.throw("Please set Payment Status if there is a Consultation Fee.")

        if not self.advocate:
            frappe.throw("Advocate must be selected for the consultation.")

        if not self.consult_date_1:
            frappe.throw("Consult Date 1 is required.")

        if self.consult_date_2 and getdate(self.consult_date_2) < getdate(self.consult_date_1):
            frappe.throw("Consult Date 2 cannot be earlier than Consult Date 1.")

        if self.consult_date_1 and getdate(self.consult_date_1) > getdate(today()):
            self.status = "Scheduled"
        elif self.consult_date_1 and getdate(self.consult_date_1) <= getdate(today()):
            self.status = "Completed"

    def after_insert(self):
        # Get advocate's email from Advocate doctype
        advocate_email = frappe.db.get_value("Advocate", self.advocate, "email")

        if not advocate_email:
            frappe.throw("No email found for the selected advocate.")

        # Send email
        frappe.sendmail(
            recipients=[advocate_email],
            subject="New Client Consultation",
            message=f"A new consultation has been created for client: {self.client_name}."
        )

        # If this email is also a valid User in Frappe, send notification
        if frappe.db.exists("User", advocate_email):
            frappe.publish_realtime(
                event="msgprint",
                message=f"New consultation for {self.client_name}",
                user=advocate_email
            )