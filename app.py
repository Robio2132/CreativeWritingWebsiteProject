from flask import Flask, render_template
from views import main as main_blueprint
from models import db, User
from auth import auth_blueprint
from flask_login import LoginManager

app = Flask(__name__)

#App configuration:
app.config['SECRET_KEY'] = 'secret keyyyyy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Register the routes from views.py
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)



@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
