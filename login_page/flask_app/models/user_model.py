from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])$')
db = "login"

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name'] 
        self.last_name = data['last_name']
        self.emai = data['email']
        self.password= data['password']
        self.created_at = data['created_at'] 
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name , last_name, email , password) VALUES (%(first_name)s , %(last_name)s , %(email)s, %(password)s);"
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM users Where id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query,data)
        user = cls(results[0])
        return user

    @classmethod
    def login_user(cls,data):
        query = "SELECT * FROM users Where email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name needs to be at least 3 charatcers!!!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name needs to be at least 3 charatcers!!!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password needs be at least 8 charatcers!!!")
            is_valid = False
        if user['confirm_pw'] != user['password']:
            flash("Your Passwords do not Match")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!!!")
            is_valid = False
        return is_valid