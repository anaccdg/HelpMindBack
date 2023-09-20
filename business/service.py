import pyodbc

class SQLServerDB:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        connection_string = f"DRIVER=SQL Server;SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        self.conn = pyodbc.connect(connection_string)
        print("Connected to SQL Server")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from SQL Server")

    def execute_query(self, query):
        if not self.conn:
            print("Not connected to SQL Server")
            return None

        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_teste(self):
        server = 'localhost'
        database = 'VINICIUS_PRD'
        username = 'sa'
        password = '1234'

        db = SQLServerDB(server, database, username, password)
        db.connect()

        # Example query
        query = "SELECT * FROM TABELA"
        result = db.execute_query(query)
        print(result)

        db.disconnect()
