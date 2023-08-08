import sqlite3
import json
# Connect to the SQLite database
def connect_db():
    return sqlite3.connect('databse/digi_loans.db')

# Users Table CRUD operations
def create_user_(email, password, role_id, full_name, date_of_birth, address, phone_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO Users (email, password, role_id, full_name, date_of_birth, address, phone_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email, password, role_id, full_name, date_of_birth, address, phone_number))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error creating user:", e)
        conn.rollback()
        conn.close()
        return False

def get_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print("Error getting user:", e)
        conn.close()
        return None

def dsa_get_branch_id(dsa_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Users WHERE branchBy = ?', (dsa_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print("Error getting user:", e)
        conn.close()
        return None
    
def get_sub_admin(branch_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (branch_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print("Error getting user:", e)
        conn.close()
        return None

def update_user(user_id, full_name, date_of_birth, address, phone_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE Users
            SET full_name = ?, date_of_birth = ?, address = ?, phone_number = ?
            WHERE user_id = ?
        ''', (full_name, date_of_birth, address, phone_number, user_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error updating user:", e)
        conn.rollback()
        conn.close()
        return False
    
def update_user_password(user_id, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE Users
            SET password = ? WHERE user_id = ?
        ''', (password, user_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error updating user:", e)
        conn.rollback()
        conn.close()
        return False
    


def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error deleting user:", e)
        conn.rollback()
        conn.close()
        return False

# Roles Table CRUD operations
def create_role(role_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO Roles (role_name) VALUES (?)', (role_name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error creating role:", e)
        conn.rollback()
        conn.close()
        return False

def get_role(role_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Roles WHERE role_id = ?', (role_id,))
        role = cursor.fetchone()
        conn.close()
        return role
    except sqlite3.Error as e:
        print("Error getting role:", e)
        conn.close()
        return None
    
def get_roles():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Roles',)
        roles = cursor.fetchall()
        conn.close()
        return roles
    except sqlite3.Error as e:
        print("Error getting role:", e)
        conn.close()
        return None

def update_role(role_id, role_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('UPDATE Roles SET role_name = ? WHERE role_id = ?', (role_name, role_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error updating role:", e)
        conn.rollback()
        conn.close()
        return False

def delete_role(role_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Roles WHERE role_id = ?', (role_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error deleting role:", e)
        conn.rollback()
        conn.close()
        return False

# Zones Table CRUD operations
def create_zone(zone_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO Zones (zone_name) VALUES (?)', (zone_name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error creating zone:", e)
        conn.rollback()
        conn.close()
        return False

def get_zone(zone_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Zones WHERE zone_id = ?', (zone_id,))
        zone = cursor.fetchone()
        conn.close()
        return zone
    except sqlite3.Error as e:
        print("Error getting zone:", e)
        conn.close()
        return None

def update_zone(zone_id, zone_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('UPDATE Zones SET zone_name = ? WHERE zone_id = ?', (zone_name, zone_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error updating zone:", e)
        conn.rollback()
        conn.close()
        return False

def delete_zone(zone_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Zones WHERE zone_id = ?', (zone_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error deleting zone:", e)
        conn.rollback()
        conn.close()
        return False

# LoanProducts Table CRUD operations

def create_loan_product(product_name, product_image, zone_id,productsCategory):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO LoanProducts (product_name, product_image, zone_id,productsCategory)
            VALUES (?, ?, ?,?)
        ''', (product_name, product_image, zone_id,productsCategory))
        
        # Get the ID of the newly inserted row
        product_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return product_id
    except sqlite3.Error as e:
        print("Error creating loan product:", e)
        conn.rollback()
        conn.close()
        return None

def update_loan_product(product_id, new_product_name, new_product_image, new_zone_id, new_productsCategory):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE LoanProducts
            SET product_name = ?,
                product_image = ?,
                zone_id = ?,
                productsCategory = ?
            WHERE product_id = ?
        ''', (new_product_name, new_product_image, new_zone_id, new_productsCategory, product_id))

        conn.commit()
        conn.close()

        return True  # Return True to indicate successful update
    except sqlite3.Error as e:
        print("Error updating loan product:", e)
        conn.rollback()
        conn.close()
        return False  # Return False to indicate failure


def get_loan_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM LoanProducts WHERE product_id = ?', (product_id,))
        loan_product = cursor.fetchone()
        conn.close()
        return loan_product
    except sqlite3.Error as e:
        print("Error getting loan product:", e)
        conn.close()
        return None

def update_loan_product(product_id, product_name, product_image, zone_id, productsCategory):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE LoanProducts
            SET product_name = ?, product_image = ?, zone_id = ?, productsCategory = ?
            WHERE product_id = ?
        ''', (product_name, product_image, zone_id, productsCategory, product_id))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error updating loan product:", e)
        conn.rollback()
        conn.close()
        return False

def delete_loan_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM LoanProducts WHERE product_id = ?', (product_id,))
        conn.commit()
        conn.close()
       
        return True
    except sqlite3.Error as e:
        print("Error deleting loan product:", e)
        conn.rollback()
        conn.close()
        return False

# ProductForms Table CRUD operations
def create_product_form(product_id, form_title, form_fields, form_link):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Convert the form_fields dictionary to a JSON-formatted string
        form_fields_json = json.dumps(form_fields)

        # Use a parameterized query to prevent SQL injection
        cursor.execute('''
            INSERT INTO ProductForms (product_id, form_title, form_fields, form_link)
            VALUES (?, ?, ?, ?)
        ''', (product_id, form_title, form_fields_json, form_link))

        # Commit the changes to the database
        conn.commit()

        # Close the connection using the context manager (with statement)
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error creating product form:", e)

        # Rollback changes in case of an error
        conn.rollback()
        conn.close()
        return False

    
def update_product_form2(form_id, new_form_title, new_form_fields, new_form_link):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Convert the new_form_fields dictionary to a JSON-formatted string
        new_form_fields_json = json.dumps(new_form_fields)

        cursor.execute('''
            UPDATE ProductForms
            SET form_title = ?,
                form_fields = ?,
                form_link = ?
            WHERE form_id = ?
        ''', (new_form_title, new_form_fields_json, new_form_link, form_id))

        conn.commit()
        conn.close()
        print(form_id, " has been updated!!")

        return True  # Return True to indicate successful update
    except sqlite3.Error as e:
        print("Error updating product form:", e)
        conn.rollback()
        conn.close()
        return False  # Return False to indicate failur

def get_product_form(form_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM ProductForms WHERE form_id = ?', (form_id,))
        product_form = cursor.fetchone()
        conn.close()
        # print(product_form)
        return product_form
    except sqlite3.Error as e:
        print("Error getting product form:", e)
        conn.close()
        return None




def delete_product_form(form_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM ProductForms WHERE form_id = ?', (form_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error deleting product form:", e)
        conn.rollback()
        conn.close()
        return False
    

def get_user_image(user_id):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM UserProfile WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()  # Fetch one row, assuming you want to retrieve a single user's image data

        conn.commit()
        print("got image result for ",user_id," : ",result)
        return result  # Return the fetched result
    except sqlite3.Error as e:
        print("Error get_user_image:", e)
        if conn:
            conn.rollback()
        return None  # Return None to indicate an error


def add_user_image(user_id, user_image):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('Insert INTO UserProfile (user_id, image) VALUES (?, ?)', (user_id,user_image))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error add_user_image :", e)
        conn.rollback()
        conn.close()
        return False
    
def update_user_image(user_id, user_image):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('UPDATE UserProfile SET image = ? WHERE user_id = ?', (user_image, user_id))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error add_user_image :", e)
        conn.rollback()
        conn.close()
        return False

# LoanApplications Table CRUD operations
def create_loan_application(user_id, product_id, form_id, application_data, status):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        
        form_fields_json = json.dumps(application_data)
        cursor.execute('''
            INSERT INTO LoanApplications (user_id, product_id, form_id, application_data, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, product_id, form_id, form_fields_json, status))
        conn.commit()
        conn.close()
        print("created application")
       
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(">>>>>>>>>>>>>Error creating loan application:", e)
        conn.rollback()
        conn.close()
        return None
    

def update_application_status(application_id,new_status):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
                """
                UPDATE LoanApplications
                SET 
                    status = ?,
                    updated_time = CURRENT_TIMESTAMP
                WHERE
                    application_id = ?;
                """,
                (new_status, application_id))
    except:
        print("faile dto update the status")
        pass
    conn.commit()
    conn.close()



def get_users_super_admin():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT * FROM Users
        ''')
        users = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return users
    except sqlite3.Error as e:
        print("Error getting loan application:", e)
        conn.close()
        return None
    
def get_users_sub_admin():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT * FROM Users where role_id >2
        ''')
        users = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return users
    except sqlite3.Error as e:
        print("Error getting loan application:", e)
        conn.close()
        return None

def get_branch_users_branchdBy(branch_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT * FROM Users WHERE role_id > 2 AND branchBy = ?
        ''', (branch_id,))  
        users = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return users
    except sqlite3.Error as e:
        print("Error get_branch_users_branchdBy :", e)
        conn.close()
        return None
        
def get_branch_user():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT * FROM Users where role_id=3
        ''')
        users = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return users
    except sqlite3.Error as e:
        print("Error getting loan application:", e)
        conn.close()
        return None
    
def getCategories():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT * FROM ProductCategory
        ''')
        categories = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return categories
    except sqlite3.Error as e:
        print("Error getting  categories:", e)
        conn.close()
        return None    

def get_loan_applications(admin_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT * FROM LoanApplications
        ''')
        loan_applications = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return loan_applications
    except sqlite3.Error as e:
        print("Error getting loan application:", e)
        conn.close()
        return None

def get_loan_application(application_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM LoanApplications WHERE application_id = ?', (application_id,))
        loan_application = cursor.fetchone()
        conn.close()
        return loan_application
    except sqlite3.Error as e:
        print("Error getting loan application:", e)
        conn.close()
        return None

def update_loan_application(application_id, application_data, status):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE LoanApplications
            SET application_data = ?, status = ?
            WHERE application_id = ?
        ''', (application_data, status, application_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error updating loan application:", e)
        conn.rollback()
        conn.close()
        return False

def delete_loan_application(application_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM LoanApplications WHERE application_id = ?', (application_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error deleting loan application:", e)
        conn.rollback()
        conn.close()
        return False


def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        print("got user data ",user)

        if user:
            return user
        else:
            return None
    except sqlite3.Error as e:
        print("Error during login:", e)
        conn.close()
        return None

def get_forms_by_category(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                               SELECT
    pf.form_id,
    pf.product_id,
    pf.form_title,
    pf.form_fields,
    pf.created_time AS form_created_time,
    pf.updated_time AS form_updated_time,
    lp.product_name,
    lp.product_image,
    lp.zone_id,
    lp.created_time AS product_created_time,
    lp.updated_time AS product_updated_time
FROM
    ProductForms pf
INNER JOIN
    LoanProducts lp ON pf.product_id = lp.product_id
WHERE
    lp.productsCategory = ?


        ''', (category_id,))
        forms = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return forms
    except sqlite3.Error as e:
        print("Error getting loan forms:", e)
        conn.close()
        return None

def get_forms():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                                SELECT
    pf.form_id,
    pf.product_id,
    pf.form_title,
    pf.form_fields,
    pf.created_time AS form_created_time,
    pf.updated_time AS form_updated_time,
    lp.product_name,
    lp.product_image,
    lp.zone_id,
    lp.created_time AS product_created_time,
    lp.updated_time AS product_updated_time
FROM
    ProductForms pf
INNER JOIN
    LoanProducts lp ON pf.product_id = lp.product_id;


        ''')
        forms = cursor.fetchall()
        conn.close()
        # print(loan_applications)

        return forms
    except sqlite3.Error as e:
        print("Error getting loan forms:", e)
        conn.close()
        return None



# Signup function
def signup_user(email, password, role_id, full_name, date_of_birth, address, phone_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "This email is already used by another user!"

        cursor.execute('''
            INSERT INTO Users (email, password, role_id, full_name, date_of_birth, address, phone_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email, password, role_id, full_name, date_of_birth, address, phone_number))
        conn.commit()
        conn.close()
        return "User has been created !!"
    except sqlite3.Error as e:
        print("Error during signup:", e)
        conn.rollback()
        conn.close()
        return "Something went wrong try again!"
    


def create_user(email, password, role_id, full_name, date_of_birth, address, phone_number,createdBy,branchBy):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return None

        cursor.execute('''
            INSERT INTO Users (email, password, role_id, full_name, date_of_birth, address, phone_number,createdBy,branchBy)
            VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
        ''', (email, password, role_id, full_name, date_of_birth, address, phone_number,createdBy,branchBy))
    
        conn.commit()
        conn.close()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print("Error during signup:", e)
        conn.rollback()
        conn.close()
        return None