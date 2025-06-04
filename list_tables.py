from connect import connect_to_database

connection = connect_to_database()

cursor = connection.cursor()

def list_tables():
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        tables_info = []
        if tables:
            for table in tables:
                print(table[0])
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                # Exporting table names and record counts to a JSON file
                table_info = {
                    "table_name": table[0],
                    "record_count": count
                }
                # Append to a list to write later

                tables_info.append(table_info)
            if 'tables_info' in locals():
                with open('tables_info.json', 'w') as f:
                    import json
                    json.dump(tables_info, f, indent=4)
        else:
            print("No tables found in the database.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def list_tables_with_prefix(list_of_content_included_in_name):
    try:
        for prefix in list_of_content_included_in_name:
            cursor.execute(f"SHOW TABLES LIKE '%{prefix}%'")
            tables = cursor.fetchall()
            
            if tables:
                print(f"Tables in the database with prefix '{prefix}':")
                for table in tables:
                    print(table[0])
                return tables
            else:
                print(f"No tables found in the database with prefix '{prefix}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return []
    
list_tables()
tables = list_tables_with_prefix(['features', 'ratings', 'addons', 'menu_options'])


def describe_table(table_name):
    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        print(f"Structure of '{table_name}':")
        for col in columns:
            print(col)
    except Exception as e:
        print(f"Error describing table {table_name}: {e}")

# Example usage
for table in ['features', 'ratings', 'addons', 'menu_options']:
    describe_table(table)
