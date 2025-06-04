import matplotlib.pyplot as plt
import pandas as pd

class SQLVisualizerAgent:
    def __init__(self, sql_agent):
        """
        Initialize SQLVisualizerAgent with the given SQLAgent instance.
        This allows for visualization of SQL query results in various formats.
        
        :param sql_agent: Instance of the SQLAgent for querying the database
        """
        self.sql_agent = sql_agent

    def plot_table(self, df, title="Table Visualization"):
        """
        Visualize the DataFrame as a table using matplotlib.
        
        :param df: Pandas DataFrame to be visualized.
        :param title: Title of the plot window.
        """
        fig, ax = plt.subplots(figsize=(8, 6))  
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colLoc='center')
        plt.title(title)
        plt.show()
        plt.savefig(f"{title}.png", bbox_inches='tight', dpi=300)
    
    def visualize_table(self, table_name):
        """
        Fetch the table from the database and visualize it.
        
        :param table_name: Name of the table to visualize.
        """
        task = {
            "operation": "select_all", 
            "args": {
                "table_name": table_name
            }
        }
        
        result = self.sql_agent.execute_task(task)
        
        if result["status"] == "success":
            df = result["data"]
            self.plot_table(df, title=f"Table: {table_name}")
        else:
            print(f"Error fetching data for {table_name}: {result['message']}")
