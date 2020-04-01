from flask import jsonify, redirect
from models import db, User, Food, get_or_create, user_foods
from crud.food_crud import create_food
def get_all_users():
	all_users = User.query.all()
	if all_users:
		results = [user.as_dict() for user in all_users]
		return jsonify(results)
	else:
		raise Exception('Error getting all users')
def get_user(id):
	user = User.query.get(id)
	if user:
		return jsonify(user.as_dict())
	else:
		raise Exception('Error getting user at id {}'.format(id))
def create_user(name, email, nickname):
	new_user = User(name=name, email=email, nickname=nickname or None)
	if new_user:
		db.session.add(new_user)
		db.session.commit()
		return jsonify(new_user.as_dict())
	else:
		raise Exception('Error in creating new user')
def destroy_user(id):
	user = User.query.get(id)
	if user:
		db.session.delete(user)
		db.session.commit()
		return redirect('/users')
	else:
		raise Exception('Error deleting user at id {}'.format(id))
def update_user(id, name, email, nickname):
	user = User.query.get(id)
	if user:
		user.email = email or user.email
		user.name = name or user.name
		user.nickname = nickname or user.nickname
		db.session.commit()
		return redirect('/users/{}'.format(id))
	else:
		raise Exception('Error updating user at id {}'.format(id))
#citation: http://philpearl-blog.logdown.com/posts/280105-flask-sqlalchemy-get-or-create
def update_user_food(id, name, cuisine):
	user = User.query.get(id)
	food = None
	if user:
		try:
			with db.session.begin_nested():
				food = create_food(name,cuisine)
		except Exception as error:
			search_name = '%' + name + '%'
			food = Food.query.filter(Food.name.ilike(search_name)).one()			
		user.foods.append(food)
		db.session.commit()		
		return redirect('/users/{}'.format(id))
	else:
		raise Exception('Error adding food to user at id {}'.format(id))
def show_user_food(id):
	user = User.query.get(id)
	curr_foods = user.foods
	results = [food.as_dict() for food in curr_foods]
	return jsonify(results)



