# Care360
A website for children aged 8-12, focusing on preventing injuries of older Australians.

## Contents of this file

* Introduction
* Requirements
* Setup Guidelines
* Deployment Guidelines

---------------------------------------------------------------------------
INTRODUCTION

--------------------------------------

Care360 is a website developed for children aged 8-12 to help them learn about potential risks associated to their grandparent's health and house. Grandchildren, along with their grandparents, will assess the questionnaires and with the recommendations from the website, they will try to make little changes to their grandparents lifestyle which may prevent big injuries.

* URL: https://www.care360.team/

--------------------------------------

REQUIREMENTS

--------------------------------------

* IDE : Visual Studio Code 
* Version Control : GitHub 
* Web Development : Flask, HTML5, CSS, JavaScript, Bootstrap
* Database : SQLlite 
* Data Wrangling : Python

--------------------------------------

Setup Guidelines

--------------------------------------

To develop the web application, we decided to use flask as framework. Before I start building the Flask app, I created a conda environment where the dependencies required to run the app are held. A conda environment is simply an isolated directory containing a particular set of appropriate conda packages for the job. The dependencies required for running this specific app are in requirements.txt file. I created virtual environment by typing “conda create –n myvirtualenv1” command.
I used “pip install –r requirements.txt” to install required dependencies. Some essential libraries are:
* FlaskSQLAlchemy which is a Flask extension that adds SQLAlchemy support to the application.
* FlaskWTF which is the simple Flask & WTForms integration which includes CSRF, file upload, and reCAPTCHA.
* Flask-OAuthlib which is designed to be a replacement for Flask-OAuth.
* Flask-DebugToolbar which adds an overlay toolbar to Flask applications that contains useful debugging knowledge.
* Jinja which is a modern and designer-friendly python templating language, it has strong automatic XSS-prevention HTML escaping framework.
When all the dependencies are installed, then I activated the virtual environment by typing “conda activate myvirtualenv1”. I created a python script called ‘app.py’ inside a folder called ‘Project’ to run the application.
After the conda environment is created and activated and the dependencies are installed, I changed directory to the folder where app.py was saved by writing ‘:D\Project’.

---------------------------------------------

Deployment Guidelines

------------------------------------------------

This document specifies the steps needed to deploy the application to the cloud server(heroku) and how changes made to the local working code line can be pushed to the testing environment to verify that the build passes on the server as well.
Below are the things that were taken into consideration for creating, committing and pushing the application from the local development environment to the cloud server.
1. Heroku Account Setup: Heroku provides free 750 hours of dynamos to its users and supports a wide variety of applications, so we decided to use heroku as the hosting provider. The first thing to do is create a heroku account with your personal email account. Select “Create new app” on the dashboard and select the language of the application as Python.
2. Heroku CLI: Heroku CLI gives the security to push the code line to the cloud server using the command prompt by authenticating with your heroku account credentials. We need to download and install heroku CLI in order to push the code to the server.
3. Git Bash: In order to deploy the application to the remote cloud server, we need to install git in the computer. After following these steps, there are additional things that are required for the application to work correctly on the server.
4. Proc file: This file is necessary to specify the server that will be used to host the application on the cloud. We have used gunicorn as the deployment server.
5. Requirements.txt file: The root application should have requirements.txt file mentioning the versions of the libraries being used in the application. We can easily get the libraries required in the application with the following command Pip freeze > requirements.txt
6. Further commands:
* Heroku login
* heroku git:clone -a “your heroku repository name”
* cd “your heroku repository name”
Then make changes to the code and
* git add .
* git commit -am “commiting changes that are being made”
* git push heroku master
