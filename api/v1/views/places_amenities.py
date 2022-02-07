#!/usr/bin/python3
"""Places-Amenities view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort
from models.place import Place
from models.amenity import Amenity
import models


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def get_all_amenities_from_place(place_id):
    """Returns all amenity objects related to a place object"""
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    if models.storage_t == "db":
        amenities = place.amenities
    else:
        amenity_ids = [place.amenity_ids] \
            if type(place.amenity_ids) is str else place.amenity_ids
        amenities = [models.storage.get(Amenity, amenity_id)
                     for amenity_id in amenity_ids]
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def create_link_place_amenity(place_id, amenity_id):
    """Stores a link between a an amenity and a place"""
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if models.storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    models.storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_link_place_amenity(place_id, amenity_id):
    """Deletes a link between a place and an amenity and
    returns an empty JSON"""
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if models.storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    models.storage.save()
    return jsonify({}), 200
