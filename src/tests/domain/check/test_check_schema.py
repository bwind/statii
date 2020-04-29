from domain.check.check import CheckSchema


def test_ssh_check_schema_dump(ssh_check, ssh_check_dump):
    dump = CheckSchema().dump(ssh_check)
    # Private key is always different
    private_key = dump.pop("private_key")
    ssh_check_dump.pop("private_key")
    assert list(private_key.keys()) == ["ciphertext", "tag", "nonce"]
    assert dump == ssh_check_dump


def test_ssh_check_schema_load(ssh_check, ssh_check_dump):
    assert CheckSchema().load(ssh_check_dump) == ssh_check
