from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Task(Document):
    def before_insert(self):
        if not self.task_id:
            from frappe.model.naming import make_autoname
            self.task_id = make_autoname("TASK-.####")

    def validate(self):
        # developer-created tasks requiring approval can be flagged; workflow will enforce
        pass
