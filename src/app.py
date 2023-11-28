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
from models import db, User, People, Favorite, Planet
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# /people get a list of all the people in the database
@app.route('/people', methods=['GET'])
def get_people():
    peoples = People.query.all()
    people_list = []
    for people in peoples:
        people_dict = {

            'id': people.id,
            'name': people.name,
            'height': people.height,
            'mass': people.mass,
            'hair_color': people.hair_color,
            'skin_color': people.skin_color,
            'eye_color': people.eye_color   
            }
        people_list.append(people_dict)
    return jsonify(people_list),200


# people/<int:people_id> get a one single people information
@app.route('/people/<int:people_id>', methods=['GET'])
def get_particular_people(people_id):
    people = People.query.get(people_id) 
    if people:
        return jsonify({
            'name': people.name,
            'height': people.height,
            'mass': people.mass,
            'hair_color': people.hair_color,
            'skin_color': people.skin_color,
            'eye_color': people.eye_color 
        })
    else:
        return jsonify({'error': 'user not found'}), 404
    



# /planets get a list of all the planets in the database
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planet_list = []
    for planet in planets:
        planet_dict = {

             "id": planet.id,
            "name": planet.name,
            "rotation_period": planet.rotation_period,
            "orbital_period": planet.orbital_period,
            "diameter": planet.diameter,
            "climate": planet.climate,
            "graviti": planet.graviti

            }
        planet_list.append(planet_dict)
    return jsonify(planet_list),200


# planet/<int:planet_id> get a one single planet information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_particular_planet(planet_id):
    planet = Planet.query.get(planet_id) 
    if planet:
        return jsonify({
            
            'name': planet.name,
            'height': planet.height,
            'mass': planet.mass,
            'hair_color': planet.hair_color,
            'skin_color': planet.skin_color,
            'eye_color': planet.eye_color 

        })
    else:
        return jsonify({'error': 'planet not found'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
