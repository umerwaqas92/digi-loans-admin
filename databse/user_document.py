import databse.db_service as db

# Create operation
def create_user_document(user_id, adhar_card, pan_card):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO UserDocument (user_id, adhar_card, pan_card) VALUES (?, ?, ?)",
                       (user_id, adhar_card, pan_card))
        connection.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted row
    except Exception as e:
        connection.rollback()
        print("Error creating user document:", e)
    finally:
        connection.close()

# Read operation
def get_user_document_by_id(user_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM UserDocument WHERE user_id=?", (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print("Error retrieving user document:", e)
    finally:
        connection.close()

# Update or create operation
def update_or_create_user_document(user_id, adhar_card, pan_card):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        # Check if the user document exists
        cursor.execute("SELECT * FROM UserDocument WHERE user_id=?", (user_id,))
        existing_document = cursor.fetchone()

        if existing_document:
            # Update the existing document
            cursor.execute("UPDATE UserDocument SET adhar_card=?, pan_card=? WHERE user_id=?",
                           (adhar_card, pan_card, user_id))
        else:
            # Create a new document
            cursor.execute("INSERT INTO UserDocument (user_id, adhar_card, pan_card) VALUES (?, ?, ?)",
                           (user_id, adhar_card, pan_card))

        connection.commit()
    except Exception as e:
        connection.rollback()
        # Handle the exception appropriately, e.g., log the error
        print("Error updating/creating user document:", e)
    finally:
        connection.close()


# Delete operation
def delete_user_document(document_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM UserDocument WHERE id=?", (document_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("Error deleting user document:", e)
    finally:
        connection.close()
