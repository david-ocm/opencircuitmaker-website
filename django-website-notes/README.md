# django website notes

Notes on building the website using django.

## Development machine

The Debian 12 Linux was for development.

On the web server itself, a virtual environment is **not** used.

### Create a virtual environment before installing django etc.

```bash
sudo apt install python3-venv
python -m venv ~/ocm-virt
```

### Activate and install django etc.

Activate the virtenv:

    source ~/ocm-virt/bin/activate

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

    kate ocm/settings.py

or use nano etc. as editor

Add an element to thje list INSTALLED_APPS []

        'website',

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

The database is content not code.

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

1. Debian 12 or equivalent installed, using a cloud provider, home machine etc.
2. Logged into the server with an account that has sudo via ssh.
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
sudo systemctl status apache2
```


- If there is a message "AH00558: apache2: Could not reliably determine the server's fully qualified domain name" do the following

```bash
sudo nano /etc/apache2/apache2.conf
```

Find the line with comment similar to this, and add the "ServerName 127.0.0.1".

    # Include the virtual host configurations:
    IncludeOptional sites-enabled/*.conf
    ServerName 127.0.0.1

Now restart apache and check again:

```bash
sudo systemctl restart apache2
sudo systemctl status apache2
```

### Update the operating system

Check for and apply operating system updates, then reboot the server.

If there were no updates, skip the reboot.

```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl reboot
```

### Install mod_wsgi module

Install then restart apache2.

```bash
sudo apt install libapache2-mod-wsgi-py3
sudo systemctl restart apache2
```

### Install pip and venv

```bash
sudo apt install python3-pip
sudo apt install python3-venv
```

### clone site code from GitHub

```bash
cd ~
git clone git@github.com:david-ocm/opencircuitmaker-website.git
```

### Update gitignore

The gitignore file should have at least this:

    www/ocm/db.sqlite3
    django-venv/

### Create Python virtenv and install Django

```bash
cd opencircuitmaker-website/
python3 -m venv django-venv
source ./django-venv/bin/activate
pip install django
```

Terminal prompt should change to:

    (django-venv) adminusername@hostname:~/opencircuitmaker-website$

Now install django:

```bash
pip install django
```

The output should look like:

```
Collecting django
  Using cached Django-4.2.4-py3-none-any.whl (8.0 MB)
Collecting asgiref<4,>=3.6.0
  Using cached asgiref-3.7.2-py3-none-any.whl (24 kB)
Collecting sqlparse>=0.3.1
  Using cached sqlparse-0.4.4-py3-none-any.whl (41 kB)
Installing collected packages: sqlparse, asgiref, django
Successfully installed asgiref-3.7.2 django-4.2.4 sqlparse-0.4.4
```

### Create database on the server if not already there

```bash
cd ~/opencircuitmaker-website/www/ocm
python manage.py migrate
```
