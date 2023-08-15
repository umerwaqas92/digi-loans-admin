from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import databse.db_service as db

about_bp = Blueprint('api', __name__)

@about_bp.route('/about')
def about():
    return 'This is the about page.'


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
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    full_name = request.args.get('full_name', '')
    date_of_birth=request.args.get('date_of_birth', None)
    address = request.args.get('address', '')
    phone_num = request.args.get('phone_num', '')
    branch=request.args.get('branch', None)

    
    hash_password = generate_password_hash(password, method='sha256')

    user=db.get_user_by_email(email=email)
    if(user!=None):
        return jsonify({"Error":"Email already used!!"})

    db.create_user(email=email, password=hash_password,role_id=1, full_name=full_name,phone_number=phone_num,date_of_birth=date_of_birth,address=address,branchBy=branch)
    # db.update_user(email=email, password=hash_password,role_id=1, full_name=full_name,phone_number=phone_num,date_of_birth=date_of_birth,address=address)
