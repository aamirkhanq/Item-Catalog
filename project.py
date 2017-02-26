from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the'
                                            'authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           %access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/')
@app.route('/index/')
def mainpage():
    #return 'You are at the main page.'
    categories = session.query(Category).all()
    latest_items = session.query(Item).all()
    latest_items.reverse()
    if len(latest_items) > 10:
        items = latest_items[0:10]
    else:
        items = latest_items
    return render_template('index.html', categories = categories, items = items, string = "Login")

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
    #return 'This page is for deleting items.'
    itemToDelete = session.query(Item).filter_by(id = item_id).first()
    categories = session.query(Category).all()
    if request.method == "POST":
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCategoryItems', category_id = category_id))
    else:
        return render_template('deleteitem.html', name = itemToDelete.name, category_id = category_id, item_id = item_id, categories = categories)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
