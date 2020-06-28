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
        self.casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3THoxb2poNF8tdUFPcXdLS3NYSiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktMjAxNWJiNS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTlkODgzMjUzMDgwMDEzODFkZGQzIiwiYXVkIjoiYWN0b3JzIiwiaWF0IjoxNTkzMzIxMzAxLCJleHAiOjE1OTM0MDc3MDEsImF6cCI6ImplM3ZJUEpVblNBcjdUUkhBZENScExVU2Q4SW01MU53Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Ky91A7Rn6SuBF9044xBuRc-lu5QtFWSlFgOs1VXgAyv2QnScSC4Nog1gjR-W_6eN2eR-U4U-SOi7OtpdeSYCBYpOFBkRDOgU2x1RsJRwl73gIGAQM--TPHljGYeqqSubVYEjhjwCvRxkKgwj6JRQ6hwxpLkEhwXdcuzok0CmkWJxkEu1vdH3nmoMHWbgMyqBP0CW95mMFkUyCpc4HbXJM9c6J4C_C62G9p90FxjPTZsgAy0CVW7GUcCMk1O58F3H61qU2hzyD6J4SNc9hjM4dJuzWh2OZwpvb1tU3YGyizvHoYPGYffxTxYnFvJTcpiEC3sE4e3JhRfCBpxaCRUFiw"
        self.casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3THoxb2poNF8tdUFPcXdLS3NYSiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktMjAxNWJiNS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkNGIyMWJiZWI2ODQwYzkzOWEzYmNiIiwiYXVkIjoiYWN0b3JzIiwiaWF0IjoxNTkzMzIxMzgwLCJleHAiOjE1OTM0MDc3ODAsImF6cCI6ImplM3ZJUEpVblNBcjdUUkhBZENScExVU2Q4SW01MU53Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.YPHmgv2CDPxAdMXDCzKKI0FT6jqkYMfaf-MFcnyRR0d17Cz1A-hCaS_UTwQsGl5cvjUIOfnny8T5ZsFRI58cljn62vWJa43jxun_u2SKm0Ls6t8vrzdU0YQHdlP451IqWkKLBAai_uhQKlTpoMwHUtgFtfsjiVBPSIeDvWv2Pr64ckH6BUstiS7MNoaxC8n4hkNo7FzsR7sU_00JeQpTelKi73BIU0YxxCU5vvfRaW14YVBFF1ZaEx-cH8XtCG_lwbDnqTDxFyxzjfZYbYh8eEOtrQQkrwoOD-tUxry2vhNdt3D6MzI6l7HXLMZDjt3IkJd-mWYFnCrrha3aMC5bcw"
        self.executive_producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3THoxb2poNF8tdUFPcXdLS3NYSiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktMjAxNWJiNS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkOGE3MDRkZWY3NWQwYmVmYmMwNDRmIiwiYXVkIjoiYWN0b3JzIiwiaWF0IjoxNTkzMzIxNDI5LCJleHAiOjE1OTM0MDc4MjksImF6cCI6ImplM3ZJUEpVblNBcjdUUkhBZENScExVU2Q4SW01MU53Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.xrvoTwblCQIewj5PDFoHZTPWyaJ-LmHSfGfZt8S6_7hVelgiOllCGmtszlP_WobNJ1lWzE_mKaz2s2Bnya_IZaCwc--k-knPS_FcA6eFtpoVRnTSFIKpSpE8vdHq_5Gf2sBjnyb3Yrwqycvy3FUmdszoNoFy2u8QvnnkZKF4IvS0gHRtBxpon9RO5aAzs1uxcSIA3EDo1YCetJMVZZxHQc6hTCFIjzXQUTLLbpxuTsJp-Eym6zBzHNitT6cRY--USRuAnvTU--SZXN9LVH4azU0qk60zrDy5FzUNryDFGT8I28i_nPNIX5thvubNr8y-dvxX08AuA-p4DDOhIiUdng"
        
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

        self.assertEqual(res.status_code,401)
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
