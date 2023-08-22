from flask import Flask, request, jsonify,render_template,flash,session,redirect,url_for,Blueprint,send_file
import json
from databse.db_service import *
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import time
import databse.application_relation_manage as ap_relation
import databse.comnet_manage as commentdb
import databse.user_document as user_documentdb
import logging
import openpyxl
import datetime
import databse.disabled_manage as disabledb
from routs.blueprints import about_bp
from routs.expanes_routes import expanes_routes
from routs.website_route import website_route






app = Flask(__name__)
app.secret_key = 'app'  # Replace 'your_secret_key_here' with a unique and secure string
CORS(app)  # Add this line to enable CORS support for the entire app
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Set maximum request size to 16 MB (adjust as needed)
logging.basicConfig(level=logging.ERROR)  # Set the logging level to capture errors and above
logging.basicConfig(filename='app.log', level=logging.ERROR)

# db_expanies.init_app(app)  # Initialize SQLAlchemy with the Flask app




app.register_blueprint(about_bp)
app.register_blueprint(expanes_routes)
app.register_blueprint(website_route)




msg=""
# Home route
@app.route('/dashboard')
def dashboard():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))
    total_branhes_count=0
    total_sub_admin_count=0
    total_dsa_count=0
    total_users_count=0
    total_pending_applications=0

    if(session["role"][0]==1):
        total_branhes_count=len(get_branch_user())
        total_sub_admin_count=len(get_all_sub_admins())
        total_dsa_count=len(get_all_dsa())
        total_users_count=len(get_all_users())
        total_pending_applications=len(get_loan_applications_pending())

    if(session["role"][0]==2):
        total_branheses=get_branch_userByUserId(session["user"][0])
        total_dsas=get_all_dsa_byUser(user_id=session["user"][0])
        total_users=[]
        total_users.extend(total_dsas)
        




        total_branhes_count=len(total_branheses)

        total_dsa_count=len(total_dsas)
        total_users_count=len(get_all_usersbyUserId(user_id=session["user"][0]))
        total_pending_applications=len(get_loan_applications_pending())


    if(session["role"][0]==3):
        total_branhes_count=len(get_branch_userByUserId(session["user"][0]))
        dsa_users=get_all_dsa_byUserforBranh(user_id=session["user"][0])
        total_dsa_count=len(dsa_users)
        # for dsa in dsa_users:
          
        #     total_pending_applications+=len(get_loan_applications_for_user(user_id=dsa[0]))

        total_users_count=len(get_all_usersbyUserId(user_id=session["user"][0]))
        # total_pending_applications=len(get_loan_applications_pending())


    applications=[]#get_loan_applications(1)

    apps_relations=ap_relation.read_all_ap_relations_by_user(user_id=session["user"][0])
    
    if(session["role"][0]==1):
        applications=get_loan_applications_pending()
    elif (session["role"][0]>3):
        applications=get_loan_applications_for_userPending(user_id=session["user"][0])


    else:
        if(apps_relations != None):
            for app in apps_relations:
                print(app[1])
                applcation=get_loan_application(app[1])
                if(applcation[5]=="pending"):
                    applications.append(applcation)

        # Convert the JSON string to a Python object
   
   





    return render_template("vertical/widgets.html",total_users_count=total_users_count,total_pending_applications=len(applications),total_branhes_count=total_branhes_count,total_sub_admin_count=total_sub_admin_count,total_dsa_count=total_dsa_count)
# user-profile


