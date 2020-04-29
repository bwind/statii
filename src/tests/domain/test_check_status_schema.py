from domain.check_status import CheckStatusSchema


def test_check_status_schema_dump(check_status, check_status_dump):
    dump = CheckStatusSchema().dump(check_status)
    assert dump == check_status_dump


def test_check_status_schema_load(check_status, check_status_dump):
    obj = CheckStatusSchema().load(check_status_dump)
    assert obj == check_status
