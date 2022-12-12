from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PublicationTopic(Base):
    __tablename__ = "PublicationTopics"
    topic_id = Column("TopicId", Integer, primary_key=True, nullable=False)
    name = Column("Name", String, nullable=False)
    description = Column("Name", String, nullable=True)
    def __init__(self, topic_id, name, description=None):   
        self.topic_id = topic_id  
        self.name = name
        self.description = description
    def __repr__(self):
        return f"{self.topic_id}: {self.name}"

class User(Base):
    __tablename__ = "Users"
    user_id = Column("UserId", Integer, primary_key=True, nullable=False)
    first_name = Column("FirstName", String, nullable=False)
    surname = Column("Surname", String, nullable=False)
    registration_date = Column("RegistrationDate", String, nullable=False, default=datetime.utcnow)
    def __init__(self, user_id, first_name, surname, registration_date):   
        self.user_id = user_id  
        self.first_name = first_name
        self.surname = surname
        self.registration_date = registration_date
    def __repr__(self): 
        return f"{self.user_id} {self.first_name} {self.surname} {self.registration_date}"

class Author(Base):
    __tablename__ = "Authors"
    user_id = Column("UserId", Integer, ForeignKey("Users.UserID"), primary_key=True, nullable=False)
    def __init__(self, user_id):   
        self.user_id = user_id  
    def __repr__(self): 
        return f"{self.user_id}"

class Publication(Base):
    __tablename__ = "Publications"
    publication_id = Column("PublicationId", Integer, primary_key=True, nullable=False)
    author = Column("Author", Integer, ForeignKey("Authors.UserID"), nullable=False)
    topic = Column("Topic", Integer, ForeignKey("PublicationTopics.TopicID"), nullable=False) 
    upload_date = Column("UploadDate", String, nullable=False, default=datetime.utcnow)
    def __init__(self, publication_id, author, topic, upload_date):   
        self.publication_id = publication_id  
        self.author = author
        self.topic = topic
        self.upload_date = upload_date
    def __repr__(self, publication_id, author, topic, upload_date):   
        return f"{self.publication_id} {self.author} {self.topic} {self.upload_date}"



# def populate_topics():
#     engine = create_engine(r"sqlite:///database\sqlite.db", echo=True)
#     Base.metadata.create_all(bind=engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()   

#     df = pd.read_csv("Tags.csv")
#     for i, topic_name in df.iterrows():
#         topic = PublicationTopic(i, topic_name["Tags"])
#         session.add(topic)
#     session.commit()