@app.route('/db')
def db():
    if not ('logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))

    # Path to the database file
    db_file_path = 'databse/digi_loans.db'

    return send_file(db_file_path, as_attachment=True)

@app.errorhandler(Exception)
def handle_error(e):
    logging.exception("An error occurred: %s", str(e))
    return render_template('error.html',e=e), 500


@app.route('/dashboard/adduser',methods=['GET', 'POST'])
def adduser():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))
    roles = get_roles()
    
    
    if(session["role"][0]==1):
       roles= roles[session["role"][0]-1:5]
    elif(session["role"][0]==3):
       roles = roles[session["role"][0]:4]

    else:
        roles = roles[session["role"][0]:4]

   
    if request.method == 'POST':
        # This block will only be executed if the request is a POST request.
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_num')
        email_address = request.form.get('email_address')
        email_address=email_address.rstrip()

        address = request.form.get('address')
        password = request.form.get('password')
        retype_password = request.form.get('retype_password')

        password=password.rstrip()

        role = request.form.get('chose_role')
        date_of_birth=request.form.get('date_of_birth')
        password_has= generate_password_hash(password, method='sha256')
        createdBy=session["user"][0]

        pan_card=request.form.get('pan_card')
        aadhar_card=request.form.get('adhaar_card')

        if(password!=retype_password):
           return render_template("add_user.html", roles=roles,error="Passwords must be matched!! ")
        # print(retype_password)
        # print(password)


            

       





            

        print(session["role"])

        if(session["role"][0])==3:#bracnh
            branchBy=session["user"][0]
        else:
            branchBy=request.form.get('chose_branch')


        user_id=create_user(full_name=full_name,email=email_address,password=password_has,role_id=role,date_of_birth=date_of_birth,address=address,phone_number=phone_number,createdBy=createdBy,branchBy=branchBy)
        update_user_password(user_id=user_id,password=password_has)
        user_documentdb.create_user_document(user_id,pan_card,aadhar_card)

        file = request.files['user_photo']
        if(file != None and user_id!=None):
            filename = file.filename
            #random file name
            file_name=time.strftime("%Y%m%d-%H%M%S")+"."+filename.split(".")[-1]
            file_path = os.path.join("static/uploads/user_profile", file_name)
            file.save(file_path)
            add_user_image(user_id,file_path.replace("static/",""))
            print("file has been save!! ",file_path)
        else:
            render_template("add_user.html", roles=roles,error="User not created")

        return render_template("add_user.html", roles=roles,error="User created successfully")


    else:
       
        branches=get_branch_user()
        return render_template("add_user.html", roles=roles,branches=branches)

@app.route('/dashboard/change_password', methods=['POST', 'GET'])
def change_password():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect("/login")


    pass_has=session['user'][2]
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        retype_password = request.form.get('retype_password')
        if(check_password_hash(pass_has, old_password)):
            if(new_password==retype_password):
                hashed_password = generate_password_hash(new_password, method='sha256')
                update_user_password(session['user'][0],hashed_password)
                return redirect("/logout")
            else:
                return render_template("vertical/user_change_password.html",error="New password and retype password not match",user_id=session["user"][0],image=session['image'],user=session['user'],role=session['role'],user_doc=session['user_doc'])
        else:
            return render_template("vertical/user_change_password.html",error="Old password not match",user_id=session["user"][0],image=session['image'],user=session['user'],role=session['role'],user_doc=session['user_doc'])


    return render_template("vertical/user_change_password.html",user_id=session["user"][0],image=session['image'],user=session['user'],role=session['role'],user_doc=session['user_doc'])


@app.route('/create_form_data', methods=['POST'])
def create_form_data():
    form_name = request.form['form_name']
    form_image = request.files['form_image']
    zone = request.form['zone']
    form_link = request.form['form_link']
    productsCategory=request.form['productsCategories']


    field_labels = request.form.getlist('field_label[]')
    field_types = request.form.getlist('field_type[]')
    field_options = request.form.getlist('field_options[]')
    field_required = request.form.getlist('field_required[]')

    if form_image:
        filename = form_image.filename
        form_image.save(os.path.join("static/uploads", filename))
        form_image_path = os.path.join("static/uploads", filename)

    else:
        form_image_path = ""

    form_image_path=form_image_path.replace("static/","")
    filed_data_final=[]

    for i in range(len(field_labels)):
        field_data = {
            "field_label": field_labels[i],
            "field_type": field_types[i],
            "required": True if field_required[i] == "true" else False
        }
        if field_types[i] == "select"   or field_types[i] == "radio":
            field_data["options"] = field_options[i].split(',')
        filed_data_final.append(field_data)
        # print(f"{i+1}: {field_data}")

        
    id=create_loan_product(product_image=form_image_path,product_name=form_name,zone_id=zone,productsCategory=productsCategory)
    create_product_form(id,form_name,filed_data_final,form_link)

    print(form_link)



    return "Form created successfully!"

    

