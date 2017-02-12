from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///restaurantapplication.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app=Flask(__name__)

#===============
#ROUTES
#===============
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['POST', 'GET'])
def newRestaurant():
	if request.method == 'GET':
		return render_template('newrestaurant.html')
	elif request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['newrestaurant'])
		session.add(newRestaurant)
		session.commit()
		return render_template('restaurants.html', restaurants=session.query(Restaurant).all())

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'GET':
		return render_template('editrestaurant.html', restaurant=restaurant)
	elif request.method == 'POST':
		restaurant.name = request.form['newname']
		session.add(restaurant)
		session.commit()
		return render_template('restaurants.html', restaurants=session.query(Restaurant).all())

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'GET':
		return render_template('deleterestaurant.html', restaurant=restaurant)
	elif request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		return render_template('restaurants.html', restaurants=session.query(Restaurant).all())

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	return render_template('menu.html', restaurant=restaurant, items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all())

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'GET':
		return render_template('newmenuitem.html', restaurant=restaurant)
	elif request.method == "POST":
		item = MenuItem(name=request.form['newname'], restaurant_id=restaurant_id, description=request.form['newdescription'], price=request.form['newprice'], course=request.form['newcourse'])
		session.add(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
	if request.method == 'GET':
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=item)
	elif request.method == "POST":
		item.name = request.form['newname']
		item.description = request.form['newdescription']
		item.price = request.form['newprice']
		item.course = request.form['newcourse']
		session.add(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
	if request.method == 'GET':
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=item)
	elif request.method == "POST":
		session.delete(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

#===============
#JSON
#===============
@app.route('/restaurant/<int:restaurant_id>/menu/json/')
def restaurantMenuItemsJSON(restaurant_id):
	restuarant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return jsonify(Restaurant=[restuarant.serialize], MenuItems=[item.serialize for item in items])

@app.route('/restaurants/json/')
def restaurantsJSON():
	return jsonify(Restaurants=[rest.serialize for rest in session.query(Restaurant).all()])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json/')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
	return jsonify(MenuItem=[item.serialize])

if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0', port = 5000)