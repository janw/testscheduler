from flask_restful import fields


class TestStatusMarshaller(fields.Raw):
    def format(self, value):
        _, status = str(value).split(".")
        return status


testrun_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "created_at": fields.DateTime(dt_format="iso8601"),
    "env_id": fields.Integer,
    "path": fields.String,
    "status": TestStatusMarshaller,
    "logs": fields.Boolean,
}
