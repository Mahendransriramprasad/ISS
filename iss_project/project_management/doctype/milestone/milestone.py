import frappe
from frappe.model.document import Document

class Milestone(Document):
    def validate(self):
        # When milestone is completed, calculate extension count
        if self.actual_date and self.planned_date:
            if self.actual_date > self.planned_date:
                self.extension_count = (self.extension_count or 0) + 1

