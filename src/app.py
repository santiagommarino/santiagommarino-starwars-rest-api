"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict()for user in users])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person: 
        return jsonify(person.to_dict())
    return jsonify({'message': 'person not found'}),404

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.to_dict()for person in people])

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.to_dict()for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet: 
        return jsonify(planet.to_dict())
    return jsonify({'message': 'planet not found'}),404

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        favorites = Favorite.query.filter_by(user_id=user_id).all() 
        return jsonify([favorite.to_dict()for favorite in favorites])
    return jsonify({'message': 'planet not found'}),404


@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def post_favorites_planet(planet_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    if planet and user:
        favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.to_dict()), 201
    return jsonify({'message':'User and Planet not found'}),404
    

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message':'Favorite deleted'}),200
    return jsonify({'message':'Favorite not found'}), 404

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorites_people(people_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    people = People.query.get(people_id)
    if people and user:
        favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.to_dict()), 201
    return jsonify({'message':'User and person not found'}),404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.args.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message':'Favorite deleted'}),200
    return jsonify({'message':'Favorite not found'}), 404

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)













