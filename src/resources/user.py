from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_refresh_token, create_access_token

from flask_restx import Resource, Namespace, fields

from src.models.user import UserModel


ns = Namespace("users", description="Users resource.")

user_schema = ns.model("User", dict(
    id=fields.Integer(readonly=True, description="User unique id."),
    username=fields.String(required=True, description="User name."),
    password=fields.String(required=True, description="User password.")
))


@ns.route("/")
class Users(Resource):

    @ns.doc("list_users")
    @ns.marshal_list_with(user_schema, skip_none=True)
    def get(self):
        return [user.as_dict() for user in UserModel.get_all()]

    @ns.doc("create_user")
    @ns.expect(user_schema)
    @ns.marshal_with(user_schema, skip_none=True)
    def post(self):
        user = UserModel(
            username=ns.payload.get('username'),
            password=ns.payload.get('password')
        )
        user.save()
        return user.as_dict(), 201


@ns.route("/<int:id>")
@ns.response(404, 'User not found.')
class User(Resource):
    @ns.doc("get_user")
    @ns.marshal_with(user_schema, skip_none=True)
    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            ns.abort(404)
        return user.as_dict()

    @ns.doc("delele_user")
    @ns.response(204, "User removed.")
    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete()
        return '', 204


token_schema = ns.model('Token', dict(
    access_token=fields.String(description="Access token for protected endpoints"),
    refresh_token=fields.String(description="Refresh access token")
))


@ns.route("/login")
class Login(Resource):
    @ns.doc("post_user_login")
    @ns.expect(user_schema)
    @ns.response(404, "User not found.")
    @ns.response(403, "Authentication failed.")
    @ns.marshal_with(token_schema)
    def post(self):
        user = UserModel.find_by_username(ns.payload.get('username'))
        if not user:
            ns.abort(404)

        if safe_str_cmp(user.password, ns.payload.get('password')):
            return dict(
                access_token=create_access_token(user.id),
                refresh_token=create_refresh_token(user.id)
            )
        else:
            ns.abort(403)
