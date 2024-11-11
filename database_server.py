import socket
import threading
import sqlite3

# Server class to handle database connections and client requests
class DatabaseServer:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = sqlite3.connect('project_database.db', check_same_thread=False)
        self.lock = threading.Lock()
        self._setup_database()

    def _setup_database(self):
        # Create tables if they don't exist
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Level (
                    levelName TEXT PRIMARY KEY,
                    levelFile TEXT,
                    creatorId TEXT NOT NULL,
                    FOREIGN KEY (creatorId) REFERENCES User(username)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Comments (
                    likes INTEGER,
                    dislikes INTEGER,
                    commentText TEXT,
                    commentId INTEGER PRIMARY KEY,
                    userId TEXT NOT NULL,
                    levelName TEXT NOT NULL,
                    FOREIGN KEY (userId) REFERENCES User(username),
                    FOREIGN KEY (levelName) REFERENCES Level(levelName)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Solution (
                    solutionId INTEGER PRIMARY KEY,
                    score INTEGER,
                    movelist TEXT,
                    userId TEXT NOT NULL,
                    FOREIGN KEY (userId) REFERENCES User(username)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Submission (
                    submissionId INTEGER PRIMARY KEY,
                    dos TEXT,
                    solutionId INTEGER NOT NULL,
                    userId TEXT NOT NULL,
                    levelName TEXT NOT NULL,
                    FOREIGN KEY (userId) REFERENCES User(username),
                    FOREIGN KEY (levelName) REFERENCES Level(levelName),
                    FOREIGN KEY (solutionId) REFERENCES Solution(solutionId)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Rating (
                    userRating INTEGER,
                    diffRating INTEGER,
                    userName TEXT NOT NULL,
                    levelName TEXT NOT NULL,
                    FOREIGN KEY (userName) REFERENCES User(username),
                    FOREIGN KEY (levelName) REFERENCES (levelName)
                )
            ''')
            self.conn.commit()

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.sock.accept()
            print(f"Client connected: {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                    print(f"Received query: {data}")
                    result = self.execute_query(data)
                    client_socket.sendall(result.encode())
                except Exception as e:
                    print(f"Error handling client request: {e}")
                    client_socket.sendall(f"Error: {e}".encode())
                    break

    def execute_query(self, query):
        with self.lock:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                if query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return str(result)
                else:
                    self.conn.commit()
                    return "Success"
            except sqlite3.Error as e:
                return f"Database error: {e}"

    def close(self):
        self.conn.close()
        self.sock.close()

if __name__ == "__main__":
    server = DatabaseServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.close()