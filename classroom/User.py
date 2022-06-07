import json
from cryptography.fernet import Fernet
from . import credentials as conf, Utils
import pyrebase

class User():
    
    FIREBASE = pyrebase.initialize_app(conf.config)
    AUTH = FIREBASE.auth()
    DB = FIREBASE.database()

    def __init__(self, email=None, passwd=None, id=None):
        self._email = None
        self._password = None
        if (isinstance(email, str) and isinstance(passwd, str)):
            self._password: str = passwd
            self._email: str = email
        if (isinstance(id, int)):
            self._id: int = id
        else:
            self._id: int = self.generate_unique_id()
        self._first_name: str = None
        self._last_name: str = None
        self._status: int = 0
        self._flags: dict = {"lang": None}

    def generate_unique_id(self):
        db_object = User.DB.child("user").get().val()
        if db_object == None:
            return 1
        else:
            return len(db_object) + 1
    
    @property
    def first_name(self): return self._first_name

    @property
    def last_name(self): return self._last_name

    @property
    def password(self): return self._password

    @property
    def email(self): return self._email

    @property
    def flags(self): return self._flags

    @property
    def status(self): return self._status

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @password.setter
    def password(self, passwd):
        self._password = passwd

    @email.setter
    def email(self, email):
        if Utils.Utils.check_if_email(email):
            self._email = email
        else:
            return None

    @flags.setter
    def flags(self, flags):
        self._flags = flags

    @status.setter
    def status(self, status):
        self._status = status

    def update_to_database(self):
        data_to_database = {
            "id": int(self._id),
            "first_name": json.dumps(self._first_name),
            "last_name": json.dumps(self._last_name),
            "email": json.dumps(self._email),
            "password": json.dumps(self._password),
            "flags": self._flags,
            "status": int(self._status)
        }
        User.DB.child("user").child(self._id).update(data_to_database)

    def insert_update_to_database(self):
        data_to_database = {
            "id": int(self._id),
            "first_name": str(self._first_name),
            "last_name": str(self._last_name),
            "email": str(self._email),
            "password": str(self._password),
            "flags": json.dumps(self._flags),
            "status": int(self._status)
        }
        user = User.find_by_email(self._email)
        if user != None:
            self.update_to_database(data_to_database)
        else:
            User.DB.child("user").child(self._id).set(data_to_database)

    def encrypt_password(self):
        fernet = Fernet(conf.SECURE_KEY.encode())
        encrypted_password = fernet.encrypt(self._password)
        return encrypted_password

    @staticmethod
    def unpacked_objects(objects):
        if len(objects) == 1:
            return objects[0]
        return objects

    @staticmethod
    def get_by_string(objects, key, word):
        users = []
        for v in objects:
            if v != None:
                print(v[key])
                if v[key] == word:
                    users.append(v)
        return users

    @staticmethod
    def find_by_first_name(first_name):
        user_db_objects = User.DB.child("user").order_by_child("first_name").get().val()
        user_objects = []
        users_with_name = User.get_by_string(user_db_objects, "first_name", first_name)
        if user_db_objects != None and len(users_with_name) > 0:
            for v in users_with_name:
                new_user = User()
                new_user.first_name = v["first_name"]
                new_user.last_name = v["last_name"]
                new_user.email = v["email"]
                new_user.password = v["password"]
                new_user.flags = json.loads(v["flags"])
                new_user.status = v["status"]
                user_objects.append(new_user)
            return User.unpacked_objects(user_objects)
        else:
            return None

    @staticmethod
    def find_by_last_name(last_name):
        user_db_objects = User.DB.child("user").order_by_child("last_name").get().val()
        user_objects = []
        users_with_name = User.get_by_string(user_db_objects, "last_name", last_name)
        if user_db_objects != None and len(users_with_name) > 0:
            for v in users_with_name:
                new_user = User()
                new_user.first_name = v["first_name"]
                new_user.last_name = v["last_name"]
                new_user.email = v["email"]
                new_user.password = v["password"]
                new_user.flags = json.loads(v["flags"])
                new_user.status = v["status"]
                user_objects.append(new_user)
            return User.unpacked_objects(user_objects)
        else:
            return None

    @staticmethod
    def find_by_email(email):
        user_db_objects = User.DB.child("user").order_by_child("email").get().val()
        user_objects = []
        users_with_email = User.get_by_string(user_db_objects, "email", email)
        if user_db_objects != None and len(users_with_email) > 0:
            for v in users_with_email:
                new_user = User()
                new_user.first_name = v["first_name"]
                new_user.last_name = v["last_name"]
                new_user.email = v["email"]
                new_user.password = v["password"]
                new_user.flags = json.loads(v["flags"])
                new_user.status = v["status"]
                user_objects.append(new_user)
            return User.unpacked_objects(user_objects)
        else:
            return None

    @staticmethod
    def find_by_status(status):
        user_db_objects = User.DB.child("user").order_by_child("status").equal_to(status).get().val()
        user_objects = []
        if user_db_objects != None and len(user_db_objects) > 0:
            for i, v in user_db_objects.items():
                new_user = User()
                new_user.first_name = v["first_name"]
                new_user.last_name = v["last_name"]
                new_user.email = v["email"]
                new_user.password = v["password"]
                new_user.flags = json.loads(v["flags"])
                new_user.status = v["status"]
                user_objects.append(new_user)
            return user_objects
        else:
            return None

    @staticmethod
    def find_by_id(id):
        user_db_object = User.DB.child("user").order_by_child("id").equal_to(id).get().val()
        if user_db_object != None:
            new_user = User()
            new_user.first_name = user_db_object["first_name"]
            new_user.last_name = user_db_object["last_name"]
            new_user.email = user_db_object["email"]
            new_user.password = user_db_object["password"]
            new_user.flags = json.loads(user_db_object["flags"])
            new_user.status = user_db_object["status"]
            return new_user
        else:
            return None
