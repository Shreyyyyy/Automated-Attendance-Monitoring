import pymysql

# Establish connection
connection = pymysql.connect(
    host='localhost', user='root', password='YES', db='manually_fill_attendance')
cursor = connection.cursor()

try:
    # Get list of tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    # Loop through tables
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        
        # Get columns of each table
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        
        # Loop through columns
        for column in columns:
            column_name = column[0]
            data_type = column[1]
            print(f"  {column_name}: {data_type}")
finally:
    # Close cursor and connection
    cursor.close()
    connection.close()
