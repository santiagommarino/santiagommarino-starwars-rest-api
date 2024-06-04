from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    persons_name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(50), nullable=True)
    mass = db.Column(db.String(50), nullable=True)
    hair_color = db.Column(db.String(50), nullable=True)
    skin_color = db.Column(db.String(50), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    birth_year = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.persons_name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
        }
    
class Planets(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    planets_name = db.Column(db.String(50), nullable=False)
    orbital_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.Integer, nullable=True)
    population= db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(50), nullable=True)
    terrain = db.Column(db.String(50), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    created = db.Column(db.String(50), nullable=True)
    edited =  db.Column(db.Integer, nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(50), nullable=True)

    

    def serialize(self):
        return {
            "id": self.id,
            "planets_name": self.planets_name,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "rotation_period": self.rotation_period,
            "created": self.created,
            "edited": self.edited,
            "diameter": self.diameter,
            "url": self.url
        }