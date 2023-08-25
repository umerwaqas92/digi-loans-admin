import databse.db_service as db


def create_referral_user(user_id, referral_user_id):
    """
    Create a new referral user entry in the database.

    Args:
        user_id (int): The user ID.
        referral_user_id (int): The referral user ID.

    Returns:
        int: The ID of the newly created entry.
    """
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO ReferralUser (user_id, referral_user_id, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (user_id, referral_user_id)
            )
            new_entry_id = cursor.lastrowid
            return new_entry_id
    except Exception as e:
        print("An error occurred:", e)  # Handle the error appropriately
    finally:
        connection.close()

def get_all_referral_users():
    """
    Retrieve all referral user entries from the database.

    Returns:
        list: List of tuples representing referral user entries.
    """
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM ReferralUser")
            referral_users = cursor.fetchall()
            return referral_users
    except Exception as e:
        print("An error occurred:", e)  # Handle the error appropriately
    finally:
        connection.close()

def update_referral_user(user_id, referral_user_id, new_timestamp):
    """
    Update a referral user entry's timestamp in the database.

    Args:
        user_id (int): The user ID.
        referral_user_id (int): The referral user ID.
        new_timestamp (str): The new timestamp value.

    Returns:
        None
    """
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE ReferralUser SET timestamp = ? WHERE user_id = ? AND referral_user_id = ?",
                (new_timestamp, user_id, referral_user_id)
            )
    except Exception as e:
        print("An error occurred:", e)  # Handle the error appropriately
    finally:
        connection.close()

def delete_referral_user(user_id, referral_user_id):
    """
    Delete a referral user entry from the database.

    Args:
        user_id (int): The user ID.
        referral_user_id (int): The referral user ID.

    Returns:
        None
    """
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM ReferralUser WHERE user_id = ? AND referral_user_id = ?",
                (user_id, referral_user_id)
            )
    except Exception as e:
        print("An error occurred:", e)  # Handle the error appropriately
    finally:
        connection.close()


def get_all_referral_usersByUserID(user_id):
    """
    Retrieve all referral user entries for a specific user ID from the database.

    Args:
        user_id (int): The user ID.

    Returns:
        list: List of tuples representing referral user entries.
    """
    connection = db.connect_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM ReferralUser WHERE user_id = ?",
                (user_id,)
            )
            referral_users = cursor.fetchall()
            return referral_users
    except Exception as e:
        print("An error occurred:", e)  # Handle the error appropriately
    finally:
        connection.close()

