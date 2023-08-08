import databse.db_service as db

# Create operation
def create_ap_comment(app_id, user_id, comment, status):
    connection = db.connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO AppComment (app_id, user_id, comment, status) VALUES (?, ?, ?, ?)",
                       (app_id, user_id, comment, status))
        connection.commit()
        return cursor.lastrowid  # Return the ID of the newly created comment
    finally:
        cursor.close()
        connection.close()

# Read operation
def get_ap_comment(comment_id):
    connection = db.connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM AppComment WHERE id=?", (comment_id,))
        return cursor.fetchone()  # Return a single comment as a tuple
    finally:
        cursor.close()
        connection.close()

# Read operation
def get_ap_comments(app_id):
    connection = db.connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM AppComment WHERE app_id=?", (app_id,))
        return cursor.fetchall()  # Return comments as a list of tuples
    finally:
        cursor.close()
        connection.close()

# Update operation
def update_ap_comment(comment_id, new_comment, new_status):
    connection = db.connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE AppComment SET comment=?, status=? WHERE id=?", (new_comment, new_status, comment_id))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

# Delete operation
def delete_ap_comment(comment_id):
    connection = db.connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM AppComment WHERE id=?", (comment_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()
