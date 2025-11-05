from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.integer, primary_key=True)
    username = db.Column(db.string(20), unique=True, nullable=False)
    password_hash = db.Column(db.string(128), nullabe=False)
    stories = db.relationship("Story", backref="author", lazy=True)
    
    
    def set_password(self, password):
        '''Hashes an inputed password.'''
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        '''Confirms that the password has been hashed.'''
        return check_password_hash(self.password_hash, password)
    
class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # Core fields “for now”
    title = db.Column(db.String(200), nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)

    # Useful toggles/metadata
    is_public = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # One to many relationship
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Optional convenience property
    @property
    def word_count(self) -> int:
        return len((self.body or "").split())

    def __repr__(self) -> str:
        return f"<Story {self.title!r} by {self.author_id}>"
    
        