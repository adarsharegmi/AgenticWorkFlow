import pandas as pd
from db_read_agent.executor_agent import SQLAgent
from standardize_agent.main import DataFrameAgent


class DatabaseInspector:
    def __init__(self, config):
        self.agent = SQLAgent(config)

    def get_all_tables(self):
        """
        Retrieve all table names from the database.
        """
        query = "SHOW TABLES"
        response = self.agent.execute_sql(query)
        return sum(response.values.tolist(), [])
    
    def get_table_columns(self, table_name):
        """
        Retrieve column names and types for a given table.
        """
        query = f"DESCRIBE {table_name}"
        response = self.agent.execute_sql(query)
        columns_info = [{"column_name": row[0], "data_type": row[1]} for row in response]
        return columns_info

    def get_column_validity(self, table_name):
        """
        Performs EDA for missing value.
        """
        query = f"SELECT * FROM {table_name} LIMIT 1000"  # Fetch a sample of the table
        response = self.agent.execute_sql(query)
        self.dataframe_agent = DataFrameAgent(dataframe=response)  
        self.dataframe_agent.filter_columns_by_valid_data()
        return self.dataframe_agent.get_dataframe()

    def inspect_database(self):
        """
        Inspect the entire database: Get all tables and columns with valid values.
        """
        all_tables = self.get_all_tables()
        tables_summary = {}

        for table in all_tables:
            print(f"\nInspecting table: {table}")
            columns_info = self.get_table_columns(table)
            dataframe = self.get_column_validity(table)

            valid_columns = {col: dataframe[col] for col in dataframe }
            
            tables_summary[table] = {
                "columns": columns_info,
                "valid_columns": valid_columns
            }

        return tables_summary