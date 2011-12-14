from datetime import datetime

class Comment(object):
    def __init__(self, author, author_url, title, content, date=None):
        self.author = author
        self.author_url = author_url
        self.title = title
        self.content = content
        self.date = date if date else datetime.now()

def create_comment_table(connection):
        tables = connection.execute('''
            SELECT name FROM SQLITE_MASTER WHERE name = ?
        ''', ('comment',)).fetchall()
        if not tables:
            connection.execute('''
                CREATE TABLE comment (
                    author      VARCHAR(50),
                    author_url  VARCHAR(50), 
                    title       VARCHAR(100),
                    content     TEXT,
                    date        TIMESTAMP
                )''')
            connection.commit()

def save_comment(connection, comment):
    params = (
            comment.author, comment.author_url, comment.title, 
            comment.content, comment.date
    )
    connection.execute('''
        INSERT INTO comment (author, author_url, title, content, date)
        VALUES (?, ?, ?, ?, ?)
        ''', params)
    connection.commit()

def get_all_comments(connection):
    rows = connection.execute('''
        SELECT author, author_url, title, content, date 
        FROM comment ORDER BY date
    ''')
    return [Comment(*row) for row in rows]
