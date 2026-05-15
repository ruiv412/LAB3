import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import socket

class TodoList:
    def __init__(self):
        #cred = credentials.Certificate("... TODO: Change this to your own Firebase Admin SDK JSON file ...")
        cred = credentials.Certificate("certificado.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    #
    # Add a new item to the database
    #
    def add_item(self, title, description):
        # add a new document to the "tasks" collection with the given title, description, and completed status
        doc_ref = self.db.collection("tasks").document()
        doc_ref.set({
            "title": title,
            "description": description,
            "completed": False
        })

    #
    # Mark an item as completed
    #
    def complete_item(self, id):
        # update the completed status of the document with the given ID in the "tasks" collection
        doc_ref = self.db.collection("tasks").document(id)
        doc_ref.update({
            "completed": True
        })

    #
    # Return the number of items in the database
    #
    def count_items(self):
        # query the "tasks" collection and return the count of documents
        tasks_ref = self.db.collection("tasks")
        count = len(tasks_ref.get())
        return count

    #
    # Return a string representation of the list of items
    #
    def get_list_of_items(self):
        # query the "tasks" collection and generate a string representation of the list of items
        tasks_ref = self.db.collection("tasks")
        docs = tasks_ref.stream()
        result = ""
        for doc in docs:
            status = "[ ]"
            if doc.to_dict()["completed"]:
                status = "[x]"
            result += f"{doc.id}. {status} {doc.to_dict()['title']}: {doc.to_dict()['description']}\n"
        return result

host = 'localhost'
port = 8888

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
    