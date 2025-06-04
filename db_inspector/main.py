import pandas as pd
from db_read_agent.executor_agent import SQLAgent
from standardize_agent.main import DataFrameAgent
import re


class DatabaseInspector:
    def __init__(self, config, table_name=None):
        """
        Initialize the DatabaseInspector with a SQLAgent instance and optionally a table name.
        :param config: Configuration for the SQLAgent, typically includes database connection details.
        :param table_name: Optional name of the table to inspect. If provided, it will fetch a sample of the table.
        """
        self.config = config
        self.table_name = table_name
        self.agent = SQLAgent(config)

    def get_all_tables(self):
        """
        Retrieve all table names from the database.
        """
        query = "SHOW TABLES"
        response = self.agent.execute_sql(query)
        return sum(response.values.tolist(), [])
    
    def get_table_columns(self):
        """
        Retrieve column names and types for a given table.
        """
        query = f"DESCRIBE {self.table_name}"
        response = self.agent.execute_sql(query)
        columns_info = [{"column_name": row[0], "data_type": row[1]} for row in response]
        return columns_info

    def set_column_validity(self, table_name=None):
        """
        Performs EDA for missing value.
        """
        if table_name is None:
            if self.table_name is None:
                raise ValueError("No table name provided for column validity check.")
            table_name = self.table_name

        query = f"SELECT * FROM {table_name} LIMIT 1000"
        response = self.agent.execute_sql(query)
        if response.empty:
            pass
            # raise ValueError(f"No data found in table: {self.table_name}")
        
        self.dataframe_agent = DataFrameAgent(dataframe=response)  
        self.dataframe_agent.filter_columns_by_valid_data()
        self.valid_columns = self.dataframe_agent.get_dataframe().columns.to_list()


    def apply_remove_postfixes(self, postfixes=None):
        """
        Remove columns whose names end with specific postfixes.
        
        :param postfixes: List of postfix strings to exclude (default: ['_id', '_at', '_ts', '_timestamp', '_ms'])
        """
        if postfixes is None:
            postfixes = ['_id', '_at', '_ts', '_timestamp','_ms', ]

        columns = self.dataframe_agent.get_dataframe().columns.to_list()
        pattern = re.compile(rf"({'|'.join(re.escape(p) for p in postfixes)})$", re.IGNORECASE)

        # Filter out columns that end with any of the postfixes
        self.valid_columns = [col for col in columns if not pattern.search(col)]



    def inspect_database(self):
        """
        Inspect the entire database: Get all tables and columns with valid values.
        """
        all_tables = self.get_all_tables()
        tables_summary = {}

        for table in all_tables:
            print(f"\nInspecting table: {table}")
            self.set_column_validity(table)
            self.apply_remove_postfixes()
            tables_summary[table] = self.valid_columns
        return tables_summary