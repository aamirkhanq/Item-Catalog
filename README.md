# Item Catalog
This project creates an Item Catalog. It stores the categories and their corresponding items in a SQLite database. The database file `itemcatalog.db` can be queried at the Linux command prompt with:
`sqlite3 itemcatalog.db`
User should have their own AWS Instance to run the project. You should run the main file for the project - `project.py` by using the following command:
`python project.py`
Once the server starts, you can run this app in your browser by navigating to `http://<YOUR_PUBLIC_IP>/` or `http://<YOUR_PUBLIC_IP>/index`.

### List of modules
- `project.py`: It is the main file that renders all templates using a set of functions.
- `database_setup.py`: It creates a database named `itemcatalog.db` that stores all the information.
- `itemcatalog.db`: It contains the schema for the project.

### List of templates
- `base.html`: This defines the common layout which all other templates inherit.
- `index.html`: This is the main page of the app. It renders Login or Logout button based on the user's login status.
- `login.html`: It is the only template which does not inherit from `base.html`. It contains the Google + sign in button to help users to log in to the app using their Google + accounts.
- `newitem.html`: This templates is rendered only to logged in users. It contains a form to add a new item to the category of your choice. 
- `categoryitems.html`: This template displays the items belonging to a particular category.
- `item.html`: This template shows the description of the item that is clicked. It renders Edit and Delete buttons based on the user's login status.
- `publicitem.html`: This template is rendered to logged in users who want to see the item descriptions of other users.
- `edititem.html`: This template is rendered when a logged in user clicks on the Edit button below the item description.
- `deleteitem.html`: This template is rendered when a logged in user clicks on the Delete button below the item description.

### List of functions
There are a couple of functions defined inside both `project.py`. These functions are for various routes of the app and serve specific purposes.
- **Function Definitions**:
	1. `mainPage()`: This function leads to the main page of the Item Catalog App. It renders the template `index.html`.
	2. `showCategoryItems(category_id)`: Takes in `id` attribute from `categories` table as input and displays items belonging to that category. It renders the template `categoryitems.html`. 
	3. `showItem(category_id, item_id)`: Takes in `id` attribute from `categories` table (category_id) and `id` attribute from `items` table (item_id). It then renders all the entries in `items` table whose `category_id` attribute matches the category_id parameter. It renders `item.html` if the user is the creator of the item, otherwise it renders `publicitem.html`.
	4. `addNewItems()`: This function checks if the user is already logged in or not by monitoring the `login_session` object. It renders the page with a login or a logout button accordingly. Only logged in users can see add item link.
	5. `editItem(category_id, item_id)`: Takes in `id` attribute from `categories` table (category_id) and `id` attribute from `items` table (item_id). It then checks if the logged in user is the creator of the item entry in `items` table. Based on this decision, a user is/is not allowed to edit the item. If the user has made a GET request, then this function renders `editItem.html` which is essentially a form to collect user's input. If the user makes a POST request (when user submits the form), this function redirects the user to the URL for `showItem()` function.
	6. `deleteItem(category_id, item_id)`: Takes in `id` attribute from `categories` table (category_id) and `id` attribute from `items` table (item_id). It then checks if the logged in user is the creator of the item entry in `items` table. Based on this decision, a user is/is not allowed to delete the item. If the user has made a GET request, then this function renders `deleteitem.html` which is essentially a form to collect user's input. If the user makes a POST request (when user submits the form), this function redirects the user to the URL for `showCategoryItems()` function.
	7. `categoryItemJSON(category_id)`: Returns a JSON object containing the details of the items(`id`, `name`, `description`) belonging to the category having the `id` that matches category_id.
	8. `categoriesJSON()`: Returns a JSON object containing details of all items (`id`, `name`, `description`, `category_id`) in the database.
	9. `showLogin()`: Creates a state token and passes it to the user. This helps in preventing anti-forgery attacks by malicius scripts. It is also linked to the Login button in the app.
	10. `gconnect()`: This handles the code sent back from the callback method. The callback method is `signInCallback()` defined in `login.html`.
	11. `gdisconnect()`: This logs the user out by deleting his information from the `login_session` object.
	12. `createUser(login_session)`: This creates entries inside the `users` table. The entries include `name` and `email` columns.
	13. `getUserInfo(user_id)`: It returns a SQLAlchemy query session object that contains the row for the user corresponding to the user_id parameter. user_id parameter gets `id` belonging to a particular entry in the `users` table.
	14. `getUserID(email)`: If the email parameter exists inside the `users` table as an `email` attribute, then this function returns the corresponding row. Otherwise it returns `None`.

### List of tables
Following tables are present in the schema:
- `categories`: It keeps track of the categories and assigns an ID to their name. The column names are `name` and `id`.
- `users`: It stores the name and email id of users. The column names are `name`, `email` and `id`.
- `items`: It stores the items belonging to a particular category. The column names are `name`, `id`, `description`, `category_id` and `user_id`. `category_id` holds a foreign key relationship with the `id` column in `categories` table. `user_id` holds a foreign key relationship with the `id` column in `users` table. 