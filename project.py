from flask import Flask
from sqlalchemy import create_engine
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
    latest_items = session.query(Item).order_by(desc(created_date))
    return render_template('index.html', categories = categories, items = items)

@app.route('/category/<int:category_id>/')
def showCategoryItems(category_id):
    return 'You are on categories item page.'

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
