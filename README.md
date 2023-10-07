# Picture Share API
App created with Django and DRF to allow users and share their images.

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
To load built plan run manage.py loaddata basic_tiers.json after initial migrations.