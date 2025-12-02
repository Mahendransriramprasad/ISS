# apps/iss_project/iss_project/www/api/login.py
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def portal_login(email=None, password=None):
    # Prefer form_dict values if available (POST form-encoded)
    form = frappe.local.form_dict
    if not email:
        email = form.get("email")
    if not password:
        password = form.get("password")

    if not email or not password:
        frappe.local.response.http_status_code = 400
        return {"status": "fail", "message": "Missing credentials"}

    try:
        # authenticate using Frappe's LoginManager
        lm = frappe.auth.LoginManager()
        lm.authenticate(user=email, pwd=password)
        lm.post_login()

        # determine redirect route based on roles
        roles = frappe.get_roles(email)
        if "HR & Finance" in roles:
            redirect = "/dashboard/hr"
        elif "Project Manager" in roles:
            redirect = "/dashboard/pm"
        elif "Developer" in roles:
            redirect = "/dashboard/developer"
        elif "Management" in roles:
            redirect = "/dashboard/management"
        else:
            redirect = "/"

        return {"status": "success", "message": {"redirect": redirect}}

    except frappe.AuthenticationError:
        frappe.local.response.http_status_code = 401
        return {"status": "fail", "message": "Invalid credentials"}
    except Exception as e:
        # log and return safe message
        frappe.log_error(frappe.get_traceback(), "portal_login_error")
        frappe.local.response.http_status_code = 500
        return {"status": "fail", "message": "Server error"}
