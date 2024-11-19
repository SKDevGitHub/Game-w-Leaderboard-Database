
CREATE TABLE IF NOT EXISTS User (
    username TEXT PRIMARY KEY,
    password TEXT
);

CREATE TABLE IF NOT EXISTS Level (
    levelName TEXT PRIMARY KEY,
    levelFile TEXT,
    creatorId TEXT NOT NULL,
    FOREIGN KEY (creatorId) REFERENCES User(username)
);

CREATE TABLE IF NOT EXISTS Comments (
    likes INTEGER,
    dislikes INTEGER,
    commentText TEXT,
    commentId INTEGER PRIMARY KEY,
    userId TEXT NOT NULL,
    levelName TEXT NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(username),
    FOREIGN KEY (levelName) REFERENCES Level(levelName)
);

CREATE TABLE IF NOT EXISTS Submission (
    submissionId INTEGER PRIMARY KEY,
    dos TEXT,
    userId TEXT NOT NULL,
    levelName TEXT NOT NULL,
    score INTEGER,
    movelist TEXT,
    FOREIGN KEY (userId) REFERENCES User(username),
    FOREIGN KEY (levelName) REFERENCES Level(levelName)
);

CREATE TABLE IF NOT EXISTS Rating (
    userRating INTEGER,
    diffRating INTEGER,
    userName TEXT NOT NULL,
    levelName TEXT NOT NULL,
    PRIMARY KEY (userName, levelName),
    FOREIGN KEY (userName) REFERENCES User(username),
    FOREIGN KEY (levelName) REFERENCES Level(levelName)
);
