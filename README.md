# Picture Share API
App created with Django and DRF to allow users and share their images.

# Technologies used
Python 3.11
Django 4.2.5
Django REST framework 3.14.0
Pillow 10.0.1


## Features
users can upload images via HTTP request

users can list their images

there are three builtin account tiers: Basic, Premium and Enterprise:

users that have "Basic" plan after uploading an image get:

a link to a thumbnail that's 200px in height

users that have "Premium" plan get:

a link to a thumbnail that's 200px in heigh

a link to a thumbnail that's 400px in height

a link to the originally uploaded image

users that have "Enterprise" plan get

a link to a thumbnail that's 200px in height

a link to a thumbnail that's 400px in height

a link to the originally uploaded image

ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))

# Setup
After running initial migrations run manage.py loaddata basic_tiers.json to populate database with basic user tiers. Create admin account with manage.py createsuperuser and then in admin panel grant admin enterprise tier account.

localhost:8000/images/ - to see uploaded images by user

localhost:8000/upload/ - to upload image

localhost:8000/expiring-links/ - to generate expiring links