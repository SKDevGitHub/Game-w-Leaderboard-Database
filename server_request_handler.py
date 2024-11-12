import socket
import ast
import Levenshtein

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
    _send(f'INSERT INTO Submission VALUES (NULL, STRFTIME(\'%Y-%m-%d %H:%M:%f\', \'NOW\'), \"{username}\", \"{level_name}\", {score}, \"{movelist}\")')
    result = _recv()
    return result == 'Success'

def get_user_completed_levels(username: str) -> list:
    """returns a set of strings, with all level names completed by the specified user"""
    _send(f'SELECT DISTINCT levelName FROM Submission WHERE userId = \"{username}\"')
    recv_raw = _recv()
    levels = [tup[0] for tup in ast.literal_eval(recv_raw)]
    return levels

def get_user_created_levels(username: str) -> list:
    _send(f'SELECT levelName FROM Level WHERE creatorId = \"{username}\"')
    recv_raw = _recv()
    levels = [tup[0] for tup in ast.literal_eval(recv_raw)]
    return levels

def leaderboard_data_query(level_name: int) -> list:
    """returns a list of tuples like: [(username1, score, timestamp), (username2, score, timestamp),...]"""
    _send(f'SELECT userId, score, dos FROM Submission WHERE levelName=\"{level_name}\"')
    recv_raw = _recv()
    result = ast.literal_eval(recv_raw)
    return result

def create_comment(comment_text: str, username: str, level_name: int) -> bool:
    """Return true if successful"""
    _send(f'INSERT INTO Comments VALUES (0,0,\"{comment_text}\",NULL,\"{username}\",\"{level_name}\")')
    result = _recv()
    return result == "Success"

def get_user_comments(username: str) -> list:
    _send(f'SELECT * FROM Comments WHERE userId=\"{username}\"')
    recv_raw = _recv()
    result = ast.literal_eval(recv_raw)
    return result

def get_level_comments(level_name: int) -> list:
    _send(f'SELECT * FROM Comments WHERE levelName=\"{level_name}\"')
    recv_raw = _recv()
    result = ast.literal_eval(recv_raw)
    return result

def like_comment(comment_id: int) -> bool:
    """Return true if successful"""
    _send(f'UPDATE Comments SET likes = likes + 1 WHERE commentId = {comment_id}')
    result = _recv()
    return result == "Success"

def dislike_comment(comment_id: int) -> bool:
    """Return true if successful"""
    _send(f'UPDATE Comments SET dislikes = dislikes + 1 WHERE commentId = {comment_id}')
    result = _recv()
    return result == "Success"

def search_for_level(search_str: str) -> list:
    _send(f'SELECT levelName FROM Level')
    recv_raw = _recv()
    levels = [t[0] for t in ast.literal_eval(recv_raw)]
    levels.sort(key=lambda s: Levenshtein.distance(s,search_str))
    return levels

def search_for_user(search_str: str) -> list:
    _send(f'SELECT username FROM User')
    recv_raw = _recv()
    users = [t[0] for t in ast.literal_eval(recv_raw)]
    users.sort(key=lambda s: Levenshtein.distance(s,search_str))
    return users

def rate_level(username: str, rating: int, difficulty: int, level_name: str) -> bool:
    _send(f'INSERT OR REPLACE INTO Rating VALUES ({rating}, {difficulty}, \"{username}\", \"{level_name}\")')
    return _recv() == "Success"

def get_level_ratings(level_name: str) -> list:
    _send(f'SELECT AVG(userRating), AVG(diffRating) FROM Rating WHERE levelName = \"{level_name}\"')
    recv_raw = _recv()
    return tuple([float(r) for r in ast.literal_eval(recv_raw)[0]])

