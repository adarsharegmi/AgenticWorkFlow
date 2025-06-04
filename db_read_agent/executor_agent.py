import os
import pandas as pd
import mysql.connector
from db_read_agent.read_queries import sql_queries  

class SQLAgent:
    def __init__(self, config):
        """
        Initialize the SQLAgent with connection config.

        :param config: Dictionary containing database connection details
        """
        self.config = config
        self.connection = None

    def connect(self):
        """Establish a connection to the database."""
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.config)

    def disconnect(self):
        """Disconnect the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def execute_task(self, task):
        """
        Execute a given task using the predefined SQL queries.

        :param task: Dictionary containing the operation and its arguments.
        :return: Dataframe with the results of the query or an error message.
        """
        try:
            operation = task.get("operation")
            args = task.get("args", {})

            query = self.generate_sql_query(task)

            if not query:
                return {"status": "error", "message": f"Unknown operation '{operation}'"}


            # Connect to the database
            self.connect()

            with self.connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            # Convert query result to a pandas DataFrame
            df = pd.DataFrame(rows, columns=columns)

            # Handle data export if required
            if args.get("export_data"):
                export_path = args.get("export_path")
                export_format = args.get("export_format", "csv").lower()

                os.makedirs(os.path.dirname(export_path), exist_ok=True)

                if export_format == "csv":
                    df.to_csv(export_path, index=False)
                elif export_format in ["xlsx", "excel"]:
                    df.to_excel(export_path, index=False)
                elif export_format == "json":
                    df.to_json(export_path, orient='records', lines=True)
                elif export_format == "html":
                    df.to_html(export_path, index=False)
                else:
                    return {"status": "error", "message": f"Unsupported export format '{export_format}'"}

                return {"status": "success", "query": query, "message": f"Data exported to {export_path}", "data": df}

            return {"status": "success", "query": query, "data": df}

        except mysql.connector.Error as err:
            return {"status": "error", "message": f"MySQL Error: {err}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            self.disconnect()


    def generate_sql_query(self, args):
        """
        Generate a SQL query dynamically based on the operation and its arguments.

        :param args: Dictionary containing the operation type and associated arguments.
        :return: A complete SQL query string or an error message.
        """
        if True:
        # try:
            operation = args.get("operation")

            query_template = sql_queries.get(operation)

            if not query_template:
                raise ValueError(f"Unknown operation '{operation}'")
            
            args = args.get("args", {})
            table_name = args.get("table_name")
            group_column = args.get("group_column")
            condition = args.get("condition", "1=1")  
            sort_clause = "{sort_clause}"
            if "sort_column" in args and "sort_order" in args:
                sort_clause = f"ORDER BY {args['sort_column']} {args['sort_order']}"
            elif "sort_column" in args:
                sort_clause = f"ORDER BY {args['sort_column']} ASC"

            limit_clause = args.get("limit", "")
            if limit_clause:
                limit_clause = f"LIMIT {limit_clause}"
            

            if not table_name or not group_column:
                raise ValueError("Both 'table_name' and 'group_column' are required.")
            
            query = query_template.format(
                table_name=table_name,
                group_column=group_column,
                condition=condition,
                sort_clause=sort_clause,
                limit_clause=limit_clause
            )

            if "sort_by" in args:
                sort_column = args["sort_by"]
                sort_order = args.get("sort_order", "asc")
                sort_clause = f"ORDER BY {sort_column} {sort_order}"
                query = query.replace("{sort_clause}", sort_clause)

            if "limit" in args:
                limit_clause = f"LIMIT {args['limit']}"
                query = query.replace("{limit_clause}", limit_clause)

            return query

        # except Exception as e:
        #     raise Exception(f"Error generating SQL query: {str(e)}")


