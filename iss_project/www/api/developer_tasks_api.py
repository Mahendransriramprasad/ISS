import frappe

@frappe.whitelist()
def get_my_tasks():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if "Developer" not in roles:
        frappe.throw("Unauthorized", frappe.PermissionError)

    tasks = frappe.get_all(
        "Task",
        filters={"assigned_to": user},
        fields=[
            "name", "title", "status", "estimated_hours",
            "project", "priority"
        ]
    )

    return tasks