def close_connection():
    """Close connection to the backend"""
    global sock
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
    # if you want the tests to work, make sure you delete project_database.db then run the server locally
    
    # test connection, registration, login
    connect('localhost',2048)
    assert(sock != None)
    login_succ_1 = login('joe miner', 'pickaxesarecool38')
    assert(login_succ_1 == False)
    register_succ = register('joe miner', 'pickaxesarecool38')
    assert(register_succ == True)
    login_succ_2 = login('joe miner', 'pickaxesarecool38')
    assert(login_succ_2 == True)

    register('mo deghani', 'mo_money$$$')

    # test level submission
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
    submit_sol_succ = submit_solution('joe miner', 'joe miners bad day', '<<>>V^^s', 110)
    assert(submit_sol_succ == True)

    # test leaderboard
    submit_level_succ = submit_new_level(test_level_str_2, 'hardest level ever', 'joe miner')
    get_level_out = get_level_data('hardest level ever')
    submit_sol_succ = submit_solution('joe miner', 'hardest level ever', '<<>>V^^s', 220)
    submit_sol_succ = submit_solution('joe miner', 'hardest level ever', '<<>>V^^s', 220)
    submit_sol_succ = submit_solution('mo deghani', 'hardest level ever', '<<>>V^^s', 220)
    submit_sol_succ = submit_solution('joe miner', 'hardest level ever', '<<><><>>V^^s', 250)
    submit_sol_succ = submit_solution('mo deghani', 'hardest level ever', '<<V^^s', 100)

    completed_levels = get_user_completed_levels('joe miner')
    assert(completed_levels == ['joe miners bad day', 'hardest level ever'])

    created_levels = get_user_created_levels('joe miner')
    assert(created_levels == ['joe miners bad day', 'hardest level ever'])
    created_levels = get_user_created_levels('mo deghani')
    assert(created_levels == [])

    leaderboard = leaderboard_data_query('hardest level ever')
    assert(len(leaderboard) == 5)

    # test comments
    create_comment_succ = create_comment(
        'Dedicated students, distinguished colleagues, and dear friends: This level is too hard',
        'mo deghani',
        'joe miners bad day'
    )
    assert(create_comment_succ == True)
    create_comment(
        'To those who think this level is too hard: git gud',
        'joe miner',
        'joe miners bad day'
    )

    level_comments = get_level_comments('joe miners bad day')
    assert(len(level_comments) == 2)
    level_comments_2 = get_level_comments('hardest level ever')
    assert(len(level_comments_2) == 0)

    user_commments = get_user_comments('joe miner')
    assert(user_commments == [(
        0,0,
        'To those who think this level is too hard: git gud',
        2,
        'joe miner',
        'joe miners bad day'
    )])

    # test comment like/dislike
    like_comment_succ = like_comment(user_commments[0][3])
    assert(like_comment_succ == True)
    dislike_comment_succ = dislike_comment(user_commments[0][3])
    assert(dislike_comment_succ == True)

    user_commments = get_user_comments('joe miner')
    assert(user_commments == [(
        1,1,
        'To those who think this level is too hard: git gud',
        2,
        'joe miner',
        'joe miners bad day'
    )])

    # test search functionality
    level_results = search_for_level('joe minahs bday')
    assert(level_results == ['joe miners bad day', 'hardest level ever'])

    register('Stephen','Kautt')
    register('Ben', 'Sullins')
    register('Justin', 'Falejczyk')
    register('Eliot','Kimmel')
    register('Jacob', 'Meyers')

    user_results = search_for_user('mow degonnie')
    assert(user_results == [
        'mo deghani',
        'joe miner',
        'Ben',
        'Stephen',
        'Eliot',
        'Jacob',
        'Justin'
    ])

    # test level rating
    rate_succ = rate_level('mo deghani', 2, 10, 'joe miners bad day')
    assert(rate_succ == True)
    rate_level('joe miner', 10, 0, 'joe miners bad day')
    rate_level('mo deghani', 5, 8, 'hardest level ever')

    level_ratings = get_level_ratings('joe miners bad day')
    assert(level_ratings == (6.0,5.0))
    
    close_connection()


