# Copyright (c) 2024, Ali Raza and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class Visitor(Document):
    
    def validate(self):
        exists = frappe.db.exists('Customer', self.phone_no)
        if exists:
            frappe.throw(_('A Visitor with this phone number already exists'))
            
        setting = frappe.db.get_single_value('Selling Settings','cust_master_name')
        if setting != "Auto Name":
            frappe.throw(_(f"Please set Customer Naming By to 'Auto Name' in Selling Settings first."))

    def after_insert(self):            
        if not frappe.db.exists('Customer', self.phone_no):
            customer = frappe.get_doc({
                'doctype': 'Customer',
                'name': self.phone_no,
                'customer_name': self.customer_name,
                'customer_type': 'Individual',
            })
            customer.insert(ignore_permissions=True)