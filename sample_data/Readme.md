## To generate sample db:

1. create clean virtualenv
   * `pip install virtualenv`
   * `vitrualenv env_name`
2. source virtual env
   * `source env_name/bin/activate`
3. make sure required packages are installed
   * `pip install django pandas plotly requests PyGithub`
4. generate sql from models
   * `python manage.py makemigrations`
5. run sql against db
   * `python manage.py migrate`
6. open interactive python shell
   * `python manage.py shell`
7. generate db objects
   * `>>>from corona_plots import db_test`
