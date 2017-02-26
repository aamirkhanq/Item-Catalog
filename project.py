from flask import Flask, render_template, request, redirect, url_for
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
    items = session.query(Item).filter_by(category_id = category_id).all()
    num_of_items = len(items)
    category = session.query(Category).filter_by(id = category_id).first()
    category = category.name
    category += ' Items (' + str(num_of_items) + ' items)'
    categories = session.query(Category).all()
    return render_template('categoryitems.html', items = items, category = category, categories = categories, category_id = category_id)

@app.route('/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    #return 'You are on the item page.'
    item = session.query(Item).filter_by(id = item_id).first()
    categories = session.query(Category).all()
    return render_template('item.html', item = item, category_id = category_id, categories = categories)

@app.route('/category/new/', methods = ["GET", "POST"])
def addNewItem():
    #return 'This page is for adding items.'
    if request.method == 'POST':
        if request.form['name']:
            category = request.form['q']
            category_id = session.query(Category).filter_by(name = category).one()
            newItem = Item(name = request.form['name'], description = request.form['description'], category_id = category_id.id)
            session.add(newItem)
            session.commit()
            return redirect(url_for('showItem', category_id = category_id.id, item_id = newItem.id))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories = categories)

@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    #return 'This page is for editing item.'
    item = session.query(Item).filter_by(id = item_id).first()
    #item_name = item.name
    #item_description = item.description
    categories = session.query(Category).all()
    if request.method == "POST":
        if request.form['title']:
            item.name = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        selected_category_name = request.form['q']
        selected_category_row = session.query(Category).filter_by(name = selected_category_name).first()
        selected_category_id = selected_category_row.id
        item.category_id = selected_category_id
        session.add(item)
        session.commit()
        return redirect(url_for('showItem', category_id = item.category_id, item_id = item_id))
    else:
        return render_template('editItem.html', name = item.name, description = item.description, category_id = category_id, item_id = item_id, categories = categories)

@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    return 'This page is for deleting items.'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
