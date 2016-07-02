A README file is included in the GitHub repo containing the following information:
IP address, URL, summary of software installed, summary of configurations made,
and a list of third-party resources used to completed this project.

The website is hosted at http://52.41.243.112/

## Dependcies
PostgreSQL
apache2
UFW
Git
pip flask

```sudo apt-get install apache2 libapache2-mod-wsgi postgresql python-psycopg2 libpq-dev```

### configuration

#### protocols and ports
* SSH:2200

* HTTP:80

* NTP:123

#### Key-based SSH authentication is enforced

#### Applications have been updated to most recent updates

#### postresql has been configured to serve data locally

#### [catalog project](https://github.com/WenchenLi/fullstackUdacity/tree/master/item-catalog) is configured as a wsgi app on the server

#### Configure the local timezone to UTC

#### PostgreSQL
* not allow remote connections
* Create a new user named catalog that has limited permissions to catalog application database: now catalog is the owner of catalogdb (catalog application database)

#### app configuration
* catalog app sits at /var/www/catalog
the catalog has the following paths

```
/var/www/catalog/app.wsgi
                /catalog/
                        /catalog.py (the app, change file paths to absolute for json and add app secret, change database connections to postgreSQL)
                        /fb_client_secrets.json
                        /g_client_secrets.json
                        /database_setup_item_catalog.py(change database connections to postgreSQL)
                        /static   (same as the project)
                        /template (same as the project)

```



app.wsgi is configured as:
```#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/catalog")

from catalog import app as application
```

### references to complete configre linux web server
[configure protocols and ports using UFW](
https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server)



[PostgreSQL install](
http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi)

postgreSQL debug and create user
[this](
http://stackoverflow.com/questions/11919391/postgresql-error-fatal-role-username-does-not-exist)
and [this](
http://superuser.com/questions/507721/user-permissions-for-creating-postgresql-db)

[debug server](http://unix.stackexchange.com/questions/38978/where-are-apache-file-access-logs-stored)

[write requirement for python](
http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/)
## Some useful command

[deploy in general](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

restart apache
 * ```sudo apache2ctl restart```
 * ```service apache2 restart```

check users
* ```finger```
* ```finger username```

add user

```sudo adduser username```

check error in log

*```cat /var/log/apache2/error.log```
