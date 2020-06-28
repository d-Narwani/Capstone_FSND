# Capstone_FSND
Casting Agency App

Heroku Link: https://fsndfinal2.herokuapp.com/

# Motivation for Project

This app is the capstone project of Udacity's Full Stack Web Developer program. It is built to streamline the mnaging process of casting agencies. By using the app, the casting agency can input actors and movies and have role based access to the data. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the main directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

From within the `src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py` file to find the application. 

### Roles:

1. Casting Assistant Permissions:
    GET:actors
    GET:movies

2. Casting Director Permissions:
All permissions a Casting Assistant has + 
    POST:actor
    DELETE:actor
    PATCH:actor
    PATCH:movie

3. Executive Producer Permissions:
All permissions a Casting Director has + 
    POST:movie
    DELETE:movie
    
#### Tokens:
These are included in the setup.sh file as well as in the test_app.py file.

##### API Endpoints:

1. GET /actors gets you all the available actors limited to 10 per page
   - Request parameters(optional): page:int
   - Response format:
{
  "actors": [
    {
      "age": 25,
      "gender": "Female",
      "id": 1,
      "name": "Dorika"
    },
    {
      "age": 25,
      "gender": "Male",
      "id": 2,
      "name": "Lambda"
    }
  ],
  "success": true
}

2. POST /actors
   - Request body: {name:string, age:int, gender:string}
   - Response Format:
   
{
  "new_actor": {
    "age": 1999,
    "gender": "Male",
    "id": 3,
    "name": "Dhaval",
  },
  "success": true
}

3. PATCH /actors/<actor_id> 
   - Request parameters: actor_id:int
   - Response format:

{
  "actor_updated": {
    "age": 25,
    "gender": "Female",
    "id": 1,
    "name": "Haiya",
    "performances": []
  },
  "success": true
}

4. DELETE /actors/<actor_id>
   - Request parameters: actor_id:int
   - Response format:

{
  "deleted": 2, 
  "success": true
}

5. GET /movies gets you all the available movies limited to 10 per page
   - Request parameters(optional): page:int
   - Response format:
{
  "movies": [
    {
      "director": "Dabra",
      "id": 1,
      "title": "Dorika first Movie",
      "year": 2020
    },
    {
      "director": "Dhaval",
      "id": 2,
      "title": "Dhaval first movie",
      "year": 1999
    }
  ],
  "success": true
}

6. POST /movies
   - Request body: {title:string, year:int, director:string}
   - Response format:
{
  "new_movie": {
    "director": "Dhaval",
    "id": 2,
    "title": "Dhaval first movie",
    "year": 1999
  },
  "success": true
}

7. PATCH /movies/<movie_id>
   - Request parameters: movie_id:int
   - Response format:

{
  "movie_updated": {
    "director": "Dabra",
    "id": 1,
    "title": "Dorika first Movie",
    "year": 2020
  },
  "success": true
}


8. DELETE /movies/<movie_id> 
   - Request parameters: movie_id:int
   - Response format:
{
  "deleted": 2,
  "success": true
}

9. GET /
   - Request parameters: movie_id:int
   - Response format:
   'Home'


## Testing
To run the tests, run
```
dropdb final_test
createdb final_test
python test_app.py
```
