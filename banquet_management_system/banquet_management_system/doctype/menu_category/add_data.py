import frappe
from frappe import _
import os
import json


def add_categories():
    json_file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_file_path, 'r') as file:
        data = json.load(file) 
        
    for d in data:
        if not frappe.db.exists('Menu Category', _(d.get("name"))):
            doc = frappe.get_doc('Menu Category', )
            doc.insert(ignore_permission=True)