# Copyright (c) 2025, Meeran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class Advocate(Document):
	def before_save(self):
		#Full Name Validation:
		#---------------------
		if len(self.full_name)<3:
			frappe.throw("Full name is Minimum 3 Charecters")
		#Email Validation:
		#-----------------
		if self.email:
			mail = self.email.strip()
			pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
			if not re.match(pattern, mail):
				frappe.throw("Enter a valid email address")
		#Phone Number Validation:
		#------------------------
		if self.phone_number:
			mobile = self.phone_number.strip()
			if mobile.startswith("+91"):
				mobile = mobile[3:]
			mobile = mobile.replace(" ","").replace("-","")
			if not re.match(r"^[6-9]\d{9}$",mobile):
				frappe.throw("Enter a valid 10-digit Indian mobile number")
		#Bar Council Validation:
		#-----------------------
		if self.bar_registration_no:
			pattern = r"^(MS|TN)/\d{1,5}/\d{4}$"
			if not re.match(pattern, self.bar_registration_no.strip(), re.IGNORECASE):
				frappe.throw("Invalid Tamil Nadu Bar Council Number format. Example: TN/1234/2025")