# Description
* This is a Django app that allows users to create shortened bookmarks.
* This was built by Ryan Burton and Will Butts
* All data is generated randomly and any real links are purely coincidental.

## Building the Database:

* First run $ pip install -r requirements.txt.
* You will need to have a PostgreSQL server running.  For details on getting it set up check https://github.com/tiyd-python-2015-08/course-resources/blob/master/week7/PostgreSQL-and-Django.md
* For info on the PostgresSQL information check settings.py
* Run python manage.py makemigrations
* Run python manage.py migrate to setup the database
* Run python manage.py generate_data.  Be aware this can take quite some time.

## Using the app

* First run $ python manage.py runserver to start the server
* Next open a browser and go to localhost:8000/ to begin.
* You can click the recent button up top on the login page to jump right in, or create a new user.
* If you want to see the graphs for the generated users their usernames can be found on the recent page and their passwords are all "password".
* Clicking the shortened bookmark or long bookmark will navigate you out of the site, and sometimes to a real site so click at your own risk!
* Clicking on a user will take you to their page that has all the links they've created.
* Clicking home (in the navbar) will take you to your home page where you will have additional functionality.  Try clicking on the title of a link (only available on your homepage).
