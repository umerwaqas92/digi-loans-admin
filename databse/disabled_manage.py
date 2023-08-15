import databse.db_service as db

# Create or Update operation based on user_id
def create_or_update_disabled_user(user_id, disabled):
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("INSERT OR REPLACE INTO disabled_user (user_id, disabled) VALUES (?, ?)",
                           (user_id, disabled))
            new_user_id = cursor.lastrowid
            return new_user_id
    finally:
        connection.close()

# Read operation - Get a single user by user_id
def get_disabled_user(user_id):
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT disabled FROM disabled_user WHERE user_id = ?", (user_id,))
            user_disabled = cursor.fetchone()
            if user_disabled is not None:
                return user_disabled[0]  # Return the value of the "disabled" column
            else:
                return False  # User is not found
    finally:
        connection.close()

# Delete operation - Delete a user by user_id
def delete_disabled_user(user_id):
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM disabled_user WHERE user_id = ?", (user_id,))
    finally:
        connection.close()

# Example usage
new_user_id = create_or_update_disabled_user(1, True)
print("Created/Updated user ID:", new_user_id)

user = get_disabled_user(1)
print("Retrieved user:", user)

delete_disabled_user(1)
print("User deleted.")
