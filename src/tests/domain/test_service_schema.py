from domain.service import ServiceSchema


def test_service_schema_dump(service, service_dump):
    dump = ServiceSchema().dump(service)
    assert dump == service_dump


def test_service_schema_load(service, service_dump):
    obj = ServiceSchema().load(service_dump)
    assert obj == service
