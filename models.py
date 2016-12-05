from peewee import *
from playhouse.db_url import connect

db = connect("mysql://root:reallysecurepassword@localhost:3306/studdybuddy")


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    uid = UUIDField(null=False, unique=True)
    username = CharField(null=False, default="unknown")
    email = CharField(null=False, unique=True)
    password = CharField(null=False)

class University(BaseModel):
    name = CharField(default="unknown")

class Course(BaseModel):
    name = CharField(default="unknown")
    subject = CharField(default="unknown")
    school = ForeignKeyField(University)

class Rating(BaseModel):
    relevant_yes = IntegerField(default=0)
    useful_yes = IntegerField(default=0)
    total_useful_votes = IntegerField(default=0)
    total_relevance_votes = IntegerField(default=0)

class File(BaseModel):
    name = CharField(default="unknown")
    semester = CharField(default="unknown")
    server_name = CharField(default="unknown")
    date_uploaded = CharField(default="unknown")
    grade = CharField(default="unknown")
    uploaded_by = ForeignKeyField(User)
    rating = ForeignKeyField(Rating, null=True)
    course = ForeignKeyField(Course, null=True)

# db.create_tables([User, University, Course, Rating, File])
