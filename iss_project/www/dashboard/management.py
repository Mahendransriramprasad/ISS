# apps/iss_project/iss_project/www/dashboard/management.py
import frappe

def get_context(context):
    user = frappe.session.user
    if user == "Guest":
        frappe.local.flags.redirect_location = "/portal_login"
        raise frappe.Redirect
    roles = frappe.get_roles(user)
    if not any(r in roles for r in ["Management", "System Manager"]):
        frappe.local.flags.redirect_location = "/portal_login"
        raise frappe.Redirect
    context.user = user
    context.roles = roles
