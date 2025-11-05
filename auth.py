from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db, User, Use
from flask_login import login_user, login_required, logout_user

# Create a blueprint
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        #Get the username and password. 
        username = request.form.get('username')
        password = request.form.get('password')
        
        #Confirmt that they are an existing user. 
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for('auth.login'))
        
        #Create the new user and set their passwrod. 
        new_user = User(username=username)
        new_user.set_password(password)
        
        # Add and commit the user to the database
        db.session.add(new_user)
        db.session.commit()
        
    # in the same file
    @auth_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.todo'))
        
        return render_template('form.html')
    


    @auth_blueprint.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))
   