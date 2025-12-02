# apps/iss_project/iss_project/www/api/dashboard_api.py
import frappe
from frappe import _

def _check_role(allowed_roles):
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Not Logged In"), frappe.AuthenticationError)
    roles = frappe.get_roles(user)
    if not any(r in roles for r in allowed_roles):
        frappe.throw(_("Permission Denied"), frappe.PermissionError)
    return user, roles

@frappe.whitelist()
def get_pm_dashboard():
    user, roles = _check_role(["Project Manager", "HR Finance", "Management", "System Manager"])
    # Projects managed by PM
    projects = frappe.get_all("Project Master", filters={"project_manager": user},
                              fields=["name", "project_code", "project_name", "budget_percent", "last_utilization_pct", "last_profit_pct"])
    # Pending timesheet approvals
    pending_ts = frappe.get_all("Timesheet Entry", filters={"status":"Pending Approval", "project": ["in", [p["name"] for p in projects]]},
                                fields=["name","user","task","hours","work_date","project"], limit_page_length=50)
    # Milestone summary
    milestones = frappe.get_all("Milestone", filters={"project": ["in", [p["name"] for p in projects]]},
                                fields=["name","milestone_name","project","planned_date","actual_date","status","extension_count"])
    # PM Scorecards
    scorecards = frappe.get_all("PM Scorecard", filters={"project_manager": user}, fields=["period","final_score"], limit_page_length=10, order_by="period desc")
    return {
        "projects": projects,
        "pending_timesheets": pending_ts,
        "milestones": milestones,
        "scorecards": scorecards
    }

@frappe.whitelist()
def get_hr_dashboard():
    user, roles = _check_role(["HR Finance", "Management", "System Manager"])
    # Budgets summary
    budgets = frappe.get_all("Budget Entry", fields=["project","budget_type","budget_percent"])
    # Resource summary
    resources = frappe.get_all("Resource Master", fields=["user","full_name","role_type","billing_rate"])
    # Costing aggregates (simple)
    # compute project-level utilization counts
    from frappe.utils import nowdate
    util_agg = frappe.db.sql("""
        SELECT project, SUM(billable_hours) as billable, SUM(non_billable_hours) as non_billable
        FROM `tabUtilization Log` GROUP BY project
    """, as_dict=1)
    return {
        "budgets": budgets,
        "resources": resources,
        "utilization": util_agg,
        "now": frappe.utils.now()
    }

@frappe.whitelist()
def get_management_dashboard():
    user, roles = _check_role(["Management", "System Manager"])
    # Portfolio summary: project count, avg utilization, top/bottom PMs
    proj_count = frappe.db.count("Project Master")
    avg_util = frappe.db.sql("""SELECT AVG(last_utilization_pct) as avg_util FROM `tabProject Master`""", as_dict=1)[0].get("avg_util") or 0
    # PM ranking: top 5 by latest PM Scorecard final_score
    pm_scores = frappe.db.sql("""
        SELECT project_manager, AVG(final_score) as avg_score
        FROM `tabPM Scorecard`
        GROUP BY project_manager
        ORDER BY avg_score DESC
        LIMIT 10
    """, as_dict=1)
    # RAG: projects by utilization thresholds (R: >100, A: 90-100, G: <90) using last_utilization_pct
    rag = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN last_utilization_pct > 100 THEN 1 ELSE 0 END) as red,
            SUM(CASE WHEN last_utilization_pct BETWEEN 90 AND 100 THEN 1 ELSE 0 END) as amber,
            SUM(CASE WHEN last_utilization_pct < 90 THEN 1 ELSE 0 END) as green
        FROM `tabProject Master`
    """, as_dict=1)[0]
    return {
        "project_count": proj_count,
        "avg_utilization": avg_util,
        "pm_ranking": pm_scores,
        "rag": rag
    }
