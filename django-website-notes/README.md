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

### .gitignore the database

Sorry, that part must not be so open.

    cd ~/opencircuitmaker-website
    touch .gitignore
    kate .gitignore

