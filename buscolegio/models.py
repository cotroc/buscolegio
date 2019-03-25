from datetime import datetime
from buscolegio import db, login_manager
from flask_login import  UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    instituto = db.relationship('Instituto', uselist=False, backref='responsable', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Instituto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    cover_picture = db.Column(db.String(120), nullable=True, default='image.png') # rename portada
    url = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    est = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(256), nullable=True)
    state = db.Column(db.String(60), nullable=True)
    loc = db.Column(db.String(60), nullable=True)
    teachers = db.Column(db.Integer, nullable=True) # rename profesores
    classrooms = db.Column(db.Integer, nullable=True) # aulas (?)
    rel_conf = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(60), nullable=True) 
    enrollment = db.Column(db.Numeric(20), nullable=True)
    fee = db.Column(db.Numeric(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='created_by', lazy=True)
    extras = db.relationship('Extra', backref='extra', lazy=True)
    


    def __repr__(self):
        return f"Instituto('{self.id}' '{self.email}', '{self.name}', '{self.url}', '{self.email}')"

class Extra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(20), nullable=False)
    instituto_id = db.Column(db.Integer, db.ForeignKey('instituto.id'), nullable=False)

    def __repr__(self):
        return f"Extra('{self.categoria}', '{self.nombre}', '{self.descripcion}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"