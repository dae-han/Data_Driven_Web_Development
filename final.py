from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# Adding database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu//<int:menu_id>/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/')
def mainPage():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    all_rs = session.query(Restaurant).all()
    return render_template('mainpage.html', all_rs = all_rs)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    rs = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rs.id)
    return render_template('menu.html', rs = rs, items = items)

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(
            name = request.form['name'],\
            description = request.form['description'],\
            price = request.form['price'],\
            course = request.form['course'],\
            restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()

        flash("new menu item created!")

        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()

        flash("Item edited!")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item = editedItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('deletemenuitem.html', item = deleteItem)

if __name__ == '__main__':
    # flask use the secret key to create sessions for out users.
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
