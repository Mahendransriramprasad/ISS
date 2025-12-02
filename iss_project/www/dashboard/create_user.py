import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/portal_login"
        raise frappe.Redirect
    
    roles = frappe.get_roles(frappe.session.user)
    if "HR Finance" not in roles:
        frappe.local.flags.redirect_location = "/portal_login"
        raise frappe.Redirect

    return context
