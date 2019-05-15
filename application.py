from flask import (Flask, render_template,
                   request, redirect,
                   url_for, flash)
from flask import session as login_session
from database_setup import Catalog, CatalogItem
from loginApi import login_api
from jsonApi import json_api
from app_session import session

app = Flask(__name__)

app.register_blueprint(login_api)
app.register_blueprint(json_api)


@app.route('/')
def catalog_home():
    """
    This function provides the catalog and item information for the home page
    """
    catalog = session.query(Catalog)
    items = session.query(CatalogItem).order_by(
        CatalogItem.created_date.desc()).limit(10)
    return render_template('home.html', catalog=catalog, items=items)


@app.route('/catalog/<name>/items/')
def catalog_items(name):
    """
    This function provides the catalog items information

    Args:
        name (string): catalog name
    """
    catalogs = session.query(Catalog)
    catalog = session.query(Catalog).filter(Catalog.name == name).one()
    items = session.query(CatalogItem).join(Catalog).filter(
        Catalog.name == name)
    return render_template('catalog.html', catalogs=catalogs, catalog=catalog,
                           items=items, num=items.count())


@app.route('/catalog/<name>/<item>/')
def catalog_item(name, item):
    """
    This function provides the item information from a specific catalog.
    Currently name is unused.

    Args:
        name (string): catalog name
        item (string): item name
    """
    items = session.query(CatalogItem).filter(CatalogItem.name == item).one()
    return render_template('item.html', items=items)


@app.route('/new', methods=['GET', 'POST'])
def new_item():
    """
    This function provides the item creation HTML page on a get request, if the
    user is logged in otherwise they are redirected to the login page.
    On a post request the information is taken from the and the item is created
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'],
                              description=request.form['description'],
                              catalog_id=request.form['catalog-id'],
                              user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New %s Item Successfully Created' % newItem.name)
        return redirect(url_for('catalog_home'))
    else:
        catalog = session.query(Catalog)
        return render_template('newitem.html', catalog=catalog)


@app.route('/catalog/<item>/edit', methods=['GET', 'POST'])
def edit_item(item):
    """
    This function provides the item editing HTML page on a get request, if the
    user is logged in otherwise they are redirected to the login page.
    If the user is authorized they will not be able to edit the item.
    On a post request only the changed fields in the form will be updated.

    Args:
        item (string): item name
    """
    editedItem = session.query(CatalogItem).filter_by(name=item).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to edit this item. Please create your own item " \
               "in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['catalog-id']:
            editedItem.catalog_id = request.form['catalog-id']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        catalog = session.query(Catalog).filter_by(
            id=request.form['catalog-id']).one()
        return redirect(url_for('catalog_item', name=catalog.name,
                                item=editedItem.name))
    else:
        catalog = session.query(Catalog)
        return render_template('edititem.html', item=editedItem,
                               catalog=catalog)


@app.route('/catalog/<item>/delete', methods=['GET', 'POST'])
def delete_item(item):
    """
    This function provides the item deletion HTML page on a get request, if the
    user is logged in otherwise they are redirected to the login page.
    If the user is authorized they will not be able to delete the item.
    On a post request the item is deleted.

    Args:
        item (string): item name
    """
    itemToDelete = session.query(CatalogItem).filter_by(name=item).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to delete this item. Please create your own item " \
               "in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('catalog_home'))
    else:
        return render_template('deleteitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0')