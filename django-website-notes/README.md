# Django website notes

Steps to create the website are mostly documented here.

See also:

[Django website notes](README.md)<br>
[Navigation bar notes](navbar.md)<br>
[Plans](../plans.md)<br>
[Defects](../defects.md)<br>
[Repository README](../README.md)

## Development machine

The Debian Linux distribution was for development and for the server.

### Text editors

For simple edits from a terminal use nano or vi.

For something more like an integrated development environment (IDE), [VSCodium](https://vscodium.com/) was used.

### Create a virtual environment before installing django etc.

```bash
apt install python3-venv
python -m venv ~/ocm-virt
```

### Activate and install django etc.

Activate the virtenv:

```bash
source ~/ocm-virt/bin/activate
```

Should see the terminal prompt now prefixed by '(ocm-virt)`.

```bash
pip install django
```

### Start the django project

```
cd ~/opencircuitmaker-website/www
django-admin startproject ocm
cd ocm
python manage.py startapp website
```

### Edit settings

```bash
nano ocm/settings.py
```

Add an element to the list INSTALLED_APPS [] named 'website'.

Set allowed hosts to include the URL, IP and localhost addresses, which will enable to run the site both from a server and from a local development machine without changes.

```python
ALLOWED_HOSTS = ["www.opencircuitmaker.com", "opencircuitmaker.com", "aaa.bbb.ccc.ddd", "127.0.0.1"]
```

For entry "aaa.bbb.ccc.ddd" use the IP address of the server, a fictitious example is "1.2.3.4"

### Migrate

Migrates various things, especially useful when using a database.

    python manage.py migrate

### First run

    python manage.py runserver

The default django site should appear.

Now used

    python manage.py createsuperuser

Answer the prompts to set superuser name, e-mail and password.

Then run the site and access it with /admin URL.

### .gitignore the database, virenv and __pycache__

Because the database is content not code, and these folders would muddy up the repository.

The __pycache__ is not needed in the git repo.

```bash
cd ~/opencircuitmaker-website
touch .gitignore
kate .gitignore
git add .gitignore
git add django-website-notes/
git commit -m "start django based website"
git push
```

For example:

```
www/ocm/db.sqlite3
django-venv/
**/__pycache__/
```

## Go live on a web server

### Server prerequisites

1. Debian Linux or equivalent installed
2. Logged into the server as root.
3. A minimal site is already running using Apache2, to test DNS, HTTPS etc.
4. Python3 is installed on the server.

### Minimal site

- For tests, enter this text in /var/www/html/index.html.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Open Circuit Maker</title>
    <link rel="stylesheet" href="style.css">
    <script src="script.js"></script>
  </head>
  <body>
    <br/>
    <h1>
        <a href="https://www.opencircuitmaker.com">www.opencircuitmaker.com is under construction</a>
    </h1>
    <br/>
    <a href="https://github.com/david-ocm/opencircuitmaker-website">The source for this website is on GitHub<>
  </body>
</html>
```

### Server notes

- check the server

```bash
systemctl status apache2
```


- If there is a message "AH00558: apache2: Could not reliably determine the server's fully qualified domain name" do the following

```bash
nano /etc/apache2/apache2.conf
```

Find the line with comment similar to this, and add the "ServerName 127.0.0.1".

    # Include the virtual host configurations:
    IncludeOptional sites-enabled/*.conf
    ServerName 127.0.0.1

Now restart apache and check again:

```bash
systemctl restart apache2
systemctl status apache2
```

### Update the operating system

Check for and apply operating system updates, then reboot the server.

If there were no updates, skip the reboot.

```bash
apt update && apt upgrade -y
systemctl reboot
```

### Install mod_wsgi module

Install then restart apache2.

```bash
apt install libapache2-mod-wsgi-py3
systemctl restart apache2
```

### Install pip and venv

```bash
apt install python3-pip
apt install python3-venv
```

### clone site code from GitHub

Connect to bash using SSH as root.
Configure root to use an administrator login and SSH key to access GitHub.

Delete existing html:

```bash
cd /var/www
rm -rf html
```

Clone:

```bash
git clone git@github.com:david-ocm/opencircuitmaker-website.git
```


### Update gitignore

The gitignore file should have at least this:

    www/ocm/db.sqlite3
    django-venv/

### Create Python virtenv and install Django

```bash
cd /var/www/opencircuitmaker-website/
python3 -m venv django-venv
source ./django-venv/bin/activate
```

Terminal prompt should change to:

    (django-venv) root@localhost:/var/www/opencircuitmaker-website#

Now install django:

```bash
pip install django
```

The output should look like:

```
Collecting django
  Using cached Django-4.2.4-py3-none-any.whl (8.0 MB)
Collecting asgiref<4,>=3.6.0
  Using cached asgiref-3.7.2-py3-none-any.whl (24
 kB)
Collecting sqlparse>=0.3.1
  Using cached sqlparse-0.4.4-py3-none-any.whl (41 kB)
Installing collected packages: sqlparse, asgiref, django
Successfully installed asgiref-3.7.2 django-4.2.4 sqlparse-0.4.4
```

### Create and init the database for this Django project

```bash
cd /var/www/opencircuitmaker-website/www/ocm
python manage.py migrate
./manage.py createsuperuser
```

Answer the prompts to set superuser name, e-mail and password.

### Copy the website database to the local dev machine

Run this from a bash terminal sesion on the local Debian development machine.

```bash
scp -r admin@opencircuitmaker.com:/var/www/opencircuitmaker-website/www/ocm/db.sqlite3 /home/david/opencircuitmaker-website/www/ocm/db.sqlite3
```

### Copy the local dev machine database to the  website

Run this from a bash terminal sesion on the local Debian development machine.

```bash
scp -r /home/david/opencircuitmaker-website/www/ocm/db.sqlite3 adminusername@opencircuitmaker.com:/var/www/opencircuitmaker-website/www/ocm/db.sqlite3
```

## Configure the web server for Django

```bash
nano /etc/apache2/sites-available/000-default.conf
```

Add this text:

```
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin admin@opencircuitmaker.com
        ServerName opencircuitmaker.com
        ServerAlias www.opencircuitmaker.com

        DocumentRoot /var/www/opencircuitmaker-website/www/ocm/

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/opencircuitmaker_error.log
        CustomLog ${APACHE_LOG_DIR}/opencircuitmaker_access.log combined

        Alias /static /var/www/opencircuitmaker-website/www/ocm/static
        <Directory /var/www/opencircuitmaker-website/www/ocm/static>
                Require all granted
        </Directory>

        Alias /media /var/www/opencircuitmaker-website/www/ocm/media
        <Directory /var/www/opencircuitmaker-website/www/ocm/media>
                Require all granted
        </Directory>

        <Directory /var/www/opencircuitmaker-website/www/ocm/ocm>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIDaemonProcess website python-path=/var/www/opencircuitmaker-website/www/ocm python-home=/var/www/opencircuitmaker-website/django-venv
        WSGIProcessGroup website
        WSGIScriptAlias / /var/www/opencircuitmaker-website/www/ocm/ocm/wsgi.py

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
RewriteEngine on
RewriteCond %{SERVER_NAME} =www.opencircuitmaker.com [OR]
RewriteCond %{SERVER_NAME} =opencircuitmaker.com
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```


```bash
nano /etc/apache2/sites-available/000-default-le-ssl.conf
```

Add this text:

```
<IfModule mod_ssl.c>
<VirtualHost *:443>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin admin@opencircuitmaker.com
        ServerName opencircuitmaker.com
        ServerAlias www.opencircuitmaker.com

        DocumentRoot /var/www/opencircuitmaker-website/www/ocm/

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/opencircuitmaker.com_error.log
        CustomLog ${APACHE_LOG_DIR}/opencircuitmaker.com_access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf

       Alias /static /var/www/opencircuitmaker-website/www/ocm/static
        <Directory /var/www/opencircuitmaker-website/www/ocm/static>
                Require all granted
        </Directory>

        Alias /media /var/www/opencircuitmaker-website/www/ocm/media
        <Directory /var/www/opencircuitmaker-website/www/ocm/media>
                Require all granted
         </Directory>

        <Directory /var/www/opencircuitmaker-website/www/ocm/ocm>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIDaemonProcess django_app python-path=/var/www/opencircuitmaker-website/www/ocm python-home=/var/www/opencircuitmaker-website/django-venv
        WSGIProcessGroup website
        WSGIScriptAlias / /var/www/opencircuitmaker-website/www/ocm/ocm/wsgi.py



Include /etc/letsencrypt/options-ssl-apache.conf
SSLCertificateFile /etc/letsencrypt/live/opencircuitmaker.com/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/opencircuitmaker.com/privkey.pem
</VirtualHost>
</IfModule>
```

### Allow www-data access to the database

These are both needed so that the database is usable by Apache2 and Django.

```bash
chown www-data: /var/www/opencircuitmaker-website/www/ocm/db.sqlite3
chown www-data: /var/www/opencircuitmaker-website/www/ocm/
```

### Enable the Django virtual host:

```bash
a2ensite 000-default.conf
a2ensite 000-default-le-ssl.conf
systemctl restart apache2
systemctl status apache2
```

### Test and then disable debug

Verify the site runs, even log in as admin by opening the URL with /admin appended.

**Warning** it is best to disable debug in settings.py.

See [Django Debug Info](https://docs.djangoproject.com/en/4.2/ref/settings/#debug)

Edit the file and change DEBUG = True to DEBUG = False

```bash
nano /var/www/opencircuitmaker-website/www/ocm/ocm/settings.py
```

After doing so, the site will give "Not Found" when accessed, at least until some content is added via python.

### Add to settings.py to handle static content for serving

```bash
nano /var/www/opencircuitmaker-website/www/ocm/ocm/settings.py
```
Add the following, replacing what is in settings.py:

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

At the top of settings.py add

```python
import os
````

To create the files in static/.

```bash
python manage.py collectstatic
```

Alternatively, run with the -n option to check the processing for errors without modifying anything.


### How to update the web site from GitHub

Log in as root on the server then:

```bash
cd /var/www/opencircuitmaker-website/
. ./django-venv/bin/activate
git pull
cd www/ocm/
python manage.py collectstatic
systemctl restart apache2
systemctl status apache2
```

## Create some basic site code using Python and Django

Now that the local development and remote server can share code via GitHub, it is time to start creating the site content.

All of this is done on the development machine, pushed to GitHub, then pulled to the remote server when ready to deploy.

Use VSCodium  to open the directory  opencircuitmaker-website/.

### Edit www/ocm/urls.py.

At the top of the file, add:

```python
from django.urls import path, include
```

Add the include below to urlpatterns:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
]
```

The empty '' path means the base URL of the site such as something.com/.

### Create a file www/ocm/website/urls.py:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Edit the file www/ocm/website/views.py:

```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})
```

### Create  a template html file for home

Django uses a template for the  html files, always stored in the same templates directory.

Create a directory www/ocm/website/templates/ and in it create a file home.html:

```html
<h1>Open Circuit Maker coming soon - under construction!</h1>
```

### Create a template to reuse across all website pages

In website/templates/ create base.html.

Go to [Bootstrap](https://getbootstrap.com/), select Docs and scroll down to the section "Include Bootstrap's CSS and JS". Copy the code into base.html.

Change the title to "Open Circuit Maker".

Replace line with "Hello World" with:

```html
{% block content %}

{% endblock %}
```

Django will pull the content from an html template into the block.

Edit home.html and in the first line add:

```html
{% extends 'base.html' %}
```

Then surround the existing html with:

```html
{% block content %}

{% endblock %}
```

### Make the template nicer

Add a line break before and wrap the content block in a divider (div).

In website/templates/base.html:

```html
    <div class="container">
        <br/>
        {% block content %}

        {% endblock %}
    </div>
```

### Add a navigation bar

Create a new file website/templates/navbar.html:

Go back to [Bootstrap](https://getbootstrap.com/), select Docs, then scroll down on the left side to Components, Navbar.

Select a Navbar and copy in the html code.

In website/templates/base.html add at the top of body:

```html
{% include 'navbar.html' %}
```

Try it out on the server. 

## Further reading

[Navigation bar notes](./navbar.md)
