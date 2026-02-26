from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy.db()

class Post:
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    room_dimensions = db.Column(db.String(120))
    monthly_rent = db.Column(db.Integer)
    non_advance_monthly_rent = db.Column(db.Integer, default=0)

    from_owner = db.Column(db.Integer, default=False)
    bills_included_on_rent = db.Column(db.Boolean, default=False)
    
    deposit_factor = db.Column(db.Integer, default=1)
    commission_factor = db.Column(db.Integer, default=1)
    
    payment_interval = db.Column(db.Integer)

    posting_type = db.Column(db.Enum('need_roommate','need_room_and_roommate'), nullable=False,  name="posting_type_enum")
    
    is_active = db.Column(db.Boolean, default=1)
    
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    

    def calculate_move_in_rent(self, paying_advance=True, from_owner=False):
        """
        summation of min deposit, advance_payment, commission
        """
        move_in_rent = self.calculate_deposit()
        if paying_advance:
            move_in_rent += self.calculate_interval_rent()
        elif not paying_advance:
            move_in_rent += self.non_advance_monthly_rent
        if not from owner:
            move_in_rent += self.calculate_commission()
        return move_in_rent
            
    
    def calculate_commission(self):
        return self.commission_factor * self.monthly_rent

    def calculate_deposit(self):
        return self.monthly_rent * self.deposit_factor

    def calculate_interval_rent(self):
        return self.monthly_rent * self.payment_interval
            
    def to_dict(self):
        return {
            
        }


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_description = db.Column(db.String(1024))
    
    gender = db.Column(db.Enum('male', 'female', name='gender_enum'), nullable=False)
    profile_photo = db.Column(db.String(2048))
    
    uni_major = db.Column(db.String(1024))
    year_of_school = db.Column(db.Enum("0","1","2","3","4", name='year_of_school_enum'), default="0")
    
    user_type = db.Column(db.Enum('ordinary_user', 'admin', name='user_type_enum'),  default='ordinary_user')
    
    
    password_hash = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    email_validated =  db.Column(db.Boolean, default=False) 
    num_posts = db.Column(db.Integer, default=0)

    school = db.Column(db.Integer, db.ForeignKey("schools.id"))
    group = db.Column(db.Integer, db.ForeignKey("groups.id"))

    posts = db.relation("Post", back_ref="user_id", lazy=True)

    sent_messages = db.relation("Message", foreign_keys="Message.sender_id", back_ref="sender", lazy=True)
    received_messages = db.relation("Message", foreign_keys="Message.receiver_id", back_ref="receiver", lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.user_type == 'admin'
    
        
    def to_dict(self):
        return {
            'id': self.id,
            'lname': self.lname,
            'fname': self.fname,
            'username': self.username,
            'email': self.email,
            'profile_description': self.profile_description,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'email_validated': self.is_active,
           
        }


class Group(db.Model):
    __tablename__ = "usergrouping"
    id = db.Column(db.Integer, primary_key=True)
    group_max_count = db.Column(db.Integer)
    group_count_status = db.Column(db.Integer)
    link_id = db.Column(db.Integer, db.ForeginKey("links.id"))

    def is_full(self):
        return self.group_max_count == self.group_count_status
    

class School(db.Model):
    __tablename__ = "schools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    acronym = db.Column(db.String(10))
    users = db.relation("User", back_ref="school", lazy=True)


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120))
    city = db.Column(db.String(120))
    area = db.Column(db.String(120))
    posts = db.relation("Post", back_ref="location_id", lazy=True)

    
class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relation("Post", back_ref="link_id", lazy=True)
    groups = db.relation("Group", back_ref="link_id", lazy=True)
    


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Colum(db.Integer, primary_key=True)
    message =  db.Column(db.String(1024))
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recepient_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
