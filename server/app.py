from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Campers(Resource):
    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]
        return make_response(jsonify(campers),200)
api.add_resource(Campers, '/campers')

class CamperByID(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(camper), 200)
api.add_resource(CamperByID, '/campers/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
