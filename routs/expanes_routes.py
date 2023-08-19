from flask import Blueprint,request,jsonify,session,render_template,redirect

import databse.expanes_manage as expanes_manage

expanes_routes = Blueprint('expanes_routes', __name__)


@expanes_routes.route('/dashboard/expenses')
def expenses():
    categories=expanes_manage.get_all_categories()
    user_id=session['user'][0]
    expanes_list=expanes_manage.get_all_expenses(user_id)
    
    return render_template("expanes.html",categories=categories,expanes_list=expanes_list)


@expanes_routes.route('/dashboard/expenses/add',methods=['POST'])
def expenses_add():
    expanes_title=request.form.get('expanes_title')
    expanes_amount=request.form.get('expanes_amount')
    expanes_categpry=request.form.get('expanes_categpry')
    expanes_date=request.form.get('expanes_date')
    user_id=session['user'][0]
    expanes_manage.create_expense(user_id,expanes_title,expanes_amount,expanes_categpry,expanes_date)
    
    
    return redirect('/expenses')

@expanes_routes.route('/dashboard/expenses_remove_item',methods=['POST'])
def expenses_remove_item():
   
    expane_id=request.form.get('expanes_id')
    expanes_manage.delete_expense(expane_id)
    
    
    return redirect('/expenses')

@expanes_routes.route('/dashboard/expenses_update_item',methods=['POST'])
def expenses_update_item():
   
    expane_id=request.form.get('expanes_id')
    expanes_title=request.form.get('expanes_title')
    expanes_amount=request.form.get('expanes_amount')
    expanes_categpry=request.form.get('expanes_categpry')
    expanes_date=request.form.get('expanes_date')

    expanes_manage.update_expense(expane_id,expanes_title,expanes_amount,expanes_categpry,expanes_date)
    
    
    return redirect('/expenses')