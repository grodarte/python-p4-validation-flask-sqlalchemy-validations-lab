from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if name in [author.name for author in Author.query.all()] or not name:
            raise ValueError("Each record must have a unique name.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        is_digit_list = [char.isdigit() for char in phone_number]
        if False in is_digit_list or len(is_digit_list) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]

        # iterate through clickbait, r
        if not title or True not in [quote in title for quote in clickbait]:
            raise ValueError("Post must contain clickbait-y title.")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post too short. Content must be 250 characters or more.")
        return content

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Invalid category, must be either 'Fiction' or 'Non-Fiction'")
        return category
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary too long, must be 250 characters or less.")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
