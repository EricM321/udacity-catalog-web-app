from flask import Blueprint, jsonify
from database_setup import Catalog, CatalogItem
from app_session import session

json_api = Blueprint('json_api', __name__)


@json_api.route('/catalog/JSON')
def catalog_json():
    """
    This function provides a JSON endpoint for the application that will return
    a JSON object containing the all catalogs amd their item information

    Return:
        :rtype: JSON object
    """
    catalog = session.query(Catalog)
    catalogitem = session.query(CatalogItem)
    category = [i.serialize for i in catalog]

    for i in category:
        for j in catalogitem:
            if i['id'] == j.catalog_id:
                if 'Item' in i:
                    i['Item'].append(j.serialize)
                else:
                    i.update({'Item': []})
                    i['Item'].append(j.serialize)
    return jsonify(Category=category)


@json_api.route('/catalog/<name>/<item>/JSON')
def catalog_item_json(name, item):
    """
    This function provides a JSON endpoint for the application that will return
    a JSON object containing the catalog item information

    Args:
        name (string): catalog name
        item (string): item name

    Return:
        :rtype: JSON object
    """
    catalog = session.query(Catalog).filter(Catalog.name == name).one()
    items = session.query(CatalogItem).filter(CatalogItem.name == item).one()
    category = catalog.serialize
    category.update({'item': items.serialize})
    return jsonify(Category=category)
