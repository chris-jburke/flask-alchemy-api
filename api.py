from models import app, User
from flask import jsonify, request
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user, update_user_food, show_user_food
from crud.food_crud import get_food
@app.errorhandler(Exception)
def unhandled_exception(e):
  app.logger.error('Unhandled Exception: %s', (e))
  message_str = e.__str__()
  return jsonify(message=message_str.split(':')[0])
@app.route('/users', methods=['GET', 'POST'])
def user_index_and_create():
	if request.method == 'GET':
		return get_all_users()
	if request.method == 'POST':
		return create_user(
			name=request.form['name'],
			email=request.form['email'],
			nickname=request.form['nickname']
		)
@app.route('/users/<int:id>', methods=['GET','PUT', 'DELETE'])
def user_show_update_delete(id):
	if request.method == 'GET':
		return get_user(id)
	if request.method == 'PUT':
		return update_user(
			id=id,
			name=request.form['name'],
			email=request.form['email'],
			nickname=request.form['nickname']
		)
	if request.method == 'DELETE':
		return destroy_user(id)
@app.route('/users/food/<int:id>', methods=['GET', 'PUT'])
def user_show_update_food(id):
	if request.method == 'PUT':
		return update_user_food(
			id=id,
			name=request.form['name'],
			cuisine=request.form['cuisine']
		)
	if request.method == 'GET':
		return show_user_food(id=id)