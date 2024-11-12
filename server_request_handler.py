import socket
import ast

port        = 65432
host        = None
buffer_size = None
sock        = None

def connect(param_host: str, param_buffer_size: int):
    """Open a connection to the backend. This should be called ONCE per client execution."""
    global host, buffer_size, sock
    host = param_host
    buffer_size = param_buffer_size    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Connected to backend at {host}:{port}")
    except socket.error as e:
        print(f"Connection error: {e}")
        sock = None

def _send(message):
    global sock
    if not sock:
        print("No connection")
        return
    try:
        sock.sendall(message.encode())
        print(f"Sent: {message}")
    except socket.error as e:
        print(f"Send error: {e}")

def _recv():
    global sock
    if not sock:
        print("No connection")
        return None
    try:
        data = sock.recv(buffer_size)
        message = data.decode()
        print(f"Received: {message}")
        return message
    except socket.error as e:
        print(f"Receive error: {e}")
        return None

def register(username: str, password: str) -> bool:
    """Return true if successful"""
    _send(f'INSERT INTO User VALUES (\"{username}\",\"{password}\")')
    result = _recv()
    return result == "Success" # no error

def login(username: str, password: str) -> bool:
    """Return true if successful"""
    _send(f'SELECT * FROM User WHERE username=\"{username}\" AND password=\"{password}\"')
    result = _recv()
    return result != '[]' # user is found

def submit_new_level(level_string_representation: str, level_name: str, username: str) -> bool:
    """Return true if successful"""
    # TODO: Figure out how to auto-generate primary key
    _send(f'INSERT INTO Level VALUES (\"{level_name}\", \"{level_string_representation}\", \"{username}\")')
    result = _recv()
    return result == 'Success' # no error

def get_level_data(level_name: int) -> tuple:
    """Returns a tuple like: ('LEVEL DATA AS STRING', 'user_creator_id')"""
    _send(f'SELECT levelFile, creatorId FROM Level WHERE levelName=\"{level_name}\"')
    result = ast.literal_eval(_recv())[0] # because normal eval() is just too gross
    return result

def submit_solution(username: str, level_name: int, movelist: str, score: int) -> bool:
    """return true if successful, DOES NOT VERIFY SOLUTION"""
    _send(f'INSERT INTO Submission VALUES (NULL, CURRENT_TIMESTAMP, \"{username}\", \"{level_name}\", {score}, \"{movelist}\")')
    result = _recv()
    return result == 'Success'

def get_user_completed_levels(username: str) -> list:
    """returns a list of strings, with all level names completed by the specified user"""
    _send(f'SELECT levelName FROM Submission WHERE userId = \"{username}\"')
    levels = [tup[0] for tup in ast.literal_eval(_recv())]
    return levels # TODO: Parse

def leaderboard_data_query(level_name: int) -> list:
    _send(f'SELECT userID, score, dos FROM Level JOIN Submission JOIN Solution WHERE levelId={level_name}')
    result = _recv()
    return result # TODO: Parse into list

def create_comment(username: str, level_name: int, comment_text: str) -> bool:
    """Return true if successful"""
    # TODO: Figure out how to auto-generate primary key
    _send(f'INSERT INTO Comments VALUES (0, 0, {comment_text}, {username}, {level_name})')
    result = _recv()
    return result == "" # no error

def like_comment(comment_id: int) -> bool:
    """Return true if successful"""
    _send(f'UPDATE Comments SET likes = likes + 1)')
    result = _recv()
    return result == "" # no error

def dislike_comment(comment_id: int) -> bool:
    """Return true if successful"""
    _send(f'UPDATE Comments SET dislikes = dislikes + 1)')
    result = _recv()
    return result == "" # no error

def get_user_comments(username: str) -> dict:
    _send(f'SELECT * FROM Comments WHERE userID={username}')
    comments = _recv()
    return (solutions,comments) # TODO: Parse both into lists

def get_level_comments(level_name: int) -> list:
    _send(f'SELECT * FROM Comments WHERE levelId={level_name}')
    result = _recv()
    return result # TODO: Parse into list

def get_user_created_levels(username: str) -> list:
    _send(f'SELECT levelName FROM Level WHERE creatorId = {username}')
    levels = _recv()
    return levels # TODO: Parse

def search_for_level(search_str: str) -> list:
    # TODO: Levenshtien distance?
    _send(f'SELECT * FROM Levels WHERE levelName LIKE {search_str}')
    result = _recv()
    return result # TODO: Parse into list

def search_for_user(search_str: str) -> list:
    # TODO: Levenshtien distance?
    _send(f'SELECT * FROM Users WHERE username LIKE {search_str}')
    result = _recv()
    return result # TODO: Parse into list

def rate_level(username: str, rating: int, difficulty: int, level_name: str) -> bool:
    _send(f'INSERT OR REPLACE INTO Rating VALUES ({rating}, {difficulty}, {username}, {level_name})')
    return _recv() == ''

def close():
    """Close connection to the backend"""
    if sock:
        try:
            sock.close()
            print("Connection closed.")
        except socket.error as e:
            print(f"Error closing connection: {e}")
        finally:
            sock = None
    else:
        print("Connection was already closed.")

if __name__ == '__main__':
    # if you run this file, it will perform unit tests,
    # if you want the tests to work, make sure you delete project_database.db and start the server
    connect('localhost',2048)
    assert(sock != None)
    login_succ_1 = login('joe miner', 'pickaxesarecool38')
    assert(login_succ_1 == False)
    register_succ = register('joe miner', 'pickaxesarecool38')
    assert(register_succ == True)
    login_succ_2 = login('joe miner', 'pickaxesarecool38')
    assert(login_succ_2 == True)
    test_level_str = ''
    test_level_str_2 = ''
    with open('board1.txt','r') as b1:
        test_level_str = b1.read()
    with open('board2.txt','r') as b2:
        test_level_str_2 = b2.read()
    
    submit_level_succ = submit_new_level(test_level_str, 'joe miners bad day', 'joe miner')
    assert(submit_level_succ == True)
    get_level_out = get_level_data('joe miners bad day')
    assert(get_level_out == (test_level_str,'joe miner'))
    submit_sol_succ = submit_solution('joe miner', 'joe miners bad day', '<<>>V^^s', 220)
    assert(submit_sol_succ == True)

    submit_level_succ = submit_new_level(test_level_str_2, 'hardest level ever', 'joe miner')
    assert(submit_level_succ == True)
    get_level_out = get_level_data('hardest level ever')
    assert(get_level_out == (test_level_str_2,'joe miner'))
    submit_sol_succ = submit_solution('joe miner', 'hardest level ever', '<<>>V^^s', 220)
    assert(submit_sol_succ == True)

    completed_levels = get_user_completed_levels('joe miner')


