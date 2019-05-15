### Project Name: Item Catalog App.
This project sets up a **PostgreSQL** database for a **news** website...
The provided Python script **application.py** uses the **SQLAlchemy** library to query 
the database and **Flask** to handle the front end elements of the app.

#### Requirements
- Python 3
- Flask
- SQLAlchemy
- Oauth2client
- Httplib2


#####The database

######Catalog table
 Column  |    Type      |  Modifiers                       
---------|:------------:|-------------------
 id      | Integer      | primary_key
 name    | String       | not nullable
 user_id | Integer      | ForeignKey
 user    | relationship 

######Catalog item table
 Column       |      Type        |      Modifiers                       
--------------|:----------------:|------------------------------------
 name         | String           | not nullable
 id           | Integer          | primary_key
 description  | String           |
 catalog_id   | Integer          | ForeignKey
 catalog      | relationship     |
 user_id      | Integer          | ForeignKey
 user         | relationship     |
 created_date | DateTime         | default=datetime.datetime.utcnow

######User table
 Column  |  Type   |  Modifiers                     
---------|:-------:|------------------
 id      | Integer | primary_key
 name    | String  | not nullable
 email   | String  | not nullable
 picture | String  |


####Running the code
Create the database:
```
$ python3 database_setup.py
```
Populate the database:
```
$ python3 lotsofcatalogs.py
```
Run the website:
```
$ python3 application.py
```
