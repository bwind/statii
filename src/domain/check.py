import asyncio
import io
import re
import socket
from dataclasses import dataclass
from typing import List

import aiohttp
import paramiko

from domain.rule import Rule
from domain.status import Status, StatusEnum


@dataclass
class HTTPCheck:
    url: str
    check_status_code: int
    check_response_text: str
    method: str = "GET"
    timeout: int = 0.01

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.url}"

    async def run(self):
        async with aiohttp.ClientSession() as client:
            method = getattr(client, self.method.lower())
            try:
                async with method(self.url, timeout=self.timeout) as response:
                    status_code = response.status
                    response_text = await response.text()
            except asyncio.TimeoutError:
                return Status(
                    StatusEnum.FAILED, message=f"Timeout after {self.timeout}s"
                )
            if (
                self.check_status_code is not None
                and status_code != self.check_status_code
            ):
                return Status(
                    status=StatusEnum.FAILED,
                    message=f"Status code {response.status} is not {self.check_status_code}",  # noqa: E501
                )
            if self.check_response_text is not None:
                pattern = re.compile(self.check_response_text)
                if not re.match(pattern, response_text):
                    response_text_truncated = (
                        f"{response_text[:30]}..."
                        if len(response_text) > 33
                        else response_text
                    )
                    check_response_text_truncated = (
                        f"{self.check_response_text[:30]}..."
                        if len(self.check_response_text) > 33
                        else self.check_response_text
                    )
                    message = f'"{response_text_truncated}" does not match "{check_response_text_truncated}"'  # noqa: E501
                    return Status(status=StatusEnum.FAILED, message=message)
        return Status(status=StatusEnum.OK)


@dataclass
class SSHCheck:
    hostname: str
    username: str
    private_key: str
    description: str
    command: str
    rules: List[Rule]

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
            stderr_text = stderr.read().decode().strip()
        except paramiko.ssh_exception.AuthenticationException:
            return Status(
                status=StatusEnum.FAILED, message="Authorization failed"
            )
        except socket.gaierror as exc:
            return Status(status=StatusEnum.FAILED, message=exc)
        else:
            if self.rules:
                status = None
                for rule in self.rules:
                    if rule.test.test(stdout_text) is False:
                        if status is None or rule.status > status:
                            status = rule.status
                            failed_rule = rule
                if status:
                    message = (
                        f'"{stdout_text}" does not pass "{failed_rule.test}"'
                    )
                    if stderr_text:
                        message += ' "(stderr: "{stderr_text}")'
                    return Status(status=status, message=message)
        finally:
            client.close()
        return Status(status=StatusEnum.OK)
