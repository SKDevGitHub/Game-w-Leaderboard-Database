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

    def register(self, username: str, password: str) -> bool:
        """Return true if successful"""
        self._send(f'INSERT INTO User VALUES ({username},{password})')
        result = self._recv()
        return result == "" # no error

    def login(self, username: str, password: str) -> bool:
        """Return true if successful"""
        """TODO: Return UserID"""
        self._send(f'SELECT * FROM User WHERE username={username} AND password={password}')
        result = self._recv()
        return result != "" # user is found

    def leaderboard_data_query(self, level_id: int) -> list:
        self._send(f'SELECT userID, score, dos FROM Level JOIN Submission JOIN Solution WHERE levelId={level_id}')
        result = self._recv()
        return result # TODO: Parse into list

    def get_level_data(self, level_id: int) -> str:
        self._send(f'SELECT levelFile FROM Level WHERE levelId={level_id}')
        result = self._recv()
        return result

    def get_level_comments(self, level_id: int) -> list:
        self._send(f'SELECT * FROM Comments WHERE levelId={level_id}')
        result = self._recv()
        return result # TODO: Parse into list

    def submit_new_level(self, level_string_representation: str, level_name: str, username: str) -> bool:
        """Return true if successful"""
         # TODO: Figure out how to auto-generate primary key
        self._send(f'INSERT INTO Level VALUES ({level_name}, {level_string_representation}, {username})')
        result = self._recv()
        return result == "" # no error

    def create_comment(self, username: str, level_id: int, comment_text: str) -> bool:
        """Return true if successful"""
        # TODO: Figure out how to auto-generate primary key
        self._send(f'INSERT INTO Comments VALUES (0, 0, {comment_text}, {username}, {level_id})')
        result = self._recv()
        return result == "" # no error

    def like_comment(self, comment_id: int) -> bool:
        """Return true if successful"""
        self._send(f'UPDATE Comments SET likes = likes + 1)')
        result = self._recv()
        return result == "" # no error

    def dislike_comment(self, comment_id: int) -> bool:
        """Return true if successful"""
        self._send(f'UPDATE Comments SET dislikes = dislikes + 1)')
        result = self._recv()
        return result == "" # no error
        pass

    def get_user_data(self, username: str): # return TBD
        self._send(f'SELECT * FROM SUBMISSION JOIN SOLUTION WHERE userID={username}')
        solutions = self._recv()
        self._send(f'SELECT * FROM Comments WHERE userID={username}')
        comments = self._recv()
        return (solutions,comments) # TODO: Parse both into lists

    def search_for_level(self, search_str: str) -> list:
        # TODO: Levenshtien distance?
        self._send(f'SELECT * FROM Levels WHERE levelName LIKE {search_str}')
        result = self._recv()
        return result # TODO: Parse into list

    def search_for_user(self, search_str: str) -> list:
        # TODO: Levenshtien distance?
        self._send(f'SELECT * FROM Users WHERE username LIKE {search_str}')
        result = self._recv()
        return result # TODO: Parse into list

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