@app.route('/delete_form', methods=['POST'])
def delete_form():
    form_id = int(request.form['form_id'])
    delete_product_form(form_id)
    delete_loan_product(product_id=form_id)
    return redirect("/dashboard/forms")






# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['inputEmailAddress']
#         password = request.form['inputChoosePassword']
#         password=password.stripe()
#         email=email.stripe()
#         remember_me = request.form.get('remember_me')  # Get the value of the "Remember Me" checkbox (if exists)
#         # hashed_password = generate_password_hash(password, method='sha256')


#         print(email)
#         print(password)
#         user=login_user(email=email,password=password)
#         if(user==None):
#             return render_template("vertical/auth-basic-signin.html",error="Invalid credentials")
            
#         check_pass=check_password_hash(user[2], password)
#         print(check_pass)

        
#         if user!=None and check_pass:
#             # flash("You are logged in as {}".format(email))
#             session['logged_in'] = True
#             session['user_email'] = email
#             session['role'] = get_role(user[3])
#             session['user'] = user
#             session['image'] = get_user_image(user[0])
#             session['user_doc'] = user_documentdb.get_user_document_by_id(user[0])



            

#             return redirect("/loan_applications")
        
#         else:
#             # flash("Invalid credentials", "danger")
#             return render_template("vertical/auth-basic-signin.html",error="Invalid credentials")
#     else:  
#         return render_template("vertical/auth-basic-signin.html",)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['inputEmailAddress'].rstrip()
        password = request.form['inputChoosePassword']

        user = login_user(email, password)



        
        if user:
            if(disabledb.get_disabled_user(user_id=user[0])):
                return render_template("vertical/auth-basic-signin.html", error="Your account has been disabled!!")
            session['logged_in'] = True
            session['user_email'] = email
            session['role'] = get_role(user[3])
            session['user'] = user
            session['image'] = get_user_image(user[0])
            session['user_doc'] = user_documentdb.get_user_document_by_id(user[0])

            return redirect("/dashboard/loan_applications")
        else:
            error_message = "Invalid credentials"
            return render_template("vertical/auth-basic-signin.html", error=error_message)
    else:
        return render_template("vertical/auth-basic-signin.html")

@app.route('/forms_creator', methods=['GET', 'POST'])
def create_form():
    if(request.method=="POST"):
        form_title=request.form['formName']
        # form_fields=request.form['jsonData']
        form_image=request.files['formImage']
        print(form_title)
        print(request)
        # create_loan_application(1,1,1,form_fields,"rejected")
        return "form created"
    
    productsCategories=getCategories()
        

    return render_template("forms_creator.html",productsCategories=productsCategories)

@app.route('/dashboard/loan_applications')
def all_applications():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))
    

    applications=[]#get_loan_applications(1)

    apps_relations=ap_relation.read_all_ap_relations_by_user(user_id=session["user"][0])
    
    if(session["role"][0]==1):
        applications=get_loan_applications(1)
    elif (session["role"][0]>3):
        applications=get_loan_applications_for_user(user_id=session["user"][0])


    else:
        if(apps_relations != None):
            for app in apps_relations:
                print(app[1])
                applcation=get_loan_application(app[1])
                applications.append(applcation)

        # Convert the JSON string to a Python object
    for index, application in enumerate(applications):
        
        applications[index] = (
            application[0],  # Keep other tuple elements unchanged
             application[1],  # Keep other tuple elements unchanged
              application[2],  # Keep other tuple elements unchanged
               application[3],  # Keep other tuple elements unchanged
            json.loads(application[4]),  # Convert JSON string to Python object
            application[5],  # Keep other tuple elements unchanged
            application[6],  # Keep other tuple elements unchanged
            application[7],
            
        )
        product_form_info = get_product_form(application[2])
        # print(application[2])
        # print("product_form_info>>>>>>> ",product_form_info)
        if product_form_info is not None:
            applications[index] += (product_form_info[2],)
        else:
            # Handle the case when product_form_info is None
            applications[index] += (product_form_info,)  # Or any
    # print(product_form_info)

    final_applications = [tuple(_app) + (commentdb.get_ap_comments(_app[0]),) for _app in applications]
    # print("final_applications ",len(applications))


    flash('This is a flash message!', 'info')  # 'info' is the category of the message


    return render_template("vertical/all-applocations.html",applications=final_applications,msg=msg,get_user=get_user)

