import io
import socket
from dataclasses import dataclass
from typing import List

import paramiko
from marshmallow import fields, post_load

from domain import EncryptedStringField
from domain.check.base import BaseCheck, BaseCheckSchema, CheckFailedError
from domain.rule import Rule, RuleSchema
from domain.status import Status, StatusEnum


@dataclass
class BaseSshCheck:
    hostname: str
    username: str
    private_key: str
    command: str
    stdout_rules: List[Rule]

    def __repr__(self):
        return (
            f"{self.__class__.__name__}: {self.hostname} ({self.description})"
        )

    async def run(self):
        private_key = paramiko.RSAKey.from_private_key(
            io.StringIO(self.private_key)
        )
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=private_key,
            )
            stdin, stdout, stderr = client.exec_command(self.command)
            stdout_text = stdout.read().decode().strip()
        except paramiko.ssh_exception.AuthenticationException:
            return Status(
                status=StatusEnum.FAILED, message="Authorization failed"
            )
        except socket.gaierror as exc:
            return Status(status=StatusEnum.FAILED, message=exc)
        else:
            try:
                self._run_rules(self.stdout_rules, stdout_text)
            except CheckFailedError as exc:
                return exc.status
        finally:
            client.close()
        return Status(status=StatusEnum.OK)


@dataclass
class SshCheck(BaseCheck, BaseSshCheck):
    pass


class SshCheckSchema(BaseCheckSchema):
    hostname = fields.Str()
    username = fields.Str()
    private_key = EncryptedStringField()
    command = fields.Str()
    stdout_rules = fields.Nested(RuleSchema, many=True)

    @post_load
    def make_object(self, data, **kwargs):
        return SshCheck(**data)
