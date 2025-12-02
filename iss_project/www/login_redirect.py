import frappe

def get_context(context):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if "Developer" in roles:
        frappe.local.flags.redirect_location = "/dashboard/developer"
    elif "Project Manager" in roles:
        frappe.local.flags.redirect_location = "/dashboard/pm"
    elif "HR Finance" in roles:
        frappe.local.flags.redirect_location = "/dashboard/hr"
    elif "Management" in roles:
        frappe.local.flags.redirect_location = "/dashboard/management"
    else:
        frappe.local.flags.redirect_location = "/portal_login"

    raise frappe.Redirect
