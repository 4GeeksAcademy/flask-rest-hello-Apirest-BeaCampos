from flask import Blueprint, jsonify
from models import db, User, People, Planet, Favorite
from utils import APIException

api = Blueprint('api', __name__)

CURRENT_USER_ID = 1



@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = [u.serialize() for u in users]

    return jsonify({
        "count": len(data),
        "results": data
    }), 200



@api.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    data = [p.serialize() for p in people]

    return jsonify({
        "count": len(data),
        "results": data
    }), 200


@api.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = db.session.get(People, people_id)

    if not person:
        raise APIException("Character not found", 404)

    return jsonify({
        "result": person.serialize()
    }), 200



@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    data = [p.serialize() for p in planets]

    return jsonify({
        "count": len(data),
        "results": data
    }), 200


@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = db.session.get(Planet, planet_id)

    if not planet:
        raise APIException("Planet not found", 404)

    return jsonify({
        "result": planet.serialize()
    }), 200



@api.route('/users/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.filter_by(user_id=CURRENT_USER_ID).all()
    data = [f.serialize() for f in favorites]

    return jsonify({
        "count": len(data),
        "results": data
    }), 200



@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planet = db.session.get(Planet, planet_id)

    if not planet:
        raise APIException("Planet not found", 404)

    existing = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    ).first()

    if existing:
        raise APIException("Planet already in favorites", 400)

    favorite = Favorite(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Planet added to favorites",
        "result": favorite.serialize()
    }), 201


@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    person = db.session.get(People, people_id)

    if not person:
        raise APIException("Character not found", 404)

    existing = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    ).first()

    if existing:
        raise APIException("Character already in favorites", 400)

    favorite = Favorite(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Character added to favorites",
        "result": favorite.serialize()
    }), 201



@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    ).first()

    if not favorite:
        raise APIException("Favorite planet not found", 404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Planet removed from favorites"
    }), 200


@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    ).first()

    if not favorite:
        raise APIException("Favorite character not found", 404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Character removed from favorites"
    }), 200