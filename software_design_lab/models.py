from datetime import datetime
from data_publisher_site import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PublicationTopic(db.Model):
    __tablename__ = "PublicationTopics"
    id = db.Column("TopicId", db.Integer(), primary_key=True, nullable=False)
    name = db.Column("Name", db.String, nullable=False)
    description = db.Column("Description", db.String, nullable=True)
    publications = db.relationship('Publication', backref='topic', lazy=True)
    def __init__(self, id, name, description=None):   
        self.id = id
        self.name = name
        self.description = description
    def __repr__(self):
        return f"{self.id}: {self.name}"

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column("UserId", db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True, nullable=False)
    first_name = db.Column("FirstName", db.String(20), nullable=False)
    surname = db.Column("Surname", db.String(20), nullable=False)
    email = db.Column("Email", db.String(120), nullable=False, unique=True)
    registration_date = db.Column("RegistrationDate", db.DateTime(25), nullable=False, default=datetime.utcnow)
    password = db.Column("Password", db.String(60), nullable=False)
    author = db.relationship('Author', backref='user', lazy=True)
    def __init__(self, first_name, surname, email, registration_date, password):   
        # self.user_id = user_id
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.registration_date = registration_date
        self.password = password
    def __repr__(self): 
        return f"{self.id} {self.first_name} {self.surname} {self.registration_date}"

class Author(db.Model):
    __tablename__ = "Authors"
    id = db.Column("UserId", db.Integer, db.ForeignKey("Users.UserId"), primary_key=True, nullable=False)
    publications = db.relationship('Publication', backref='author', lazy=True)
    def __init__(self, user_id):   
        self.id = user_id  
    def __repr__(self): 
        return f"{self.id}"

class Publication(db.Model):
    __tablename__ = "Publications"
    id = db.Column("PublicationId", db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True, nullable=False)
    title = db.Column("Title", db.String(40), nullable=False)
    thumbnail = db.Column("Thumbnail", db.String(20), nullable=False, default="default.jpg")
    author_id = db.Column("Author", db.Integer, db.ForeignKey('Authors.UserId'), nullable=False)
    abstract = db.Column("Abstract", db.String(3000), nullable=False)
    simple_desc = db.Column("SimpleDesc", db.String(3000), nullable=False)
    topic_id = db.Column("TopicId", db.Integer, db.ForeignKey("PublicationTopics.TopicId"), nullable=False) 
    upload_date = db.Column("UploadDate", db.DateTime(25), nullable=False, default=datetime.utcnow)
    publication_file = db.Column("File", db.String(20), nullable=False)
    article_authors = db.Column("ArticleAuthors", db.String(200), nullable=False)

    def __repr__(self):   
        return f"{self.id} {self.topic} {self.upload_date}"