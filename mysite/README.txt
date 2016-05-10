1) Install Django:  

       sudo apt-get install python-django

2) Follow the link to setup postgresql with Django on Ubuntu 14.04:

       https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

3) Create Database Schema for running the application

       The postgres database must have the schema used for the application as mentioned in the README for the Flask application.

4) Start the django project

       django-admin startproject mysite

5) This will create the mysite directory in the current directory. This will create the following directory structure:

   mysite/
       manage.py
       mysite/
           __init__.py
           settings.py
           urls.py
           wsgi.py

6) Copy the files from the github link to mysite directory.

7) Edit the settings.py to enter the database name, Username and password of the PostgreSql database.

8) Execute the below command to start the website:

       python manage.py runserver 
