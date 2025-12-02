import frappe
from frappe import _

@frappe.whitelist()
def log_hours(task, hours, work_date, description):
    user = frappe.session.user

    if "Developer" not in frappe.get_roles(user):
        frappe.throw(_("Not allowed"), frappe.PermissionError)

    doc = frappe.get_doc({
        "doctype": "Timesheet Entry",
        "developer": user,
        "task": task,
        "hours": float(hours),
        "work_date": work_date,
        "description": description,
        "status": "Pending Approval"
    })

    doc.insert(ignore_permissions=True)

    return {"ok": True, "message": "Timesheet submitted for approval"}
