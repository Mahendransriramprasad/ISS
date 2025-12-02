import frappe
from frappe.model.document import Document

class BudgetEntry(Document):
    def validate(self):
        # Budget percent cannot exceed 100
        if self.budget_percent and self.budget_percent > 100:
            frappe.throw("Budget percent cannot exceed 100%.")