# Function to fix the JSON data in the input string and convert it to a dictionary
def fix_json_data(input_str):
    try:
        data_dict = json.loads(input_str)
    except json.JSONDecodeError:
        # If JSONDecodeError occurs, assume the input_str is already a dictionary
        data_dict = json.loads(input_str.replace("'", "\""))  # Replace single quotes with double quotes
    return data_dict


@app.route('/chat')
def user_chat():
    return render_template("vertical/app-chat-box.html")

@app.route('/dashboard/user_profile', methods=['GET', 'POST'])
def user_profile():
    if(session['logged_in']==False):
        return redirect(url_for('login'))
    if(request.method=="POST"):
        full_name=request.form['full_name']
        # email=request.form['email_address']
        phone=request.form['phone']
        address=request.form['address']
        date_of_birth=request.form['date_of_birth']
        user_profile_image=request.files['profile_photo']
        adhhar_card=request.form['adhaar_card']
        pan_card=request.form['pan_card']


        
        if(user_profile_image):
            filename = user_profile_image.filename
            #random file name
            user_id=session['user'][0]
            file_name=time.strftime("%Y%m%d-%H%M%S")+"."+filename.split(".")[-1]
            file_path = os.path.join("static/uploads/user_profile", file_name)
            user_profile_image.save(file_path)
            update_user_image(user_id,file_path.replace("static/",""))
            session['image']=get_user_image(user_id)
            print("file has been save!! ",file_path)


        update_user(session['user'][0],full_name=full_name,phone_number=phone,address=address,date_of_birth=date_of_birth)
        user_documentdb.update_or_create_user_document(session['user'][0],adhhar_card,pan_card)
        
        session['user']=get_user(session['user'][0])
        session['user_doc'] = user_documentdb.get_user_document_by_id(session['user'][0])

        return redirect(url_for('/dashboard/user_profile'))
        
    
    return render_template("vertical/user_profile.html")


@app.route('/dashboard/user_view/<int:user_id>', methods=['GET', 'POST'])
def user_view(user_id):
    user=get_user(user_id)
    role=get_role(user[3])
    image=get_user_image(user_id)
    roles=get_roles()
    user_doc=user_documentdb.get_user_document_by_id(user_id)
    return render_template("vertical/user_profile_other.html",user=user,role=role,image=image,roles=roles,user_id=user_id,user_doc=user_doc)



