import jwt
import datetime
import databse.db_service as db



def create_token(user_id, expiration_minutes=30):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, db.SECRET_KEY, algorithm='HS256')
    return token

def store_token(user_id, token):
    connection = db.connect_db()
    cursor = connection.cursor()

    # Ensure the token is in string format
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    expiration = jwt.decode(token, db.SECRET_KEY, algorithms=['HS256'])['exp']
    cursor.execute('INSERT INTO tokens (user_id, token, expiration) VALUES (?, ?, ?)',
                   (user_id, token, expiration))
    connection.commit()
    connection.close()


def get_user_token(user_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT token FROM tokens WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    connection.close()
    
    if row:
        return row[0]
    return None

def invalidate_token(token):
    connection = db.connect_db()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM tokens WHERE token = ?', (token,))
    connection.commit()
    connection.close()

