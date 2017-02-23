from flask import Flask, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def mainpage():
    #return 'You are at the main page.'
    categories = session.query(Category).all()
    latest_items = session.query(Item).all()
    return render_template('index.html', categories = categories, items = latest_items, string = "Login")

@app.route('/category/<int:category_id>/')
def showCategoryItems(category_id):
    #return 'You are on categories item page.'
    items = session.query(Item).filter_by(id = category_id).all()
    num_of_items = len(items)
    category = session.query(Category).filter_by(id = category_id).first()
    category = category.name
    category += 'Items (' + str(num_of_items) + 'items)'
    return render_template('categoryitems.html', items = items)

@app.route('/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    return 'You are on the item page.'

@app.route('/category/<int:category_id>/new/')
def addNewItem(category_id):
    return 'This page is for adding items.'

@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    return 'This page is for editing item.'

@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    return 'This page is for deleting items.'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
