from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from datetime import *
from datetime import date


db = SQLAlchemy()



def setup_db(app):
    '''binds a flask application and a SQLAlchemy service'''
    app.config.from_object('.config')
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test records.'''

    new_actor = (Actor(
        name = 'Dhaval',
        gender = 'Male',
        age = 25
        ))

    new_movie = (Movie(
        title = 'Dhaval first Movie',
        year = 2020,
        director = 'Dabra'
        ))

    new_performance = Performance.insert().values(
        movie_id = new_movie.id,
        actor_id = new_actor.id,
        actor_fee = 1000.00
    )

    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_performance) 
    db.session.commit()


#-----------------------------------------------------------------------------
# Association table of actors and movies
#-----------------------------------------------------------------------------

Performance = db.Table('Performance',
                db.Column(('movie_id'),db.Integer,db.ForeignKey('movie.id')),
                db.Column(('actor_id'),db.Integer,db.ForeignKey('actor.id')),
                db.Column('actor_fee',db.Float))




class  Actor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"Actor id:'{self.id}',name='{self.name}'"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'gender':self.gender,
            'age':self.age,
            'performances':list(map(Movie.to_dict,self.performances))
        }




class Movie(db.Model):
    id = id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    director = db.Column(db.String(100),nullable=False)
    actors = db.relationship('Actor',secondary=Performance,backref=db.backref('performances'),lazy='joined')

    def __repr__(self):
        return f"Movie id:'{self.id}',title:'{self.title}'"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'director':self.director,
            'year':self.year,
            'actors':[obj.id for obj in self.actors]
        }


