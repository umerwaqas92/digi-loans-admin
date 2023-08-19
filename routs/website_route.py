from flask import Blueprint,request,jsonify,render_template,redirect,session
from werkzeug.security import generate_password_hash, check_password_hash
import databse.db_service as db
import databse.disabled_manage as disabled_managedb
import databse.comnet_manage as comnet_managedb
import databse.user_document as user_document
import os
import time
import json
import databse.models as models

website_route = Blueprint('website_route', __name__)


@website_route.route('/')
def index():
    return render_template("website/index.html")


@website_route.route('/services')
def services():
    # Initialize the category variable with None
    category = None

    # Get the 'category' query parameter from the URL
    category_id = request.args.get('category', None)

    forms = db.get_all_loan_products()
    categories = db.getCategories()

    if category_id:
        forms = db.get_all_loan_products_byCategory(category=category_id)
        category = db.getCategoryByID(category_id)
        final_forms = []

        for form in forms:
            final_forms.append(models.ProductForm(id=form[0], name=form[1], image=form[2], is_category= False))
            

        print(category)  # Print the category within the if-block
        return render_template("website/services.html", forms=final_forms, get_loan_product=db.get_loan_product, category=category)

    # Remove the print(category) from here

   
    # # final_forms = [(_from[0],_from[1],_from[2],False,) for _from in forms]
    # print(final_forms[0])

    # for cat in categories:
    #     form={
    #         cat[0],
    #         cat[1],
    #         cat[2],
    #         True

    #     }
    #     final_forms.append(form)

    final_forms = []
    # for cat in categories[1:6]:
    #     form = models.ProductForm(id=cat[0], name=cat[1], image=cat[2], is_category=True)
    #     final_forms.append(form)

    # for form in forms:
    #     final_forms.append(models.ProductForm(id=form[0], name=form[1], image=form[2], is_category= False))

    for i in [8, 5,2, 7,1,4,  1, 3, 4,  6]:
        category=db.getCategoryByID(i)
        category_id=category[0]
        print(category_id,category[1])

        if(category_id==8):
            products=db.get_all_loan_products_byCategory(category=category[0])
            for product in products:
                form = models.ProductForm(id=product[0], name=product[1], image=product[2], is_category=False)
                final_forms.append(form)
            
        
        if category_id==1:
            products=db.get_all_loan_products_byCategory(category=category[0])
            for product in products:
                form = models.ProductForm(id=product[0], name=product[1], image=product[2], is_category=False)
                final_forms.append(form)

        if(category_id!=8 and category_id!=1):
            form = models.ProductForm(id=category[0], name=category[1], image=category[2], is_category=True)
            final_forms.append(form)





    return render_template("website/services.html", forms=final_forms, get_loan_product=db.get_loan_product, category=category)


@website_route.route('/lenders')
def lenders():
    return render_template("website/lenders.html")


@website_route.route('/website/contact')
def contact():
    return render_template("website/contact.html")

@website_route.route('/aboutus')
def aboutus():
    return render_template("website/aboutus.html")


@website_route.route('/support')
def support():
    return render_template("website/support.html")


@website_route.route('/emi_calculator')
def emi_calculator():
    return render_template("website/emi_calculator.html")



# templates/website/support/adityabirla.html
# templates/website/support/axisbankmanager.html
@website_route.route('/support/adityabirla')
def adityabirla():
    return render_template("website/support/adityabirla.html")

@website_route.route('/support/axisbankmanager')
def axisbankmanager():
    return render_template("website/support/axisbankmanager.html")