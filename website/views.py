from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from .models import Expense, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    one_month_ago = datetime.now() - timedelta(days=30)

    daily_expenses = (
        db.session.query(
            db.func.date(Expense.date).label("date"),
            db.func.sum(
                db.func.coalesce(Expense.debit, 0) -
                db.func.coalesce(Expense.credit, 0)
            ).label("total")
        )
        .filter(Expense.user_id == current_user.id, Expense.date >= one_month_ago)
        .group_by(db.func.date(Expense.date))
        .order_by(db.func.date(Expense.date))
        .all()
    )

    dates = [row.date for row in daily_expenses]
    totals = [float(row.total or 0) for row in daily_expenses]

    return render_template("dashboard.html", user=current_user, expense=get_total_expense(), budget=get_budget(), dates=dates, totals=totals)


@views.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():

    user = User.query.get(current_user.id)

    if request.method == 'POST':
                    
        category_name = request.form.get('category')
        category_budget = request.form.get('categoryBudget')
        
        if category_name.capitalize() in user.categories.split(','):
            flash('Category already exists', category='error')
        elif len(category_name) < 1:
            flash('Category name too short', category='error')
        elif int(category_budget) < 1:
            flash('Budget must be greater than 0', category='error')
        else:
            new_categories = str(user.categories) + ',' + category_name.capitalize()
            new_budgets = str(user.budgets) + ',' + str(category_budget)

            user.categories = new_categories
            user.budgets = new_budgets
            db.session.commit()

            flash('Category added', category='success')

    total_expenses = {}
    for category in current_user.categories.split(','):
        total_expenses[category] = 0

    try:
        category_expenses = db.session.query(Expense.category, db.func.sum(Expense.debit), db.func.sum(Expense.credit)).filter(Expense.user_id == current_user.id).group_by(Expense.category).all()

        for i, (category, debit, credit) in enumerate(category_expenses):
            debit = debit or 0
            credit = credit or 0
            total_expenses[category] = int(debit - credit)

    except TypeError:
        pass

    return render_template("budget.html", user=current_user, total_expense=get_total_expense(), total_budget=get_budget(), category_wise_expenses=total_expenses)


@views.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
            
            debit = request.form.get('debit')
            credit = request.form.get('credit')
            description = request.form.get('description')
            category = request.form.get('category')

            if debit and credit:
                 flash('Cannot add debit and credit.', category='error')

            elif not (debit or credit):
                 flash('Please enter debit or credit amount.', category='error')

            elif len(description) < 2:
                 flash('Description is too short.', category='error')

            else:
                new_expense = Expense(debit=debit, credit=credit, description=description, category=category, user_id=current_user.id)
                db.session.add(new_expense)
                db.session.commit()
                flash('Expense added', category='success')

    return render_template("expense.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    expense = json.loads(request.data)
    expenseId = expense['expenseId']
    expense = Expense.query.get(expenseId)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()

    return jsonify({})


def get_budget():
    budget_amount = 0
    
    user = User.query.get(current_user.id)
    for budget in user.budgets.split(','):
        budget_amount += int(budget)

    return budget_amount


def get_total_expense():

    try:
        total_debit = int(db.session.query(db.func.sum(Expense.debit)).filter(Expense.user_id == current_user.id).scalar())
        total_credit = int(db.session.query(db.func.sum(Expense.credit)).filter(Expense.user_id == current_user.id).scalar())
        total_expense = total_debit - total_credit
    except TypeError:
        total_expense = 0

    return total_expense


@views.route('/delete-category', methods=['POST'])
def delete_category():
    
    user = User.query.get(current_user.id)
    categories = user.categories.split(',')
    budgets = user.budgets.split(',')
    
    data = json.loads(request.data)
    category_to_delete = data['category']

    Expense.query.filter_by(category=category_to_delete, user_id=current_user.id).update({"category": "General"})
    
    if category_to_delete in categories:
        removed_budget = budgets.pop(categories.index(category_to_delete))
        budgets[0] = str(int(budgets[0]) + int(removed_budget))
        categories.remove(category_to_delete)

        new_categories, new_budgets = "", ""
        for i, category in enumerate(categories):
            new_categories += f',{category}' if i > 0 else category
        for i, budget in enumerate(budgets):
            new_budgets += f',{budget}' if i > 0 else budget

        user.categories = new_categories
        user.budgets = new_budgets

    db.session.commit()

    return jsonify({})


@views.route('/edit-category', methods=['POST'])
def edit_category():
    old_category_name = request.form.get("old_category")
    category_name = request.form.get("category_name")
    category_budget = request.form.get("budget")
    
    user = User.query.get(current_user.id)
    categories = user.categories.split(',')
    budgets = user.budgets.split(',')
  
    category_name = category_name.capitalize() if category_name else ''
        
    if category_name in categories:
        flash('Category already exists', category='error')
    elif len(category_name) < 1:
        flash('Category name too short', category='error')
    elif int(category_budget) < 1:
        flash('Budget must be greater than 0', category='error')
    elif old_category_name in categories:

        budgets[categories.index(old_category_name)] = category_budget
        new_budgets = ""
        for i, budget in enumerate(budgets):
            new_budgets += f',{budget}' if i > 0 else budget
            
        user.budgets = new_budgets    

        if old_category_name != "General":      

            Expense.query.filter_by(category=old_category_name, user_id=current_user.id).update({"category": category_name})

            categories[categories.index(old_category_name)] = category_name
            new_categories = ""

            for i, category in enumerate(categories):
                new_categories += f',{category}' if i > 0 else category
            
            user.categories = new_categories
            
    
        flash('Category edited', category='success')
        db.session.commit()

    return redirect(url_for('views.budget'))
