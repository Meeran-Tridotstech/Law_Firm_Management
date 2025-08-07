# Copyright (c) 2025, Meeran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class Client(Document):
	def before_save(self):
		if len(self.client_name)<3:
			frappe.throw("More than 3 Charecter...")
		if self.phone_number:
			mobile = self.phone_number.strip()
			if mobile.startswith("+91"):
				mobile = mobile[3:]
			mobile = mobile.replace(" ","").replace("-","")
			if not re.match(r"^[6-9]\d{9}$",mobile):
				frappe.throw("Enter a valid 10-digit Indian mobile number")
		if self.email:
			email = self.email.strip()
			pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
			if not re.match(pattern, email):
				frappe.throw("Enter a valid email address")