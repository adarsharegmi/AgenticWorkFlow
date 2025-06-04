import pandas as pd

class ExporterAgent:
    """
    Description:
    ExporterAgent is responsible for exporting data to various file formats.
    It supports exporting data in JSON, CSV, and TXT formats.
    This agent can be used to save query results or any other data in a structured format.
    Attributes:
        name (str): Name of the agent.
        file_path (str): Path where the exported file will be saved.
        export_format (str): Format in which data will be exported. Supported formats are "json", "csv", and "txt".
    Methods:
        export_data(data): Exports the provided data to a file in the specified format.
        export_format: str: The format in which data will be exported.
        
    
    """
    def __init__(self, name: str, file_path: str = "/tmp/exported_data.json", export_format: str = "json"):
        self.name = name
        self.file_path = file_path  # Default path for exported data
        self.export_format = export_format   # supports "json", "csv", "txt"
        
    def export_data(self, data):
        """
        Export data to a file in the specified format.
        :param data: Data to be exported.
        """
        import json
        try:
            with open(self.file_path, 'w') as file:
                if self.export_format == "json":
                    json.dump(data, file, indent=4)
                elif self.export_format == "csv":
                    df = pd.DataFrame(data)
                    df.to_csv(file, index=False)
                elif self.export_format == "txt":
                    with open(self.file_path, 'w') as file:
                        for item in data:
                            file.write(f"{item}\n")
                else:
                    raise ValueError("Unsupported export format")
            print(f"Data exported successfully to {self.file_path}")
        except Exception as e:
            print(f"An error occurred while exporting data: {e}")

    def set_export_format(self, format: str):
        """
        Set the export format for the data.
        :param format: Format in which data will be exported. Supported formats are "json", "csv", and "txt".
        """
        if format in ["json", "csv", "txt"]:
            self.export_format = format
        else:
            raise ValueError("Unsupported export format. Supported formats are 'json', 'csv', and 'txt'.")
        
    def set_file_path(self, path: str):
        """
        Set the file path where the exported data will be saved.
        :param path: Path where the exported file will be saved.
        """
        self.file_path = path
    
    def get_file_path(self):
        """
        Get the current file path where the exported data will be saved.
        :return: Current file path.
        """
        return self.file_path
    
