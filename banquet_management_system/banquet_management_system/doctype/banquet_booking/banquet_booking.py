# Copyright (c) 2024, Ali Raza and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import money_in_words, cint, now

class BanquetBooking(Document):
    def validate(self):
        self.posting_datetime = now()
        if not self.selected_menu:
            frappe.throw(_('Please select menu items to proceed to save'))
            
        self.calculate_totals()
        
        if self.grand_total <= 0:
            frappe.throw(_('Grand Total should be greater than zero'))
        
    
    def calculate_totals(self):
        grand_total = 0
        for item in self.selected_menu:
            item.amount = item.qty * item.price
            grand_total += item.amount
            
        self.grand_total = grand_total
        self.total_in_words = money_in_words(self.grand_total)
