
# Item Catalog
An Item Catalog web template for multiple user to add share online. It can be extended to similar purpose as user can add restaurants and it's menus.

* database_setup_item_catalog.py : contain database schema build with [sqlachememy](http://www.sqlalchemy.org/)
* item-catalog.py ­ ​: the handler for the website

## Features includes:

#####  authentication and authorization

user currently can login through google account or facebook account through Oauth2.0, anti-forgery token is created for each login session.

##### [flask framework](http://flask.pocoo.org/)
Flask framework is used, so you can focus on the implementations thats most matters to your application. Flask includes jinja2, so your code is easily reusable.

##### RESTAPI supported
* all items under specific catalog_id

  ```localhost:5000/catalog/<int:catalog_id>/item/JSON```

* one specific item under one specific catalog

  ```localhost:5000/catalog/<int:catalog_id>/item/<int:item_id>/JSON```

* all catalogs and items at the site

  ```localhost:5000/catalog/JSON```

## Quick Run
To test the implementation please navigate to vagrant/catalog
and to setup the database use:

```python database_setup_item_catalog.py```

to host the website run:

```python item-catalog.py```


## Using the Vagrant Virtual Machine  
  This project is run in vagrant VM, please follow the below instruction to setup the working enviroment:

 The Vagrant VM has PostgreSQL installed and configured, as well as the psql
command line interface (CLI)​
 , so that you don't have to install or configure them on your
local machine.
To use the Vagrant virtual machine, navigate to the
vagrant/tournament directory in the terminal, then ​
 use the command

```vagrant up ​```
(powers on the virtual machine)
followed by

```vagrant ​ssh ​```
 (logs into the
virtual machine)​  

once you have executed the ​
 vagrant ssh ​
 command, you will want to cd
 ​
/vagrant ​
 to change directory to the ​
 synced folders​

The Vagrant VM provided in the already has PostgreSQL server installed,
as well as the psql command line interface (CLI).
