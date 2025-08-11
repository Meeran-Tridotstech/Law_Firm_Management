# Copyright (c) 2025, Meeran and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document

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
        if self.consult_date_2 and self.consult_date_2 < self.consult_date_1:
            frappe.throw("Consult Date 2 cannot be earlier than Consult Date 1.")

        if self.consult_date_1 and self.consult_date_1 > frappe.utils.today():
            self.status = "Scheduled"
        elif self.consult_date_1 and self.consult_date_1 <= frappe.utils.today():
            self.status = "Completed"
    
	