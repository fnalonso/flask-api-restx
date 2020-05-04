from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from models.cat import Cat as CatModel


ns = Namespace('cats', 'Cats resources.')


cat_schema = ns.model('Cat', dict(
    id=fields.Integer(readonly=True, description='Cat unique id.'),
    name=fields.String(required=True, description='The cat name.')
))


@ns.route("/")
class Cats(Resource):

    @ns.doc("list_cats")
    @ns.marshal_list_with(cat_schema)
    def get(self):
        """
        List all cats
        """
        return [cat.as_dict() for cat in CatModel.get_all()]

    @jwt_required
    @ns.doc('create_cat', security='bearerAuth')
    @ns.expect(cat_schema)
    @ns.marshal_with(cat_schema, code=201)
    def post(self):
        cat = CatModel(name=ns.payload.get('name'))
        cat.save()
        return cat.as_dict(), 201


@ns.route("/<id>")
@ns.response(404, 'Cat not found.')
@ns.param('id', 'Cat id.')
class Cat(Resource):
    """
    Return a single cat.
    """
    @ns.doc('get_cat')
    @ns.marshal_with(cat_schema, skip_none=True)
    def get(self, id):
        """Fetch the cat."""
        cat = CatModel.find_by_id(id)
        if not cat:
            return None, 404
        return cat.as_dict()

    @jwt_required
    @ns.doc('remove_cat', security='bearerAuth')
    @ns.response(204, 'Cat removed.')
    def delete(self, id):
        """Remove a cat"""
        cat = CatModel.find_by_id(id)
        if cat:
            cat.delete()
        return '', 204

    @jwt_required
    @ns.doc('update_cat', security='bearerAuth')
    @ns.expect(cat_schema)
    @ns.marshal_with(cat_schema)
    def put(self, id):
        """Update a cat"""
        cat = CatModel.find_by_id(id)
        if not cat:
            ns.abort(404)
        cat.name = ns.payload.get('name')
        cat.save()
        return cat.as_dict()
