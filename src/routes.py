from flask import redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, current_user
from src import app, db, login_manager
from src.models import USER, EXPENSE
from src.forms import Register_Form, Login_Form, Add_expense, Edit_expense
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route('/')
def redirect_from_home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard',id=current_user.id, username=current_user.username))
    
    form = Register_Form()
    if form.validate_on_submit():
        username= form.name.data
        password= form.password.data
        if len(username) < 8 or len(password) < 8:
            return render_template('register.html', form=form, error='Username and password must be 8 or above characters long!')
        
        check_username = db.session.query(USER).filter_by(username=username).first()
        if check_username:
            return render_template('register.html', form=form, error="Account already exists!")
        
        user = USER(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard',id=current_user.id, username=current_user.username))
    
    form = Login_Form()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        user = db.session.execute(db.select(USER).where(USER.username == username)).scalar_one_or_none()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)  
            return redirect(url_for('dashboard',id=user.id, username=username))
        else:
            return render_template('login.html', form=form, error='Incorrect password or username!')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('redirect_from_home'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(USER, user_id)

@app.route('/Dashboard/<int:id>/<string:username>', methods=['GET', 'POST'])
def dashboard(id, username):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    user_expenses = db.session.execute(db.select(EXPENSE).where(EXPENSE.user_id == id).order_by(EXPENSE.id)).scalars().all()

    return render_template('dashboard.html', username=username, id=id, expenses=user_expenses)

@app.route('/Dashboard/<int:id>/<string:username>/Add', methods=['GET', 'POST'])
def add(id, username):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    form = Add_expense()
    if form.validate_on_submit():
        expense_name = form.name.data
        expense_description = form.description.data
        expense_to_add = EXPENSE(name=expense_name, info=expense_description, user_id=id, time=datetime.now().strftime("%Y-%b-%d  %H:%M%p"))

        db.session.add(expense_to_add)
        db.session.commit()
        return render_template('add_expense.html', form=form, id=id, username=username, msg='Success')
        
    return render_template('add_expense.html', form=form, id=id, username=username)

@app.route('/Dashboard/<int:id>/<string:username>/Edit/<int:expense_id>', methods=['GET', 'POST'])
def edit(id, username, expense_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    form = Edit_expense()
    expense= db.session.execute(db.select(EXPENSE).where(EXPENSE.id == expense_id)).scalar_one_or_none()
    if form.validate_on_submit():
        new_name = form.name.data
        new_description = form.description.data

        if new_name and new_name.strip():
            expense.name = new_name
        
        if new_description and new_description.strip():
            expense.info = new_description
        
        db.session.commit()

        return render_template('edit_expense.html', form=form, id=id, username=username, expense_id=expense_id ,expense=expense, msg="Changes saved")
    return render_template('edit_expense.html', form=form, id=id, username=username, expense_id=expense_id, expense=expense)

@app.route('/Dashboard/<int:id>/<string:username>/Delete/<int:expense_id>', methods=['GET', 'POST'])
def delete(id, username, expense_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    expense = db.session.execute(db.select(EXPENSE).where(EXPENSE.id == expense_id)).scalar_one_or_none()
    try:
        db.session.delete(expense)
        db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for('dashboard', id=id, username=username))


@app.route('/Dashboard/<int:id>/<string:username>/DELETE_ALL', methods=['GET', 'POST'])
def DELETE_ALL(id, username):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    expenses = db.session.execute(db.select(EXPENSE).where(EXPENSE.user_id == id)).scalars().all() 

    for expense in expenses:
        db.session.delete(expense)
    db.session.commit()

    return redirect(url_for('dashboard', id=id, username=username))
