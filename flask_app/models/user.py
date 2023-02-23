from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash


class User:

    db = 'log_reg_2'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



#Validate Method/Static method - only pass in the class!
#insert value from index.html - register so you can use flash method on two separate forms

    @staticmethod
    def is_valid_reg(user):
        is_valid = True
    #now query the database to check to see if the email is ALREADY in the DB and if email is valid with bcrypt
    #like get one method
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
#now check if the email is already in the DB
        if len(results) >= 1:
            flash("This email is already in use!  Please login instead!", "register")
            is_valid = False
#now check to see if email is valid email address 
        if not EMAIL_REGEX.match(user['email']):
            flash("Not a valid email address! Try again!", "register" )
            return False

#add validations for first + last name (3 chara's) and password (8 chara's)
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters. Try again.", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters. Try again", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.  Please try again", "register")
            is_valid = False

#add validation to check to make sure both passwords match
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match!", "register")
        return is_valid



#CRUD METHOD


#GET ALL -READ ALL 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users




#GET ONE - Read ONE
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


#Get by email address - used for LOGIN form

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
#Validate here
        if len(results) < 1:
            return False
        return cls(results[0])



#CREATE/SAVE
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        return connectToMySQL(cls.db).query_db(query,data)





#We don't use UPDATE and DELETE in this assignment

#UPDATE
    @classmethod
    def udpate(cls,data):
        query = "UPDATE users SET NAME first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s; "
        return connectToMySQL(cls.db).query_db(query, data)



#Delete
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)