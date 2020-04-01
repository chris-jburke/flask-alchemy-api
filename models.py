from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/foodflasql'
db = SQLAlchemy(app)
user_foods = db.Table('user_foods',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
	db.Column('food_id', db.Integer, db.ForeignKey('foods.id'), primary_key=True)
)
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	nickname = db.Column(db.String)
	foods = db.relationship('Food', 
		secondary=user_foods,
		lazy='subquery',
		backref=db.backref('food', lazy=True)
	)
	def __repr__(self):
		return f"🦀 User(id={self.id}, email='{self.email}', 'name={self.name}', 'nickname={self.name}') 🦀"
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class Food(db.Model):
	__tablename__ = 'foods'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	cuisine = db.Column(db.String)
	def __repr__(self):
		return f"🦀 Food(id={self.id}, name='{self.name}', 'cuisine={self.cuisine}') 🦀"
	def as_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'cuisine': self.cuisine
		}
def get_or_create(model, defaults=None, **kwargs):
	instance = db.session.query(model).filter_by(**kwargs).first()
	if instance:
		return instance, False
	else:
		params = dict((k,v) for k, v in kwargs.items())
		params.update(defaults or {})
		instance = model(**params)
		db.session.add(instance)
		return instance, True