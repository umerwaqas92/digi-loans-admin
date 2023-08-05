# blueprints.py
from flask_app import Blueprint


# Create the Blueprint object
bp_other_routes = Blueprint('other_routes', __name__)

# Define a route within the Blueprint
@bp_other_routes.route('/api/get_forms_List', methods=['GET'])
def get_forms_list_api():
    categories=db.getCategories()
    
    form_json=[]
    for category in categories:
        forms_list=db.get_forms_by_category(7)
        _form_list=[]
        for form in forms_list:
            # print(form)
          
            _form_list.append({"title":form[2],"image":"static/"+form[7],"link":"form/"+str(form[0]),})
        
        if(category[0]!=1):
             sub_category_json={"image_sub":"static/"+category[2],"link_sub":"form/"+str(category[0]),"title_sub":category[1],"services_sub":_form_list}
             form_json.append(sub_category_json)
        else:
             form_json.append(_form_list)


    return jsonify(form_json)


