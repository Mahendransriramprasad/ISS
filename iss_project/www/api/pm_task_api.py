import frappe
from frappe import _

@frappe.whitelist()
def create_task(title, developer, project, estimated_hours, priority):
    user = frappe.session.user

    # Only PM can create tasks
    if "Project Manager" not in frappe.get_roles(user):
        frappe.throw(_("Not allowed."), frappe.PermissionError)

    doc = frappe.get_doc({
        "doctype": "Task",
        "title": title,
        "assigned_to": developer,
        "project": project,
        "estimated_hours": float(estimated_hours),
        "priority": priority,
        "status": "Open",
        "created_by_pm": user
    })

    doc.insert(ignore_permissions=True)

    return {"ok": True, "message": "Task created & assigned successfully"}
