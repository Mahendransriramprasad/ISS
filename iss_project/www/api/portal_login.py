import frappe

@frappe.whitelist(allow_guest=True)
def portal_login(email=None, password=None):
    if not email or not password:
        return {"status": "error", "message": "Missing email or password"}

    try:
        # try login
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(email, password)
        login_manager.post_login()

        return {
            "status": "success",
            "message": "Logged in",
            "user": email
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
