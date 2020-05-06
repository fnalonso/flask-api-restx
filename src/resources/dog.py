from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from src.models.dog import Dog as DogModel

ns = Namespace('dogs', 'Dogs resources.')


dog_schema = ns.model('Dog', dict(
    id=fields.Integer(readonly=True, description='Dog unique id.'),
    name=fields.String(required=True, description='The dog name.')
))


@ns.route("/")
class Dogs(Resource):

    @ns.doc("list_dogs")
    @ns.marshal_list_with(dog_schema)
    def get(self):
        return [dog.as_dict() for dog in DogModel.get_all()]

    @jwt_required
    @ns.doc("create_dog")
    @ns.expect(dog_schema)
    @ns.marshal_with(dog_schema)
    def post(self):
        dog = DogModel(name=ns.payload.get('name'))
        dog.save()
        return dog.as_dict(), 201


@ns.route("/<int:id>")
@ns.response(404, 'Dog not found.')
@ns.param('id', 'Dog unique id.')
class Dog(Resource):

    @ns.doc('get_dog')
    @ns.marshal_with(dog_schema)
    def get(self, id):
        dog = DogModel.find_by_id(id)
        if not dog:
            ns.abort(404)
        return dog.as_dict()

    @jwt_required
    @ns.doc('delete_dog')
    @ns.response(204, 'Dog removed :)')
    def delete(self, id):
        dog = DogModel.find_by_id(id)
        if dog:
            dog.delete()
        return '', 204

    @jwt_required
    @ns.doc("update_dog")
    @ns.marshal_with(dog_schema)
    def put(self, id):
        dog = DogModel.find_by_id(id)
        if not dog:
            ns.abort(404)
        dog.name = ns.payload.get('name')
        dog.save()
        return dog.as_dict()
