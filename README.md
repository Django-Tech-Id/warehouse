# [Warehouse] Sistem Informasi Gudang

Warehouse is an application for warehouse management. It's writtern on Python 3 and Django Framework.

<br />

# Features

- Customer Management
- Supplier Management
- Warehouse Management
- Category Management
- Product Management
- Purchase Management
- Sales Management
- Inventory Management
- RFID Tracking
- Tracking History
- Rest API
- User Management
- An Intuitive Dashboard

<br />

# Screenshot

> Dashboard

![Dashboard - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/dashboard.png?raw=true)

> Customer List

![Customer List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/customer.png?raw=true)

> Customer Form

![Customer Form - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/customerform.png?raw=true)

> Customer Print

![Customer Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/customerprint.png?raw=true)

> Supplier List

![Supplier List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/supplier.png?raw=true)

> Warehouse List

![Warehouse List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/warehouse.png?raw=true)

> Category List

![Category List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/category.png?raw=true)

> Product List

![Product List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/product.png?raw=true)

> Product Print

![Product Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/productprint.png?raw=true)

> Purchase List

![Purchase List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/buy.png?raw=true)

> Purchase Print

![Purchase Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/buyprint.png?raw=true)

> Purchase Invoice

![Purchase Invoice - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/buyinvoice.png?raw=true)

> Sales List

![Sales List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/sell.png?raw=true)

> Sales Print

![Sales Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/sellprint.png?raw=true)

> Sales Invoice

![Sales Invoice - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/sellinvoice.png?raw=true)

> Moveout List

![Moveout List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/moveout.png?raw=true)

> Moveout Print

![Moveout Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/moveoutprint.png?raw=true)

> Moveout Evidence

![Moveout Invoice - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/moveoutinvoice.png?raw=true)

> Movein List

![Movein List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/movein.png?raw=true)

> Moveout Print

![Movein Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/moveinprint.png?raw=true)

> Moveout Evidence

![Movein Invoice - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/moveininvoice.png?raw=true)

> Inventory List

![Movein List - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/inventory.png?raw=true)

> Inventory Print

![Movein Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/inventoryprint.png?raw=true)

> API History

![API History - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/apihistory.png?raw=true)

> API Warehouse

![Movein Print - Sistem Informasi Gudang](https://github.com/Django-Tech-Id/warehouse/blob/master/media/screenshot/apiwarehouse.png?raw=true)

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Django-Tech-Id/warehouse.git
$ cd warehouse
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Storage
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

<br />

## Code-base structure

The project is coded using a simple and intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app logic and serve the static assets
   |    |-- settings.py                    # Django app bootstrapper
   |    |-- wsgi.py                        # Start the app in production
   |    |-- urls.py                        # Define URLs served by all apps/nodes
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |         |
   |         |-- includes/                 # HTML chunks and components
   |         |    |-- navigation.html      # Top menu component
   |         |    |-- sidebar.html         # Sidebar component
   |         |    |-- footer.html          # App Footer
   |         |    |-- scripts.html         # Scripts common to all pages
   |         |
   |         |-- layouts/                  # Master pages
   |         |    |-- base-fullscreen.html # Used by Authentication pages
   |         |    |-- base.html            # Used by common pages
   |         |
   |         |-- accounts/                 # Authentication pages
   |         |    |-- login.html           # Login page
   |         |    |-- register.html        # Register page
   |         |
   |      index.html                       # The default page
   |     page-404.html                     # Error 404 page
   |     page-500.html                     # Error 404 page
   |       *.html                          # All other HTML pages
   |
   |-- authentication/                     # Handles auth routes (login and register)
   |    |
   |    |-- urls.py                        # Define authentication routes  
   |    |-- views.py                       # Handles login and registration  
   |    |-- forms.py                       # Define auth forms  
   |
   |-- app/                                # A simple app that serve HTML files
   |    |
   |    |-- views.py                       # Serve HTML pages for authenticated users
   |    |-- urls.py                        # Define some super simple routes  
   |
   |-- requirements.txt                    # Development modules - SQLite storage
   |
   |-- .env                                # Inject Configuration via Environment
   |-- manage.py                           # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

> The bootstrap flow

- Django bootstrapper `manage.py` uses `core/settings.py` as the main configuration file
- `core/settings.py` loads the app magic from `.env` file
- Redirect the guest users to Login page
- Unlock the pages served by *app* node for authenticated users

<br />

## Deployment

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/), [Gunicorn](https://gunicorn.org/), and [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

### [Docker](https://www.docker.com/) execution
---

The application can be easily executed in a docker container. The steps:

> Get the code

```bash
$ git clone https://github.com/app-generator/django-dashboard-atlantis.git
$ cd django-dashboard-atlantis
```

> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:5005` in your browser. The app should be up & running.

<br />

### [Gunicorn](https://gunicorn.org/)
---

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

> Install using pip

```bash
$ pip install gunicorn
```
> Start the app using gunicorn binary

```bash
$ gunicorn --bind=0.0.0.0:8001 core.wsgi:application
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.


<br />

### [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)
---

Waitress (Gunicorn equivalent for Windows) is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones that live in the Python standard library.

> Install using pip

```bash
$ pip install waitress
```
> Start the app using [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)

```bash
$ waitress-serve --port=8001 core.wsgi:application
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

<br />

## Credits & Links

- [Django](https://www.djangoproject.com/) - The official website
- [Boilerplate Code](https://appseed.us/boilerplate-code) - Index provided by **AppSeed**
- [Boilerplate Code](https://github.com/app-generator/boilerplate-code) - Index published on Github

<br />

---
[Django Dashboard](https://appseed.us/admin-dashboards/django) Atlantis Lite - Provided by **AppSeed [App Generator](https://appseed.us/app-generator)**.
