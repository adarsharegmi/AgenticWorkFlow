from db_read_agent.executor_agent import SQLAgent
from standardize_agent.main import DataFrameAgent
from ui_agent import SQLVisualizerAgentUI
from visualizer_agent import SQLVisualizerAgent
from db_inspector import DatabaseInspector
from exporter_agent import ExporterAgent

import os

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def take_input(prompt):
    """
    Take input from the user.
    This function can be modified to handle different input methods if needed.
    """
    return input(prompt)

# parse the input to get the task type
def parse_input(input_str):
    """
    Parse the input string to determine the type of task.
    This function can be modified to handle different input formats if needed.

    table name detect column name, operation and so on
    """
    found_data = {}

    # first search for task type in the prompt
    input_str = input_str.lower().strip()
    if "group by" in input_str:
        found_data["operation"] = "group_by_count"
    elif "describe" in input_str:
        found_data["operation"] = "describe_table"
    elif "select" in input_str:
        found_data["operation"] = "select_all"
    elif "count" in input_str:
        found_data["operation"] = "count_records"
    elif "list tables" in input_str or "show tables" in input_str:
        found_data["operation"] = "list_tables"
    elif "select with condition" in input_str:
        found_data["operation"] = "select_with_condition"
    else:
        found_data["operation"] = "group_by_count"

    # Extract table name and column name if present
    if "from" in input_str:
        table_name_start = input_str.find("from") + 4
        table_name_end = input_str.find(" ", table_name_start)
        if table_name_end == -1:
            table_name_end = len(input_str)
        found_data["table_name"] = input_str[table_name_start:table_name_end].strip()

    else:
        found_data["table_name"] = "booking_origins"

    if "group by" in input_str:
        group_column_start = input_str.find("group by") + 8
        group_column_end = input_str.find(" ", group_column_start)
        if group_column_end == -1:
            group_column_end = len(input_str)
        found_data["group_column"] = input_str[group_column_start:group_column_end].strip()
    else:
        found_data["group_column"] = "code"

    if "where" in input_str:
        condition_start = input_str.find("where") + 5
        condition_end = input_str.find(" ", condition_start)
        if condition_end == -1:
            condition_end = len(input_str)
        found_data["condition"] = input_str[condition_start:condition_end].strip()

    else:
        found_data["condition"] = "code IS NOT NULL"

    if "sort by" in input_str:
        sort_by_start = input_str.find("sort by") + 8
        sort_by_end = input_str.find(" ", sort_by_start)
        if sort_by_end == -1:
            sort_by_end = len(input_str)
        found_data["sort_column"] = input_str[sort_by_start:sort_by_end].strip()
    else:
        found_data["sort_column"] = "count"

    if "sort order" in input_str:
        sort_order_start = input_str.find("sort order") + 11
        sort_order_end = input_str.find(" ", sort_order_start)
        if sort_order_end == -1:
            sort_order_end = len(input_str)
        found_data["sort_order"] = input_str[sort_order_start:sort_order_end].strip()
    else:
        found_data["sort_order"] = "desc"

    if "limit" in input_str:
        limit_start = input_str.find("limit") + 5
        limit_end = input_str.find(" ", limit_start)
        if limit_end == -1:
            limit_end = len(input_str)
        found_data["limit"] = input_str[limit_start:limit_end].strip()
    else:
        found_data["limit"] = 10

    return found_data 


def generate_task(type="select_with_condition", table_name="booking_origins", column_name="code",
                  sort_by="count", sort_order="desc", limit=10, condition="code IS NOT NULL"):
    """
    Generate a task for the SQLAgent to execute.
    This function can be modified to create different tasks as needed.
    """
    return {
        "operation": type,
        "args": {
            "table_name": table_name,
            "group_column": column_name,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "limit": limit,
            "condition": condition,
            "export_data": True,
            "export_format": "csv",
            "export_path": "summary/booking_origins_grouped.csv"
        }
    }


task = {
    "operation": "select_with_condition",
    "args": {
        "table_name": "booking_origins",
        "group_column": "addon_groups",
        "sort_by": "count",
        "sort_order": "desc",
        "limit": 10,
        "export_data": True,
        "export_format": "json",
        "export_path": "summary/booking_origins_grouped.json"
    }
}

config = {
    "host": os.environ.get("DB_HOST", "localhost"),  
    "user": os.environ.get("DB_USER", "mysql"), 
    "password": os.environ.get("DB_PASSWORD", "mysql"), 
    "database": os.environ.get("DB_NAME", "mysql") 
}


inspector = DatabaseInspector(config)
database_summary = inspector.inspect_database()

exporter_agent = ExporterAgent(name="DatabaseSummaryExporter", export_format="json", export_path="summary/database_summary.json")
response = exporter_agent.export_data(data=database_summary)


if response["status"] == "success":
    print(f"Database summary exported successfully to: {response['message']}")
else:
    print(f"Error exporting database summary: {response['message']}")



# from db_read_agent.executor_agent import SQLAgent
# Show summary
# for table, summary in database_summary.items():
#     print(f"\nTable: {table}")
#     print(f"Valid Columns (more than 50% non-null values):")
#     for col, valid_percentage in summary['valid_columns'].items():
#         print(f"  - {col}: {valid_percentage}% valid")




# agent = SQLAgent(config)
# response = agent.execute_task(task)

# if response["status"] == "success":
#     print(f"Task executed successfully. Data exported to: {response['message']}")
#     agent = DataFrameAgent(dataframe=response["data"])

#     # Data Processing (e.g., handling missing data, duplicates, etc.)
#     agent.remove_duplicates()
#     agent.filter_columns_by_valid_data()

#     # View the processed dataframe
#     processed_df = agent.get_dataframe()

#     print(processed_df.head())

#     # Visualize using UI
#     visualizer_ui = SQLVisualizerAgentUI(agent)
#     visualizer_ui.display_table_in_ui(processed_df)  # Display processed DataFrame in UI
# else:
#     print(f"Error: {response['message']}")
