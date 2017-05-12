from flask import Blueprint, request, jsonify

dungeon_api = Blueprint("services.dungeon.service", __name__)


@dungeon_api.route("/api/v1/dungeon", methods=['POST'])
def dungeon_controller():
	return jsonify({"message": "hello"})


@dungeon_api.route("/api/v1/dungeon/players/<int:id>", methods=['GET'])
def get_players(id):
	return jsonify({"message": "player #{}".format(id)})


@dungeon_api.route("/api/v1/dungeon/assets/<int:id>", methods=['GET'])
def get_asset(id):
	return jsonify({"message": "asset #{}".format(id)})
