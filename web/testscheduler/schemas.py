import pygments.formatters
import pygments.lexers
from marshmallow import fields
from marshmallow import Schema
from marshmallow import validate
from marshmallow import ValidationError
from marshmallow_enum import EnumField
from testscheduler.models import TestStatus

STATUS_CHOICES = list(TestStatus.__members__.keys())
ENV_ID_RANGE = (1, 100)


lexer = pygments.lexers.get_lexer_by_name("ansi-color")
formatter = pygments.formatters.HtmlFormatter(linenos=True)


def is_valid_tests_file(data):
    from testscheduler.utils import testfiles

    if data not in testfiles:
        raise ValidationError("Not a valid test file")


class TestRunSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(3))
    created_at = fields.AwareDateTime(dump_only=True)
    env_id = fields.Int(validate=validate.Range(*ENV_ID_RANGE))
    path = fields.Str(validate=is_valid_tests_file)
    status = EnumField(TestStatus, dump_only=True)
    logs = fields.Boolean(truthy=set(), dump_only=True)


class TestRunLogsSchema(Schema):
    logs = fields.Method("serialize_logs", dump_only=True)

    def serialize_logs(self, item):
        if item.logs:
            return pygments.highlight(item.logs, lexer, formatter)
        return ""


class TestRunLogsStatusSchema(Schema):
    status = EnumField(TestStatus)
    logs = fields.Method(load_only=True)
    token = fields.Str(required=True)


testrun_schema = TestRunSchema()
testrun_schema_list = TestRunSchema(many=True)
testrun_logs_status = TestRunLogsStatusSchema()
testrun_logs = TestRunLogsSchema()
