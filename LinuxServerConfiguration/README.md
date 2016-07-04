The website is hosted at 52.36.26.117

## Dependcies
install dependencies :
```sudo apt-get install git apache2 libapache2-mod-wsgi postgresql python-psycopg2 libpq-dev python-pip finger postgres-xc-client postgres-xc```
```sudo pip install flask sqlalchemy oauth2client```

### configuration

#### protocols and ports
* SSH:2200

* HTTP:80

* NTP:123

#### Key-based SSH authentication is enforced

```sudo nano /etc/ssh/sshd_config```
then set PasswordAuthentication to no

#### [Create seperate private,public key pair for user grader and put public key on server](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2)

#### Applications have been updated to most recent updates

#### postresql has been configured to serve data locally

#### [catalog project](https://github.com/WenchenLi/fullstackUdacity/tree/master/item-catalog) is configured as a wsgi app on the server

#### [Configure the local timezone to UTC](http://askubuntu.com/questions/138423/how-do-i-change-my-timezone-to-utc-gmt)

```sudo dpkg-reconfigure tzdata```
choose none of above then set to utc.

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
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/catalog")

from catalog import app as application
```
nano /etc/apache2/sites-available/catalog.conf
```
<VirtualHost *:80>
        ServerName 52.36.26.117
        ServerAdmin grader@52.36.26.117
        WSGIScriptAlias / /var/www/catalog/app.wsgi
        <Directory /var/www/catalog/catalog/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
                Order allow,deny
                Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### references to complete configre linux web server
[configure protocols and ports using UFW](
https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)



[PostgreSQL install](
http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi)

postgreSQL debug and create user
[this](https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2)
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


### Key-based

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,82FECA4CD0790E85B8E460B69BA4A074

GPzW83zQLnngQSeCMi1hI5wrOIMbVxwp5wtL/0cVR1emIk3zDkRHWto4CJ06JHBI
q3yh8BNN8TXdhsky6xb+9pC3APdmL+vGieeqG+Aj+vDBiAACGn0T85rcnSDh2H2m
NujkBwrxX+riz/fCWATLc8SkiJ1r3rVqYBMi1RfCA0yehrigrnbO/81luxoTDcRh
nQmpSHCtNlX90zXQDYyi2Npn0VYWCbuYQpliz3W+EAn5E3cWnmv6YprBmbkc6BTu
bUIbiYXsN7uz7MAjfU62H6sQIust3PqILGjoa9SEWjGvFmHF+/WMy2roN8SCB8U9
DStRXgsgt9ASylt4StjlkfBFh30f2cNXEoxhsNQpKROLSKGSQbB+1STL43x1KAqP
utpjThA3OWsOQmJKDhH1h9UhIZHmlWAkJEzsI1az9tqsRpTVfAZcbNHca7OasiO7
b+ihLhC8jdsIRpJkkHJEIfOpW2EFbP2n5jGJqrkgSzTya+dQwbeb+m5BRDTVg3WB
/O6NU2RBKIXE34kf+bZGRnLGxuxyYYvXgouClYyv5ulPMs6rmRmCNyMmS7C/C9+v
N72dVpXJMHnLQTG72A5d/Ui9YxwMP8PlDscCR8GEQDoxryaIhtJ5WqHq9mcl7q6I
qKl739won1bvS1ZzIBkEMcofzKnVR6578DHVyNFkiokPAad6pB6L5YEENQzIT0dk
SOKECsoajHLgpqG0ReYbq3R4aXG+YnV6odqm0Jf26KTC45qhd7BWr9hZLJw8Zgcl
7sXp1TkWgoxzQNnrI4OKgUi4N8ust9fn8UZALV8yX7fHcNkmYfK0TwNxJ85q5LUZ
wL2Jc5CtP5dCFUj+p+nCf5lLeNI7kgaF/3+bGBaiApXB1b3T32/gYzIwVivDlC6I
45zpC93w8ma18fS5nauuanIwun8/eLsyAP5wyWFXvyxn8yLaLNVTVYXVmBVBDRsi
7p9FpaFxch/AwV63Aj/3+Q5gZCr847aFqfnG0qWp9ueX0QFPA7EAvQLouTakWDzV
Q87xkBFrV1WgJ1jSc7dcAlLLE7pQNqBGA83wXvXf/mmmK/aLTp5yRtOe+XKevPaM
IxArh8A09k1Pl9c5eHZbyJ/tIZfglmbw/MctuR2mhPo9ZRtqkcqknK5e4Ny/PVJM
pcksscWZMOejTdGZk4u72ptvXaWljq63+Sp5YBQlbNtLOG1fe8TK9ELJeSsojTT5
imi7p5wNECfWo7uQ++gJ/LycHxcR+uKxJJlG+AVcGw/9BrausThs4uiWFYrhrYUc
mKdF9IDm08GXSChFfVLV1PU2zIJ8id9YZNot6iC2Ap8yg1A1/YsdI9k+O3zRyEht
sPW86D5+dDGl+vNCjpJ/gkHobiogBV0b/B89NPtectv4o4dw40KuKniksprzx2X+
UGHX52syyMwW2G5rSYYf7dJ/Gn4owJHtl2SIpsxeF2PNWX7RuTSTFfFg3hSUFNbN
GNpepBneWJBn9WxeR4rs4P7UkYrzNdC4fyWm7d9zacFdHcLBpGLrL5cz2VOe8NNL
FBkckYuS4Tei3BD4WCQg8/Gc5sd7v0YZHUVDawo29kglYmIXEj4EbnAAvC3BU4gw
-----END RSA PRIVATE KEY-----

passphrase:iloveudacity
```
