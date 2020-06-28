import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.casting_assistant = os.environ['casting_assistant']
        self.casting_director = os.environ['casting_director']
        self.executive_producer = os.environ['executive_producer']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Abra",
            "age": 20,
            "gender": "male",
        }

        self.INVALID_NEW_ACTOR = {
            "title": "Haiya"
        }

        self.VALID_UPDATE_ACTOR = {
            "name": "Dabra"
        }

        self.INVALID_UPDATE_ACTOR = None

        self.VALID_NEW_MOVIE = {
            "title": "Abra ka Dabra",
            "year": 2019,
            "director": "Dhaval",
        }

        self.INVALID_NEW_MOVIE = {
            "title": "XYZ",
            "rating": 10,
            "director": "Zoomba"
        }

        self.VALID_UPDATE_MOVIE = {
            "year": 3000
        }

        self.INVALID_UPDATE_MOVIE = None

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header not found.")

    def test_get_actors(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actors', data)

    def test_create_actor_with_casting_assistant(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('new_actor', data)

    def test_422_create_actor(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        }, json=self.INVALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_actor_info(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        }, json=self.VALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor_updated', data)

    def test_400_update_actor_info(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        }, json=self.INVALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_with_casting_assistant(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue('deleted', 1)

    def test_404_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movies', data)

    def test_create_movie_with_casting_assistant(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_movie(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('new_movie', data)

    def test_422_create_movie(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer)
        }, json=self.INVALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_info(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        }, json=self.VALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie_updated', data)

    def test_400_update_movie_info(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        }, json=self.INVALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_casting_director(self):
        """Failing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue('deleted', 1)

    def test_404_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
