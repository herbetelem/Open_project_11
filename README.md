# Open_project_11

# Project Openclassroom : Améliorez une application Web Python par des tests et du débogage
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)  [![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](http://forthebadge.com).

this project aims to improve and correct an existing project, as well as to do unit tests

### library and tools

- [https://www.djangoproject.com/](https://flask.palletsprojects.com/en/2.3.x/) Flask
- [https://www.django-rest-framework.org/](https://docs.python.org/fr/3/library/unittest.html) Unittest
- https://coverage.readthedocs.io/en/7.2.7/ Coverage

### Prerequisites

You should have Python on you're OS and set a Venv before continue if you want to have a clean env

You have to install the requirements with the command ``pip3 install -r requirements.txt``

For Flask you have to set the server with this command ``export FLASK_APP=server.py``

## Launching

For launch the projet use the command ``Flask run``

If you want to launch the test use the command ``python3 -m unittest test_flask.py``

If you want to see the percent of coverage unittest, run the command ``python -m coverage run -m unittest`` then this one ``python -m coverage report ``


## Functional

This project aims to allow bodybuilding associations to be able to register in tournaments.
However there are some restrictions (the club must have the required points, each club can only take a maximum of 12 places per tournament, and we can only take places in future tournaments)

## Made with

* [Visual Studio Code](https://code.visualstudio.com/) - Code editor


## Author

* **Hadrien Louppe Herbet** _alias_ [@herbetelem](https://github.com/herbetelem)


