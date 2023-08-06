from flask import Flask, request, jsonify,render_template,flash,session,redirect,url_for,Blueprint
import json
from databse.db_service import *
import os
from flask_cors import CORS



app = Flask(__name__)
app.secret_key = 'app'  # Replace 'your_secret_key_here' with a unique and secure string
CORS(app)  # Add this line to enable CORS support for the entire app




msg=""
# Home route
@app.route('/')
def home():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))

    return redirect("/loan_applications")
# user-profile


@app.route('/adduser')
def adduser():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))

    return render_template("add_user.html")

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
        form_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        form_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

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
    return redirect("/forms")






@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['inputEmailAddress']
        password = request.form['inputChoosePassword']
        remember_me = request.form.get('remember_me')  # Get the value of the "Remember Me" checkbox (if exists)

        print(email)
        print(password)
        if email == 'admin@demo.com' and password == '123456':
            # flash("You are logged in as {}".format(email))
            session['logged_in'] = True
            session['user_email'] = email

            return redirect("/loan_applications")
        
        else:
            # flash("Invalid credentials", "danger")
            return render_template("vertical/auth-basic-signin.html",error="Invalid credentials")
    else:  
        return render_template("vertical/auth-basic-signin.html",)

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

@app.route('/loan_applications')
def all_applications():
    if not ( 'logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))
    

    applications=get_loan_applications(1)


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
        print(application[2])
        print("product_form_info>>>>>>> ",product_form_info)
        if product_form_info is not None:
            applications[index] += (product_form_info[2],)
        else:
            # Handle the case when product_form_info is None
            applications[index] += (product_form_info,)  # Or any
    # print(product_form_info)

   


    return render_template("vertical/all-applocations.html",applications=applications,msg=msg)

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

@app.route('/user_profile')
def user_profile():
    return render_template("vertical/user_profile.html")

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('user_email', None)
    return redirect(url_for('login'))


@app.route('/users')
def admin_users():
    users=get_users()

    return render_template("users_list.html",users=users)

@app.route('/forms')
def admin_forms():
    forms=get_forms()
    print(forms)

    return render_template("forms_list.html",forms=forms)



# Route to handle form submission
@app.route('/updateLoanStatus', methods=['POST'])
def update_loan_status():
    # Get the value selected from the dropdown
    status = request.form.get('rmAssignedDropdown')
    application_id = request.form.get('application_id')



    print(f"Selected status: {status}")
    print(f"Selected status: {application_id}")



    
    update_application_status(application_id, status)


    return redirect("/loan_applications")


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

            return redirect("/loan_applications")
        except Exception as e:
            print(e)
            return render_template("vertical/auth-basic-signup.html",error=e)

        # Your logic to handle the form data here...

        return render_template("vertical/auth-basic-signup.html")
    return render_template("vertical/auth-basic-signup.html")




@app.route('/edit-form/<int:form_id>', methods=['GET', 'POST'])
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
                form_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                form_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

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



            return redirect("/forms")
        
        
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

          
            create_loan_application(1,form_id,form_id,form_values,"pending")

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

            return render_template('form_template.html', form_id=form_id, form_title=form_title, form_fields=form_fields,form_image=form_image,redirectUrl=form_data[6])
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

@app.route('/api/get_forms_List', methods=['GET'])
def get_forms_list_api():
    categories = getCategories()

    
    form_json = []
    for i in [7,4,1,6,0,2,3,4,5]:
        category=categories[i]
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

    return jsonify(form_json)


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    

    app.run(debug=True)
