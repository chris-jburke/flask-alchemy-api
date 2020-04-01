from flask import jsonify, redirect
from models import db, User, Food
def get_all_food():
	all_food = Food.query.all()
	if all_food:
		result = [food.as_dict() for food in all_food]
		return jsonify(results)
	else:
		raise Expection('Error getting all food')
def get_food(id):
	food = Food.query.get(id)
	if food:
		return jsonify(food.as_dict())
	else:
		raise Expection('Error getting food at id {}'.format(id))
def create_food(name, cuisine):
	new_food = Food(name=name, cuisine=cuisine)
	if new_food:
		db.session.add(new_food)
		db.session.commit()
		return jsonify(new_food.as_dict())
	else:
		raise Expection('Error in creating new food')
