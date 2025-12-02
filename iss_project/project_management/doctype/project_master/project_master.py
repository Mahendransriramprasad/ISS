from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class ProjectMaster(Document):
    def validate(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            frappe.throw(_("End Date cannot be before Start Date"))

    def on_update(self):
        # placeholder for later hooks/enqueue
        pass

    def compute_summary(self):
        from iss_project.modules.utils.calculations import calculate_project_summary
        summary = calculate_project_summary(self.name)
        self.db_set("last_utilization_pct", summary.get("util_pct") or 0)
        self.db_set("last_profit_pct", summary.get("profit_pct") or 0)
        return summary
