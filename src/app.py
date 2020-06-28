import os
import datetime
from .auth import AuthError, requires_auth
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import Actor, Movie, setup_db, \
      db_drop_and_create_all, db_init_records

ENTRIES_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    setup_db(app)
    # db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Autorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, POST, DELETE, OPTIONS'
        )
        return response

    def paginate_output(response, selection):
        page = request.args.get('page', 1, type=int)
        start = ENTRIES_PER_PAGE*(page-1)
        end = start+ENTRIES_PER_PAGE
        output = list(obj.to_dict() for obj in selection)
        return output[start:end]

# ------------------------------------------------------------------
# Api endpoints
# ------------------------------------------------------------------

    @app.route('/')
    def index():
        return 'Home'

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.order_by(Actor.id).all()
        if len(selection) == 0:
            abort(404)
        try:
            actors = paginate_output(request, selection)
            return jsonify({
                'success': True,
                'actors': actors
            }), 200
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(payload):
        body = request.get_json()
        # print("body:",body)
        if body is None:
            abort(400)
        try:
            name = body['name']
            gender = body['gender']
            age = int(body['age'])
            new_actor = Actor(
                name=name,
                gender=gender,
                age=age
            )
            Actor.insert(new_actor)
            return jsonify({
                'success': True,
                'new_actor': new_actor.to_dict()
            }), 200
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actors(payload, actor_id):
        current_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if current_actor is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(400)
        try:
            name = body.get('name', '')
            gender = body.get('gender', '')
            age = body.get('age', '')
            if name != '':
                current_actor.name = name
            if gender != '':
                current_actor.gender = gender
            if age != '':
                current_actor.age = int(age)
            Actor.update(current_actor)
            return jsonify({
                'success': True,
                'actor_updated': current_actor.to_dict()
            }), 200
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        current_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if current_actor is None:
            abort(404)
        try:
            Actor.delete(current_actor)
            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200
        except:
            abort(422)

    # -----------------
    # Movies endpoints
    # -----------------

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.order_by(Movie.id).all()
        if len(selection) == 0:
            abort(404)
        try:
            output = paginate_output(request, selection)
            return jsonify({
                'success': True,
                'movies': output
              }), 200
            except:
                abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        body = request.get_json()
        # print('body:',body)
        # print('request:',request)
        if body is None:
            abort(400)
        try:
            title = body['title']
            date_str = body['year']
            director = body['director']
            # print(title,date_str,director)
            new_movie = Movie(
                title=title,
                year=int(date_str),
                director=director
            )
            Movie.insert(new_movie)
            return jsonify({
                'success': True,
                'new_movie': new_movie.to_dict()
            }), 200
            except:
                abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movies(payload, movie_id):
        current_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if current_movie is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(400)
        try:
            title = body.get('title', '')
            date_str = body.get('year', '')
            director = body.get('director', '')
            if title != '':
                current_movie.title = title
            if date_str != '':
                # year = datetime.strptime(date_str, '%Y-%m-%d').date()
                current_movie.year = int(date_str)
            if director != '':
                current_movie.director = director
            Movie.update(current_movie)
            return jsonify({
                'success': True,
                'movie_updated': current_movie.to_dict()
            }), 200
            except:
                abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        current_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if current_movie is None:
            abort(404)
        try:
            Movie.delete(current_movie)
            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200
        except:
            abort(422)

    # -----------------------------------------------------------------------------
    # Error Handlers
    # -----------------------------------------------------------------------------

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
        }), error.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
