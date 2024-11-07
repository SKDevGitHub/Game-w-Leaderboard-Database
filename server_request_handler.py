import socket

class ServerRequestHandler:
    def __init__(self, host, port, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.sock = None

    def connect(self):
        """Open a connection to the backend"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"Connected to backend at {self.host}:{self.port}")
        except socket.error as e:
            print(f"Connection error: {e}")
            self.sock = None

    def _send(self, message):
        if not self.sock:
            print("No connection")
            return
        try:
            self.sock.sendall(message.encode())
            print(f"Sent: {message}")
        except socket.error as e:
            print(f"Send error: {e}")

    def _recv(self):
        if not self.sock:
            print("No connection")
            return None
        try:
            data = self.sock.recv(self.buffer_size)
            message = data.decode()
            print(f"Received: {message}")
            return message
        except socket.error as e:
            print(f"Receive error: {e}")
            return None

    def register(username: str, password: str) -> bool:
        """Return true if successful"""
        pass

    def login(username: str, password: str) -> bool:
        """Return true if successful"""
        pass

    def leaderboard_data_query(level_id: int) -> list:
        pass

    def get_level_data(level_id: int) -> str:
        pass

    def get_level_comments(level_id: int) -> list:
        pass

    def submit_new_level(level_string_representation: str, level_name: str, username: str) -> bool:
        """Return true if successful"""
        pass

    def create_comment(username: str, level_id: int, comment_text: str) -> bool:
        """Return true if successful"""
        pass

    def like_comment(comment_id: int) -> bool:
        """Return true if successful"""
        pass

    def dislike_comment(comment_id: int) -> bool:
        """Return true if successful"""
        pass

    def get_user_data(username: str): # return TBD
        pass

    def search_for_level(search_str: str) -> list:
        pass

    def search_for_user(search_str: str) -> list:
        pass

    def close(self):
        """Close connection to the backend"""
        if self.sock:
            try:
                self.sock.close()
                print("Connection closed.")
            except socket.error as e:
                print(f"Error closing connection: {e}")
            finally:
                self.sock = None
        else:
            print("Connection was already closed.")