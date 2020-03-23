# offershub-test-project
This is a test-task project for Offershub.

# Setup
Following environment variables should be specified in your shell session:
* `export ASANA_TOKEN=your_asana_token`
* `export POSTGRES_PASSWORD=any_password`
* `export DJANGO_SECRET_KEY=your_secret_key`
* `export DJANGO_DEBUG=1` (if you want)
* `export DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"`

# Start
* clone this repository
* `docker-compose up` to build and run containers
* `docker-compose exec web python manage.py migrate` to apply all the migrations
* `docker-compose exec web python manage.py createsuperuser` to create a superuser to access django-admin interface
* open in your browser http://localhost:8000 and login

## Notes
The first time you hit a model name in the interface it is going to fetch all the data accessible with your token. That may take some time.
Later it will only update what is necessary.
