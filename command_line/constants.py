class RestoreFromBackupTemplateConfig:

    CMD_DIRECTORY = "C:"

    CMD_SCRIPT_TEMPLATE = """
    pg_restore.exe --host {server} --port {port} --username {username} --dbname postgresql://{username}:{password}@{server}:{port}/{database} --table {table} --schema {schema} --verbose "{backup_path_name}"
    """

    RESTORE_SCHEMA = "public"
    RESTORE_DATABASE = "datamart_partial"

    TABLES_TO_RESTORE = {
        "g_africa": [
            "integration_control",
            "stage_vendor",
            "stage_entity_advanced_funding",
            "smart_project_entity",
            "stage_wire_transactions_entity",
            "stage_ceo_expenses_wages_transactions_entity",
            "stage_entity_standard_costs",
            "trip_cost_accruals_entity",
            "prepost_cost_accruals_entity",
            "trip_revenue_accruals_entity",
            "prepost_revenue_accruals_entity",
            "stage_gl_revenue_entity",
            "stage_gl_cogs_move_entity",
            "stage_expired_entity_advanced_funding",
            "stage_entity_actual_funding",
        ]
    }

    RESTORE_FILENAME = {"g_africa": "gafrica_restore.bat"}
