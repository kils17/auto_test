""" Module containing all the various Mitg BU exception classes.
"""

# pylint: disable=locally-disabled,super-init-not-called

class EngMibuRuntimeException(Exception):
    """
    Mibu Exception
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class EngMibuException(Exception):
    """
    Mibu Exception
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class EngNetworkError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class EngCallModelToolLIError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class EngConnectionError(EngNetworkError):
    """
    Mibu Exception
    """
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.msg = "Connection is not open, connection id: {0}".format(self.conn_id)

    def __str__(self):
        return self.msg


class EngPingError(EngNetworkError):
    """
    Mibu Exception
    """
    def __init__(self, ping_address):
        self.ping_address = ping_address
        self.msg = "Failed to ping {0}\n" \
                   "Confirm host configuration & physical connections".format(self.ping_address)

    def __str__(self):
        return self.msg


class EngTelnetError(EngNetworkError):
    """
    Mibu Exception
    """
    def __init__(self, host_address):
        self.host_address = host_address
        self.msg = "Telnet to {0} unsuccessful\n" \
                   "Confirm host online with correct address".format(self.host_address)

    def __str__(self):
        return self.msg


class EngTelnetCredentialsError(EngNetworkError):
    """
    Mibu Exception
    """
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.msg = "Failed telnet login with login {0} and password {1}\n" \
                   "Confirm login & password".format(self.login, self.password)

    def __str__(self):
        return self.msg

class EngSshCredentialsError(EngNetworkError):
    """
    Mibu Exception
    """
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.msg = "Failed ssh login with login {0} and password {1}\n" \
                   "Confirm login & password".format(self.login, self.password)

    def __str__(self):
        return self.msg


class EngTimeoutError(EngNetworkError):
    """
    Mibu Exception
    """
    def __init__(self, prompt_string, command, timeout):
        self.msg = "Timeout Waiting for prompt:{0} " \
                   "running cmd:{1} with timeout {2}".format(prompt_string, command, timeout)

    def __str__(self):
        return self.msg


class EngOutputError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Failed to get output {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngProcCmd(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Failed to process Cmd Output {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngHealthCheckError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Health check error {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngFatalError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Fatal error {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngMissingCards(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Error, missing cards, {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngPostRestart(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Error, missing cards required restart, {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngAbortError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Abort error {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg

class EngNotImplementedError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Not implemented error {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg

class EngBulkstatsFileNotFound(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Bulkstats file not found on server {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg

class EngBulkstatsError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Bulkstats error {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg

class EngBFDProtocolError(EngMibuException):
    """
    Defines BFDProtocolError. Can be used to selectively treat BFD health check
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "BFD error {0}".format(self.expect_phrase)

class EngSnmpError(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Snmp error {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngUnexpectedResult(EngMibuException):
    """
    Mibu Exception
    """
    def __init__(self, result):
        self.result = result
        self.msg = "Unexpected result: {0}".format(self.result)

    def __str__(self):
        return self.msg


class EngRedundancyError(EngMibuException):
    """
    Mibu Redundancy Exception
    """
    def __init__(self, result):
        self.result = result
        self.msg = "Redundancy error: {0}".format(self.result)

    def __str__(self):
        return self.msg


class EngAlarmError(EngMibuException):
    """
    Mibu Alarm Exception
    """
    def __init__(self, result):
        self.result = result
        self.msg = "Alarm error: {0}".format(self.result)

    def __str__(self):
        return self.msg


class EngLicenseError(EngMibuException):
    """
    MIBU License Error
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "License error: {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg


class EngMemoryError(EngMibuException):
    """
    Mibu Memroy Exception
    """
    def __init__(self, result):
        self.result = result
        self.msg = "Card Memory error: {0}".format(self.result)

    def __str__(self):
        return self.msg


class EngVirshError(EngMibuException):
    """
    Mibu Virsh Exception
    """
    def __init__(self, result):
        self.result = result
        self.msg = "Virsh Error: {0}".format(self.result)

    def __str__(self):
        return self.msg


class EngArgumentValueError(EngMibuException):
    """
    Mibu Exception.
    This exception can be used when a method fails to verify the arguments.
    """
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase
        self.msg = "Invalid argument or value: {0}".format(self.expect_phrase)

    def __str__(self):
        return self.msg
