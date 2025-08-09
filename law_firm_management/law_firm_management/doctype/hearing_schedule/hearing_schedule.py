# Copyright (c) 2025, Meeran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HearingSchedule(Document):
    def before_save(self):
        if not self.case:
            frappe.throw("Please select a Legal Case.")

        if self.status != "Completed" and self.hearing_date < frappe.utils.today():
            frappe.throw("Hearing date cannot be in the past unless the status is 'Completed'.")

        valid_status = ["Pending", "Completed", "Adjourned"]
        if self.status not in valid_status:
            frappe.throw(f"Status must be one of: {','.join(valid_status)}")