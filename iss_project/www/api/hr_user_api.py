import frappe
from frappe import _

@frappe.whitelist()
def create_portal_user(full_name, email, role_type):
    # Ensure only HR Finance or System Manager can create users
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if not any(r in roles for r in ["HR Finance", "System Manager"]):
        frappe.throw(_("Permission Denied"), frappe.PermissionError)

    # Check if email exists
    if frappe.db.exists("User", email):
        frappe.throw(_("User already exists."))

    # Create user
    new_user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "enabled": 1,
        "new_password": "indosakura",   # Default password
        "send_welcome_email": 0,
        "user_type": "Website User"
    })
    new_user.insert(ignore_permissions=True)

    # Assign roles
    role_map = {
        "Developer": "Developer",
        "Project Manager": "Project Manager",
        "HR Finance": "HR Finance",
        "Management": "Management",
    }

    assigned_role = role_map.get(role_type)

    if not assigned_role:
        frappe.throw(_("Invalid role type"))

    new_user.add_roles(assigned_role)

    return {
        "ok": True,
        "message": f"{role_type} user created successfully."
    }
