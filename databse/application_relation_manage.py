import databse.db_service as db


# Create operation
def create_ap_relation(app_id, user_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO ap_relation (app_id, user_id) VALUES (?, ?)", (app_id, user_id))
        connection.commit()
        print("Record inserted successfully.")
    except Exception as e:
        connection.rollback()
        print("Error:", str(e))
    finally:
        connection.close()

# Read operation
def read_ap_relation(id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM ap_relation WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            print("ID:", row[0])
            print("App ID:", row[1])
            print("User ID:", row[2])
        else:
            print("Record not found.")
    except Exception as e:
        print("Error:", str(e))
    finally:
        connection.close()

# Update operation
def update_ap_relation(id, new_app_id, new_user_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE ap_relation SET app_id = ?, user_id = ? WHERE id = ?", (new_app_id, new_user_id, id))
        connection.commit()
        print("Record updated successfully.")
    except Exception as e:
        connection.rollback()
        print("Error:", str(e))
    finally:
        connection.close()

# Delete operation
def delete_ap_relation(id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM ap_relation WHERE id = ?", (id,))
        connection.commit()
        print("Record deleted successfully.")
    except Exception as e:
        connection.rollback()
        print("Error:", str(e))
    finally:
        connection.close()

# Read all ap_relation records by user ID
def read_all_ap_relations_by_user(user_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM ap_relation WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print("Error:", str(e))
    finally:
        connection.close()





def read_all_ap_relations_by_application(app_id):
    connection = db.connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM ap_relation WHERE app_id = ?", (app_id,))
        rows = cursor.fetchall()
        if rows:
            print("All ap_relation records for App ID:", app_id)
            for row in rows:
                print("ID:", row[0])
                print("App ID:", row[1])
                print("User ID:", row[2])
                print("-----")
        else:
            print("No records found for App ID:", app_id)
    except Exception as e:
        print("Error:", str(e))
    finally:
        connection.close()


