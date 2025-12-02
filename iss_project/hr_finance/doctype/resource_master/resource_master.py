import frappe
from frappe.model.document import Document

class ResourceMaster(Document):
    def validate(self):
        # sync full name
        if self.user:
            self.full_name = frappe.db.get_value("User", self.user, "full_name")
