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


#[GET] /users Get a list of all the blog post users.
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]

    return jsonify(users_list), 200

#[GET] /users/favorites Get all the favorites that belong to the current user.
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)

    if user in None:
        return jsonify({'message': 'User ot found'}), 404
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorites_list = [favorite.serialize() for favorite in favorites]

    return jsonify({favorites_list}), 200

#[POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'message':'user_id is required'}), 400
    user_id = data['user_id']

    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if user is None:
        return jsonify({'message':'User not found'}), 404
    
    if planet is None:
        return jsonify({'message': 'Planet not found'}), 404
    
    new_favorite_planet = Favorite(
        planet_id=planet_id,
        user_id=user_id
    )

    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify({'message':'Favorite planet added successfully'}), 201

#[POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id

app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'message':'user_id is required'}), 400
    user_id = data['user_id']
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    if user is None:
        return jsonify({'message':'User ot found'}), 404
    if people is None:
        return jsonify({'message': 'People not found'}), 404
    
    new_favorite_people = Favorite(
        people_id=people_id,
        user_id=user_id
    )

    db.session.add(new_favorite_people)
    db.session.commit()

app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_to_delete = Favorite.query.get(planet_id)
    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify({'message': 'Favorite planet deleted successfully'}), 201
    else:
        return jsonify({'message': 'Favorite planet not found'}), 404


app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_to_delete = Favorite.query.get(people_id)
    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify({'message': 'Favorite people deleted successfully'}), 201
    else:
        return jsonify({'message': 'Favorite people not found'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
