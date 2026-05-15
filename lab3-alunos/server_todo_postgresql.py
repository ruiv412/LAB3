import psycopg2 
import socket

# TODO: Change this to your own connection string
CONNECTION_STRING = "postgresql://postgres.gcblvyidlrutgzmbxmvb:Asdrubal1234.@aws-1-eu-west-2.pooler.supabase.com:5432/postgres"

# This class reads and saves ToDo items from an SQL database
class TodoList:

    #
    # Add a new item to the database
    #
    def add_item(self, title, description):
        # create a connection to the database
        conn = psycopg2.connect(CONNECTION_STRING)

        # create a cursor object
        cur = conn.cursor()

        # define the SQL statement with placeholders
        sql = "INSERT INTO Tasks (title, description, completed) VALUES (%s, %s, %s)"

        # execute the prepared statement with the input values
        cur.execute(sql, (title, description, False))

        # commit the changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()

    #
    # Mark an item as completed
    #
    def complete_item(self, id):
        # create a connection to the database
        conn = psycopg2.connect(CONNECTION_STRING)

        # create a cursor object
        cur = conn.cursor()

        # define the SQL statement with placeholders
        sql = "UPDATE Tasks SET completed = TRUE WHERE id = %s"

        # execute the prepared statement with the input values
        cur.execute(sql, (id,))

        # commit the changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()

    #
    # Return the number of items in the database
    #
    def count_items(self):
        # create a connection to the database
        conn = psycopg2.connect(CONNECTION_STRING)

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Tasks;")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    #
    # Return a string representation of the list of items
    #
    def get_list_of_items(self):
        # connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()

        # retrieve the list of items from the Tasks table
        cur.execute("SELECT id, title, description, completed FROM Tasks")
        rows = cur.fetchall()

        # generate the string representation of the list of items
        result = ""
        for row in rows:
            status = "[ ]"
            if row[3]:
                status = "[x]"
            result += f"{row[0]}. {status} {row[1]}: {row[2]}\n"

        # close the database connection and return the result
        cur.close()
        conn.close()
        return result

host = 'localhost'
port = 5432

todo_list = TodoList()    

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server started on port {port}...")
print("Serving todo list...")
print(todo_list.get_list_of_items())

# Loop forever, waiting for client commands
while True:
    # Accept a connection
    print("Waiting for connection...")
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # receive operation and numbers and make calculation
    command = client_socket.recv(1024).decode()
    print(f"Received command: {command}")
    choice, data = command.split("-")
    if choice == "1":
        title, description = data.split(",")
        todo_list.add_item(title, description)
        result = "Todo added."
    elif choice == "2":
        result = todo_list.get_list_of_items()
    elif choice == "3":
        todo_list.complete_item(data)
        result = "Todo completed."
    else:
        result = "Invalid command."
    print("Logging: " + result)
    client_socket.send(result.encode())
    client_socket.close()