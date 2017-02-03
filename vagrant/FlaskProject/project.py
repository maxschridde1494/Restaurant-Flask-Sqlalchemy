from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app=Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#===============
#ROUTES
#===============
@app.route('/')
def welcomePage():
	return "Welcome to the Restaurant Page."

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	return render_template('menu.html', restaurant=restaurant, items=menuItems, url_for=url_for)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['newrestaurantname'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash('new menu item created.')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	elif request.method == 'GET':
		return render_template('newmenuitem.html', restaurant_id=restaurant.id, url_for=url_for)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
	originalName = menuItem.name
	# restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		newName = request.form['name']
		menuItem.name = newName
		menuItem.course = request.form['course']
		print menuItem.course
		menuItem.price = request.form['price']
		menuItem.description = request.form['description']
		session.add(menuItem)
		session.commit()
		string = "%s has been changed to %s." % (originalName, newName)
		flash(string)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	elif request.method=='GET':
		return render_template('editmenus.html', item=menuItem, restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
	name = menuItem.name
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		session.delete(menuItem)
		session.commit()
		string = "%s has been deleted." % name
		flash(string)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	elif request.method=='GET':
		return render_template('deletemenus.html', item=menuItem, restaurant=restaurant, url_for=url_for)

#===============
#JSON
#===============
@app.route("/restaurants/JSON/")
def getRestaurants():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route("/restaurants/<int:restaurant_id>/menu/JSON/")
def getMenuItems(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/")
def getMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
	return jsonify(MenuItem=item.serialize)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug=True
	app.run(host='0.0.0.0', port = 5000)

