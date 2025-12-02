import frappe
from frappe.model.document import Document

class PMScorecard(Document):
    def validate(self):
        # Automatically calculate final score
        self.final_score = (
            (self.on_time_delivery or 0) * 0.4 +
            (self.budget_efficiency or 0) * 0.4 +
            (self.resource_utilization_score or 0) * 0.2
        )
