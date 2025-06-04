# queries that canbe used for retrieving and analyzing data in a database


sql_queries = {
    "describe_table": "DESCRIBE {table_name};",
    "select_all": "SELECT * FROM {table_name} LIMIT 5;",
    "count_records": "SELECT COUNT(*) FROM {table_name};",
    "list_tables": "SHOW TABLES;",
    "show_tables": "SHOW TABLES;",
    "select_with_condition": "SELECT * FROM {table_name} WHERE {condition};",
     "group_by_count": """
        SELECT {group_column}, COUNT(*) as count
        FROM {table_name}
        WHERE {condition}
        GROUP BY {group_column}
        {sort_clause}
        {limit_clause};
    """
}
