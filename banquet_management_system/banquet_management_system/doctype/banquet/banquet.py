# Copyright (c) 2024, Ali Raza and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class Banquet(Document):
    
    def validate(self):
        if frappe.db.count('Item', {'item_code': self.banquet_name}) > 0:
            frappe.throw(_('Item with this banquet is already exists.'))
            
    
    def after_insert(self):
        doc = frappe.get_doc({
			'doctype': 'Item',
			'item_code': self.banquet_name,
			'item_name': self.banquet_name,
			'item_group': 'Services'
		})
        doc.insert(ignore_permissions=True)