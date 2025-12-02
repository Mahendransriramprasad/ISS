import frappe
from frappe import _

@frappe.whitelist()
def approve_timesheet(timesheet_id):
    user = frappe.session.user

    if "Project Manager" not in frappe.get_roles(user):
        frappe.throw(_("Permission denied"), frappe.PermissionError)

    ts = frappe.get_doc("Timesheet Entry", timesheet_id)
    ts.status = "Approved"
    ts.save(ignore_permissions=True)

    return {"ok": True, "message": "Approved"}

@frappe.whitelist()
def reject_timesheet(timesheet_id, reason):
    user = frappe.session.user

    if "Project Manager" not in frappe.get_roles(user):
        frappe.throw(_("Permission denied"), frappe.PermissionError)

    ts = frappe.get_doc("Timesheet Entry", timesheet_id)
    ts.status = "Rejected"
    ts.rejection_reason = reason
    ts.save(ignore_permissions=True)

    return {"ok": True, "message": "Rejected"}
