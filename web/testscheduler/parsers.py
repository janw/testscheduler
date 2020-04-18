from flask_restful import inputs
from flask_restful import reqparse

from testscheduler.models import TestStatus

STATUS_CHOICES = list(TestStatus.__members__.keys())
ENV_ID_RANGE = (1, 100)

create_parser = reqparse.RequestParser()
create_parser.add_argument(
    "username", required=True, type=str, help="Invalid Username for the test to be run"
)
create_parser.add_argument(
    "env_id", required=True, type=inputs.int_range(*ENV_ID_RANGE), help="{error_msg}",
)
create_parser.add_argument(
    "path", required=True, help="Invalid path of tests to be run"
)

update_parser = reqparse.RequestParser()
update_parser.add_argument("token", required=True, type=str, help="Invalid Auth Token")
update_parser.add_argument(
    "status", required=True, type=str, choices=STATUS_CHOICES, help="Invalid status",
)
update_parser.add_argument("logs", required=False, type=str, help="Invalid logs")
