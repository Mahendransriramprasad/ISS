import frappe
from frappe.model.document import Document

class TimesheetEntry(Document):
    def validate(self):
        if self.hours <= 0:
            frappe.throw("Hours must be greater than 0")

        if self.status not in ["Pending Approval", "Approved", "Rejected"]:
            frappe.throw("Invalid status")

    def on_submit(self):
        pass