@app.route('/dashboard/user_edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    if(session['logged_in']==False):
        return redirect(url_for('login'))
    if(request.method=="POST"):
        full_name=request.form['full_name']
        # email=request.form['email_address']
        phone=request.form['phone']
        address=request.form['address']
        date_of_birth=request.form['date_of_birth']
        user_profile_image=request.files['profile_photo']
        role=request.form['chose_role']
        password=request.form['user_password']
        adhar_card=request.form['adhaar_card']
        pan_card=request.form['pan_card']
        if(session["role"][0]==1):
            chose_branch=request.form['chose_branch']
            chose_subadmin=request.form['chose_subadmin']


            if(chose_branch):
                update_user_branch(user_id=user_id,branh_id=chose_branch)
            if(chose_subadmin):
                update_user_sub_admin(user_id=user_id,subadmin=chose_subadmin)






        # print("user_profile_image ", user_profile_image and user_profile_image.filename != '' and user_profile_image.content_length == 0)

        if user_profile_image and user_profile_image.filename != '' and user_profile_image.content_length == 0:
            filename = user_profile_image.filename
            #random file name
            print("file has been found")
            
            file_name=time.strftime("%Y%m%d-%H%M%S")+"."+filename.split(".")[-1]
            file_path = os.path.join("static/uploads/user_profile", file_name)
            user_profile_image.save(file_path)
            imageUploaderUpdate(user_id,file_path.replace("static/",""))
           
            print("file has been save!! ",file_path)


        update_user(user_id,full_name=full_name,phone_number=phone,address=address,date_of_birth=date_of_birth)
        
        update_user_role(role_id=role,user_id=user_id)

        try:
             user_documentdb.update_or_create_user_document(user_id,adhar_card,pan_card)
        except:
            pass

        if(password is not None and password.strip() != ""):
            hashed_password = generate_password_hash(password, method='sha256')
            update_user_password(user_id,hashed_password)
        
      

        user=get_user(user_id)
        role=get_role(user[3])
        image=get_user_image(user_id)
        roles=get_roles()
        branches=get_branch_user()
        sub_admins=get_all_subadminds_user()

        user_doc=user_documentdb.get_user_document_by_id(user_id)
        



        return render_template("vertical/user_profile_edit.html",user=user,role=role,image=image,roles=roles,user_id=user_id,user_doc=user_doc,branches=branches,sub_admins=sub_admins)
        
    user=get_user(user_id)
    role=get_role(user[3])
    image=get_user_image(user_id)
    roles=get_roles()
    user_doc=user_documentdb.get_user_document_by_id(user_id)
    branches=get_branch_user()
    sub_admins=get_all_subadminds_user()

    return render_template("vertical/user_profile_edit.html",user=user,role=role,image=image,roles=roles,user_id=user_id,user_doc=user_doc,branches=branches,sub_admins=sub_admins)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('user_email', None)
    return redirect(url_for('login'))


@app.route('/download_application_data/<int:application_id>', methods=['GET'])
def get_application_data(application_id):
    application = get_loan_application(application_id)
    # application = get_application(application_id)
    # data_dict = fix_json_data(application[5])
    # print(data_dict)
    # 
    json_data = json.dumps(application)
    return jsonify(application)


@app.route('/dashboard/users')
def admin_users():
    user_id=session["user"][0]
    role_id=session["role"][0]

  
    if(role_id==1):
        users = get_users_super_admin()
    elif (role_id==2):
        raw_users=get_users_sub_admin(user_id)
        
        users=[]
        users.extend(raw_users)
        for user in raw_users:
            raw_sub_users=get_users_sub_admin(user[0])
            users.extend(raw_sub_users)

        

    elif (role_id==3):
        users=get_branch_users_branchdBy(user_id)


    final_users = [tuple(user) + (get_role(user[3])[1],get_user_image(user[0],),user_documentdb.get_user_document_by_id(user[0]),disabledb.get_disabled_user(user[0])) for user in users]
    
    
    # print("final_users_Users--->",final_users[1])



    return render_template("users_list.html",users=final_users,get_user=get_user)

@app.route('/dashboard/forms')
def admin_forms():
    forms=get_forms()
    print(forms)

    return render_template("forms_list.html",forms=forms)



# Route to handle form submission
@app.route('/dashboard/updateLoanStatus', methods=['POST'])
def update_loan_status():
    # Get the value selected from the dropdown
    status = request.form.get('rmAssignedDropdown')
    application_id = request.form.get('application_id')
    comment=request.form.get('comment')







    print(f"Selected status: {status}")
    print(f"Selected status: {application_id}")



    
    update_application_status(application_id, status)
    commentdb.create_ap_comment(app_id=application_id,user_id=session["role"][0],comment=comment,status=status)


    return redirect("/dashboard/loan_applications")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('inputEmailAddress', '')  # Using default value ''
        password = request.form.get('inputChoosePassword', '')  # Using default value ''
        retyped_password = request.form.get('inputChoosePasswordConfirm', '')  # Using default value ''
        full_name = request.form.get('full_name', '')  # Using default value ''
        zone=request.form.get('inputSelectCountry', '')  # Using default value ''

        if(password!=retyped_password):
            return render_template("vertical/auth-basic-signup.html",error="Passwords do not match")
        
        try:
            signup_user(email=email, password=password,role_id=zone, full_name=full_name,phone_number=None,date_of_birth=None,address="")
            
            session['logged_in'] = True
            session['user_email'] = email

            return redirect("/dashboard/loan_applications")
        except Exception as e:
            print(e)
            return render_template("vertical/auth-basic-signup.html",error=e)

        # Your logic to handle the form data here...

        return render_template("vertical/auth-basic-signup.html")
    return render_template("vertical/auth-basic-signup.html")




@app.route('/dashboard/edit-form/<int:form_id>', methods=['GET', 'POST'])
def edit_form(form_id):

    if request.method == 'POST':
            form_name = request.form['form_name']
            form_image = request.files['form_image']
            zone = request.form['zone']
            image_path = request.form['image_path']
            form_link = request.form['form_link']

            productsCategory=request.form['productsCategories']


            field_labels = request.form.getlist('field_label[]')
            field_types = request.form.getlist('field_type[]')
            field_options = request.form.getlist('field_options[]')
            field_required = request.form.getlist('field_required[]')

            if form_image:
                filename = form_image.filename
                form_image.save(os.path.join("static/uploads", filename))
                form_image_path = os.path.join("static/uploads", filename)

            else:

                form_image_path =image_path

            form_image_path=form_image_path.replace("static/","")
            filed_data_final=[]

            for i in range(len(field_labels)):
                field_data = {
                    "field_label": field_labels[i],
                    "field_type": field_types[i],
                    "required": True if field_required[i] == "true" else False
                }
                if field_types[i] == "select"   or field_types[i] == "radio":
                    field_data["options"] = field_options[i].split(',')
                filed_data_final.append(field_data)
                # print(f"{i+1}: {field_data}")

                
            update_loan_product(product_id=form_id,product_image=form_image_path,product_name=form_name,zone_id=zone,productsCategory=productsCategory)
            
            update_product_form2(form_id=form_id,new_form_title=form_name,new_form_link=form_link,new_form_fields=filed_data_final)

            print(form_id)



            return redirect("/dashboard/forms")
        
        
    else:
        form_product=get_loan_product(form_id)
        form_data=get_product_form(form_id)

        form_fields = [
       
        ]
        form_name=form_product[1]
        form_link=form_data[6]

        form_image=form_product[2]
        form_category=form_product[6]

        form_fileds_data=form_data[3]
        print(form_link)

        try:
            form_fields=json.loads(form_fileds_data)
        except:
             pass
        productsCategories=getCategories()
        
        return render_template('form_editor.html',form_fields=form_fields,form_name=form_name,form_image=form_image,form_category=form_category,productsCategories=productsCategories,form_link=form_link,form_id=form_id)

def get_products_data(categories):
    data = {"products": []}

    for category in categories:
        forms = get_forms_by_category(category)
        if forms:
            product = {
                "category": category,
                "forms": []
            }
            for form in forms:
                # Replace the following attributes with the actual attributes of your forms
                form_data = {
                    "title": form.title,
                    "description": form.description,
                    "link": form.link
                }
                product["forms"].append(form_data)
            data["products"].append(product)

    return data



@app.route('/form/<int:form_id>', methods=['GET', 'POST'])
def show_form(form_id):
    if request.method == 'POST':
        # Handle form submission and file upload
        form_data = get_product_form(form_id)
        if form_data:
            form_fields_json = get_product_form(form_id)[3]  # Assuming form_fields is stored at index 3
            req_value = request.form.to_dict()
            redirectUrl = request.form.get('redirectUrl')
            dsa_id = request.form.get('dsa_id') #user id

            form_values = []
            # print(req_value)
            # # keys=json.loads(req_value).keys()
            # print(form_fields_json)

            for filed in json.loads(form_fields_json):
               
            #    if filed['field_type'] == 'heading' or filed['field_type'] == 'paragraph':
            #     continue 
        
              try:
                    # print(filed)
                    if filed['field_type'] == 'file':
                        # print("Saving file", request.files[filed["field_label"]])
                        uploaded_file = request.files[filed["field_label"]]
                        if uploaded_file:
                            file_path = os.path.join('static/uploads/user_data', uploaded_file.filename)
                            uploaded_file.save(file_path)
                            filed["value"] = file_path
                            
                    else:
                            filed["value"]=req_value[filed["field_label"]]
                
                    form_values.append(filed)
              except Exception as e:
                  print("got errror >>>>>",e)
                  pass 

          
            app_id= create_loan_application(dsa_id,form_id,form_id,form_values,"pending")
            
            dsa_user = get_user(dsa_id)
            if(dsa_user==None):
                return ("DSA code not found ",dsa_id)
            # print(dsa_user)
            branch_user = get_user(dsa_user[12])
            # print(branch_user)
          
            # print(dsa_user[0],branch_user[11],)
            # print(dsa_user[0],dsa_user[12],)

            # sub_admin_user = get_sub_admin(branch_user[0])

            if(app_id):
                if(branch_user[11]!=None):
                    ap_relation.create_ap_relation(app_id,branch_user[11])
                if(dsa_user[12]!=None):
                    ap_relation.create_ap_relation(app_id,dsa_user[12])

            # print(form_values)
            
            
            # print(filed)
        if(redirectUrl != None and redirectUrl!=""):
            return redirect(redirectUrl)

        return  "Form submitted"

    else:
        form_data = get_product_form(form_id)

        if form_data:
            form_title = form_data[2]  # Assuming form_title is stored at index 2
            form_image = get_loan_product(form_id)[2]
            print(form_image)

            form_fields_json = form_data[3]  # Assuming form_fields is stored at index 3

            # Convert form_fields JSON string to Python dictionary
            form_fields = json.loads(form_fields_json)
            redirectUrl=form_data[6]
            
            # if form_data[6] != None and form_data[2] != "":
            #    return redirect(form_data[6])
            # print(form_data[6])

            user_id=request.args.get('user_id', type=int)
            if(user_id==None):
                user_id=""


            return render_template('form_template.html', form_id=form_id, form_title=form_title, form_fields=form_fields,form_image=form_image,redirectUrl=form_data[6],user_id=user_id)
        else:
            return "Form not found."



# API List
# @app.route('/api/get_forms_List', methods=['GET'])
# def get_forms_list_api():
#     categories=getCategories()
    
#     form_json=[]
#     for category in categories:
        
#         forms_list=get_forms_by_category(category[0])
#         _form_list=[]
#         for form in forms_list:
#             _form_list.append({"title":form[2],"image":"static/"+form[7],"link":"form/"+str(form[0]),})
        
#         if(category[0]!=1):
#              sub_category_json={"image":"static/"+category[2],"link":"form/"+str(category[0]),"title":category[1],"services_sub":_form_list}
#              form_json.append(sub_category_json)
#         else:
#              form_json.append(_form_list)
        



#     return jsonify(form_json)

# @app.route('/api/get_forms_List', methods=['GET'])
# def get_forms_list_api():
#     categories = getCategories()

    
#     form_json = []
#     for i in [7,4,1,6,0,2,3,4,5]:
#         category=categories[i]
#         forms_list = get_forms_by_category(category[0])
#         _form_list = []
#         for form in forms_list:
#             _form_list.append({
#                 "title": form[2],
#                 "image": "static/" + form[7],
#                 "link": "form/" + str(form[0]),
#             })
        
#         if category[0] != 1 and category[0] != 8:
#             sub_category_json = {
#                 "image": "static/" + category[2],
#                 "link": "form/" + str(category[0]),
#                 "title": category[1],
#                 "services_sub": _form_list
#             }
#             form_json.append(sub_category_json)
#         else:
#             form_json.extend(_form_list)

#     return jsonify(form_json)

@app.route('/api/get_forms_List', methods=['GET'])
def get_forms_list_api():
    categories = getCategories()
    
    form_json = []
    processed_categories = set()  # Keep track of processed categories
    
    for i in [7, 4, 1, 6, 0, 2, 3, 4, 5]:
        category = categories[i]
        if category[0] not in processed_categories:  # Check if category is not processed
            forms_list = get_forms_by_category(category[0])
            _form_list = []
            for form in forms_list:
                _form_list.append({
                    "title": form[2],
                    "image": "static/" + form[7],
                    "link": "form/" + str(form[0]),
                })

            if category[0] != 1 and category[0] != 8:
                sub_category_json = {
                    "image": "static/" + category[2],
                    "link": "form/" + str(category[0]),
                    "title": category[1],
                    "services_sub": _form_list
                }
                form_json.append(sub_category_json)
            else:
                form_json.extend(_form_list)

            processed_categories.add(category[0])  # Mark category as processed

    return jsonify(form_json)


@app.route('/disabled_user/<int:user_id>', methods=['GET'])
def disabled_user(user_id):
    prevoud_val=disabledb.get_disabled_user(user_id=user_id)
    disabled=True
    
    if(prevoud_val!=None):
        if(prevoud_val==1):
            disabled=False
        else:
            disabled=True
            
    
    disabledb.create_or_update_disabled_user(user_id=user_id,disabled=disabled)
    
    return redirect("/dashboard/users")



@app.route('/export_applications_data', methods=['GET'])
def export_applications_data():
    
    applications = get_loan_applications(0)

    if(applications == None or len(applications)==0):
        return redirect("/dashboard/loan_applications")
    # Create an Excel workbook and add user data to a worksheet
    wb = openpyxl.Workbook()
    ws = wb.active

    # Write header row

    roles=get_roles()
    header = (
        "date", "dsa code", "dsa mobile", "dsa name", "Loan name","Status","CUSTOMER Name","CUSTOMER Mobile"
    )
    ws.append(header)


    apllications2=[]
    for application in applications:
        try:
            user=get_user(application[1])
            loan=get_loan_product(application[2])
                                # "date",        "dsa code",   "dsa mobile", "dsa name","dsa email", "Loan name","Status"
            apllications2.append((application[6],application[1],user[7],user[4],loan[1],application[5]))
           
        except Exception as e:
            pass

    print("apllications2 ---> ",len(apllications2))

    # print("User ---> ",apllications2[0])
    # final_users = [tuple(_app) + (commentdb.get_ap_comments(_app[0]),) for _app in user]


    # Write user data rows
    for application in apllications2:
        # Convert the JSON string to a Python object

        ws.append(application)

    # Save the Excel file to the specified path
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    file_name = f"application_data_{formatted_datetime}.xlsx"
    file_path = os.path.join("static/report", file_name)


    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    wb.save(file_path)
    

    return send_file(file_path, as_attachment=True)

@app.route('/export_user_data', methods=['GET'])
def export_user_data():
    users = get_users_super_admin()

    # Create an Excel workbook and add user data to a worksheet
    wb = openpyxl.Workbook()
    ws = wb.active

    # Write header row

    roles=get_roles()
    header = (
        "id", "email", "Role", "Name",  "Address",
        "Phone number"
    )
    ws.append(header)

    users2=[]
    for user in users:
        users2.append((user[0],user[1],roles[user[3]][1],user[4],user[6],user[7]))
    # print("User ---> ",users[0])

    print("User ---> ",users2[0])
    # final_users = [tuple(_app) + (commentdb.get_ap_comments(_app[0]),) for _app in user]


    # Write user data rows
    for user in users2:
        # Convert the JSON string to a Python object

        ws.append(user)

    # Save the Excel file to the specified path
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    file_name = f"user_data_{formatted_datetime}.xlsx"
    file_path = os.path.join("static/report", file_name)


    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    wb.save(file_path)
    

    return send_file(file_path, as_attachment=True)

#api



if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    with app.app_context():
            # db_expanies.create_all()  # Create the database tables
            app.run(debug=True)
