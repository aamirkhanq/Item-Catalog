from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def mainpage():
    return 'You are at the main page.'

@app.route('/category/<int:category_id>/')
def showCategoryItems(category_id):
    return 'You are on categories item page.'

@app.route('/category/<int:category_id>/item/<int:item_id>')
def showItem(category_id, item_id):
    return 'You are on the item page.'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
