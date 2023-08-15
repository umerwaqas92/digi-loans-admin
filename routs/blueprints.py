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
    users_branches=db.get_branch_user()
    
    return jsonify(users_branches)


@about_bp.route('/api/signup', methods=['POST'])
def api_signup():
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    retyped_password = request.args.get('retyped_password', '')
    full_name = request.args.get('full_name', '')
    if(password!=retyped_password):
        return jsonify({"error":"Passwords do not match"})

    hash_password = generate_password_hash(password, method='sha256')

    db.signup_user(email=email, password=hash_password,role_id=1, full_name=full_name,phone_number=None,date_of_birth=None,address="")