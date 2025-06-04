import tkinter as tk
from tkinter import ttk
import pandas as pd

class SQLVisualizerAgentUI:
    def __init__(self, sql_agent):
        """
        Initialize SQLVisualizerAgentUI with the given SQLAgent instance.
        This allows for a UI-based visualization of SQL query results.
        
        :param sql_agent: Instance of the SQLAgent for querying the database
        """
        self.sql_agent = sql_agent

    def display_table_in_ui(self, df, title="Table Visualization"):
        """
        Display the table in a Tkinter UI window.
        
        :param df: Pandas DataFrame to be displayed.
        :param title: Title of the window.
        """
        root = tk.Tk()
        root.title(title)

        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
        
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll_y.set)

        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        scroll_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scroll_x.set)

        tree.pack(fill="both", expand=True)

        root.mainloop()

    def visualize_table_in_ui(self, table_name):
        """
        Fetch the table from the database and display it in a Tkinter UI window.
        
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
            self.display_table_in_ui(df, title=f"Table: {table_name}")
        else:
            print(f"Error fetching data for {table_name}: {result['message']}")
