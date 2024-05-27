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
        
        self.validate_dates()
        self.validate_banquet()            
        self.calculate_totals()
        
        if self.grand_total <= 0:
            frappe.throw(_('Grand Total should be greater than zero'))
        
    
    def calculate_totals(self):
        total_per_person = 0
        for item in self.selected_menu:
            item.amount = item.qty * item.price
            total_per_person += item.amount
            
        self.total_per_person = total_per_person
        self.grand_total = self.total_per_person * cint(self.expected_persons)
        self.total_in_words = money_in_words(self.grand_total)

    def validate_banquet(self):
        query = """
            SELECT COUNT(*) 
            FROM `tabBanquet Booking` 
            WHERE docstatus = 1
            AND visitor = %(visitor)s
            AND banquet = %(banquet)s 
            AND event_from >= %(event_from)s 
            AND event_to <= %(event_to)s;
        """
        params = {
            'visitor': self.visitor,
            'banquet': self.banquet,
            'event_from': self.event_from,
            'event_to': self.event_to
        }
        banquet_count = frappe.db.sql(query, params)[0][0]
        if banquet_count > 0:
            frappe.throw(_(f'Banquet {self.banquet} is already booked between provided dates'))

    def validate_dates(self):
        if self.event_from > self.event_to:
            frappe.throw(_('Event From date should not be less than Event To.'))