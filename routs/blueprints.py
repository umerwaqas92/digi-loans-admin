from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import databse.db_service as db
import databse.disabled_manage as disabled_managedb
import databse.comnet_manage as comnet_managedb
import databse.user_document as user_document
import os
import time
from databse.models import User
import json

about_bp = Blueprint('api', __name__)


@about_bp.route('/api/get_users', methods=['GET'])
def get_users():
    users=db.get_users_super_admin()
    
    return jsonify(users)


@about_bp.route('/api/get_branches', methods=['GET'])
def get_branches():
    users_branches = db.get_branch_user()
    
    # Assuming users_branches is a list of lists containing branch data
    branches = []
    for branch_data in users_branches:
        branch = {
            "id": branch_data[0],
            "email": branch_data[1],
            "password": branch_data[2],
            "some_number": branch_data[3],
            "name": branch_data[4],
            "join_date": branch_data[5],
            "location": branch_data[6],
            "phone": branch_data[7],
            "created_at": branch_data[8],
            "updated_at": branch_data[9]
        }
        branches.append(branch)
    
    return jsonify(branches)


@about_bp.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.json  # Use request.json for POST requests

    email = data.get('email', '')
    password = data.get('password', '')
    full_name = data.get('full_name', '')
    date_of_birth = data.get('date_of_birth', None)
    address = data.get('address', '')
    phone_num = data.get('phone_num', '')
    branch = data.get('branch', None)

    hash_password = generate_password_hash(password, method='sha256')

    user = db.get_user_by_email(email=email)
    if user is not None:
        return jsonify({"status": False, "data": None, "code": 400, "message": "Email already used!!"})
    else:
        try:
            user_id=db.create_user(email=email, password=hash_password, role_id=4, full_name=full_name, phone_number=phone_num, date_of_birth=date_of_birth, address=address, branchBy=branch,createdBy=None)
            user=db.get_user(user_id=user_id)
            doc=user_document.get_user_document_by_id(user_id=user[0])
            user_data = {
                "id": user[0],
                "email": user[1],
                "role_id": user[3],
                "full_name": user[4],
                "phone_number": user[7],
                "date_of_birth": user[5],
                "address": user[6],
                "branchBy": user[12],
                "created_at": user[8],
                "updated_at": user[9],
                "profile_image":db.get_user_image(user[2]),
                "adhar_card":doc[2],
                "pan_card":doc[3],
            }
            return jsonify({"status": True, "data": None, "code": 200, "message": "User created successfully","user":user_data})
        except Exception as e:
            return jsonify({"status": False, "data": None, "code": 500, "message": "Failed to create user: " + str(e)})

@about_bp.route('/api/profile_image_update', methods=['POST'])
def api_profile_image_update():
    user_id = request.args.get('user_id', '')

    file=request.files['image']
    user_profile_image=file.read()
    #save to staticstatic/uploads/user_profile/20230807-154903.jpg
    filename = user_profile_image.filename

            
    file_name=time.strftime("%Y%m%d-%H%M%S")+"."+filename.split(".")[-1]
    file_path = os.path.join("static/uploads/user_profile", file_name)
    user_profile_image.save(file_path)
    db.update_user_image(user_id,file_path.replace("static/",""))

    return jsonify({"status":True,"data":None,"code":200,"message":"Image updated successfully"})


@about_bp.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        if not data:
            return jsonify({"status": False, "code": 400, "message": "Malformed request"})

        email = data.get('email', '')
        password = data.get('password', '')
        print("Got email and pass: ", email, password)

        user = db.get_user_by_email(email=email)
        if user is None:
            return jsonify({"status": False, "code": 400, "message": "Email or password is wrong!!"})

        is_blocked_user = disabled_managedb.get_disabled_user(user_id=user[0])
        if is_blocked_user == 1:
            return jsonify({"status": False, "code": 400, "message": "User is blocked!!"})

        if check_password_hash(user[2], password):
            doc=user_document.get_user_document_by_id(user_id=user[0])
            user_data = {
                "id": user[0],
                "email": user[1],
                "role_id": user[3],
                "full_name": user[4],
                "phone_number": user[7],
                "date_of_birth": user[5],
                "address": user[6],
                "branchBy": user[12],
                "created_at": user[8],
                "updated_at": user[9],
                "profile_image":db.get_user_image(user[2]),
                "adhar_card":doc[2],
                "pan_card":doc[3],
            }

            return jsonify({"status": True, "code": 200, "message": "User login successfully", "user": user_data})
        else:
            return jsonify({"status": False, "code": 400, "message": "Email or password is wrong!!"})
    except Exception as e:
        return jsonify({"status": False, "code": 500, "message": "An error occurred", "error": str(e)})



@about_bp.route('/api/get_user_applications', methods=['GET'])
def get_user_applications():
    user_id = request.args.get('user_id', '')
    applications = db.get_loan_applications_for_user(user_id=user_id)
    print("user id", user_id)
    
    final_data = []
    for application in applications:
        rawcomments=comnet_managedb.get_ap_comments (application[0])
        comments=[]
        for comment in rawcomments:
            comments.append({
                "id": comment[0],
                "application_id": comment[1],
                "user_id": comment[2],
                "comment": comment[3],
                "status": comment[4],
                "created_at": comment[5],
                
            })

        data = {
        
           "applications":{ 
            "id": application[0],
            "user_id": application[1],
            "title": db.get_loan_product(application[2])[1],
            "description": application[3],
            "status": application[5],
            "created_at": application[6],
            "updated_at": application[7]},
            "comments":comments
        }
        final_data.append(data)
    
    return jsonify(final_data)


@about_bp.route('/api/user', methods=['GET'])
def api_user():
    user_id = request.args.get('user_id', '')
    user=db.get_user(user_id=user_id)
    adah_doc=user_document.get_user_document_by_id(user_id=user_id)
   
    if(user!=None):
        user=User(user_id=user[0],email=user[1],password=user[2],role_id=user[3],full_name=user[4],phone_number=user[5],date_of_birth=user[6],address=user[7],branch_by=user[8],created_time=user[9],updated_time=user[10])
        usejosn=json.dumps(user.__dict__)
        return jsonify({"status":True,"data":None,"code":200,"message":"",'data':usejosn})
    else:
        return jsonify({"status":False,"data":None,"code":400,"message":"User not found!!"})