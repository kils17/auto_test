""" Module containing the Telnet Connection object.
This object is used to connect to devices in order to run various commands.
"""
import telnetlib
import logging
import os
import re
import subprocess
import time
import traceback
import eng_mibu_exceptions as eme
import comm_utils as comm_utils


logger = logging.getLogger(__name__)


class TelnetController(telnetlib.Telnet):
    """ Telnet base class

    Connect to remote host with TELNET and issue commands.

    """

    def __init__(self, host, user_name, password, prompt, **options):
        """
        Init Method for class

        :param str host: Hostname
        :param str user_name: User Name of the user being logged into the device
        :param str password: Login Password of the User
        :param str|list prompt: Prompt String of the Host
        :param dict **options: Options.  Currently the method doesnt use any

        :return: object: The Mitg Telnet Object

        *Example*

        >>> connection = TelnetController("mitg.cisco.com", "LedZepellin", "stairway", "Promp#")
        >>> connection.login(40)

        """
        self.host_name = host
        self.user_name = user_name
        self.password = password
        self.prompt = prompt
        self.options = options
        self.esc_prompt = None
        self.state = "Idle"
        self.logged_in = False
        self.protocol = "telnet"
        self.in_read_retry = False

        super().__init__(host=None)

    def __repr__(self):
        return "Telnet Connection to Host {0} state {1}".format(self.host_name, self.state)

    @staticmethod
    def __clean_output(command, prompt_list, response, strip_command=True):
        """
        Method will Remove/Strip the response EXCEPT the actual command output

        :param str command: The Command String that was run
        :param str response: Output from the Command
        :param bool strip_command: whether command should be stripped

        :return: The stripped output from the command
        :rtype: str

        .. note:: This method is hidden.  The method returns a modified string output
        from the command to the caller.

        """
        # remove command from response, WARNING: it might be spread over multiple lines
        if strip_command:
            response = comm_utils.strip_output(command, response)

        # remove prompt at the end of response,
        # build string from prompt_list first
        prompt_str = '|'.join(prompt_list)
        response = re.sub(r'.*?' + prompt_str + r'.*?$', '', response, re.S)
        return response

    def is_connected(self):
        """
        Return True if state == connected.
        :return: bool: return true if state == connected

        """
        return self.state == 'Connected'

    def login(self, timeout=30):
        """
        Function that will login into the specified host. The Object will contain the
        information needed to telnet to the specific chassis. First the function will
        Ping the destination to insure it is up and running.  This method will use the login
        username and password provided at the creation of the connection object.  The
        method will also set the prompt string.

        :param int timeout: Timeout value.  If one is not provided the method uses a default of 30 seconds

        :return: None
        :raises eme.EngProcCmd:
        :raises eme.EngTelnetCredentialsError: Login failure

        **Example  This example shows the user using a 40 second timeout to log in**

        >>> connection = TelnetController("mitg.cisco.com","LedZepelin","stairway","Prompt#")
        >>> connection.login(40)

        .. note:: Prior to running any comands the user should call this method to log into the device

        """

        self.in_read_retry = False

        if not self.state == "Idle":
            raise eme.EngTelnetError("Connection not in Idle state, state is {0}".format(self.state))

        try:
            out = subprocess.check_output(['ping', '-c3', self.host_name], universal_newlines=True)
            logger.debug(out)
        except subprocess.CalledProcessError as err:
            logger.warning("Failed to ping [{0}] return code {1}".format(self.host_name, err.returncode))
            raise eme.EngPingError(ping_address=self.host_name)
        except Exception as err:
            logger.warning("Failed to ping [{0}] Exception [{1}]".format(self.host_name, err))
            raise eme.EngTelnetError("Failed to ping [{0}] Exception [{1}]".format(self.host_name, err))

        try:
            self.open(self.host_name, timeout=30)
        except:
            logger.warning("Failed to open connection to [{0}]".format(self.host_name))
            raise eme.EngTelnetError("Failed to open connection to [{0}]".format(self.host_name))

        self.state = "Connected"

        try:
            # Attempt to log into the chassis using username and password
            # Wait for login prompt
            self.run_command(None, 'login:')
            self.run_command(self.user_name, 'assword:')
            self.set_prompt(self.prompt)
            # Echo the password
            # Do not attempt to reconnect if we fail on logging into the box on
            # the first attempt
            response = self.run_command(self.password, timeout=timeout)
            if "Login incorrect" in response:
                self.logout()
                raise eme.EngTelnetCredentialsError(login=self.user_name, password=self.password)
        except Exception as err:
            self.logout()
            logger.warning("Failed to login to [{0}] Exception [{1}]".format(self.host_name, err))
            raise eme.EngTelnetCredentialsError(login=self.user_name, password=self.password)

        self.logged_in = True
        # Print out the connection info.  Set the prompt string to the Boxer prompt.
        logger.debug("host {0} : {1}".format(self.host_name, self.prompt))

    def logout(self):
        """
        Method logout: it closes the connection adn reset the state

        **Example**

        """
        if not self.state == "Connected":
            logger.warning("Connection not in Connected state {0}, closing...".format(self.state))
        self.close()
        self.logged_in = False
        self.state = "Idle"

    def reconnect(self, attempts=240, sleep_time=5, timeout=30):
        """
        Closes connection if still there and attempts to reconnect.  This method logs any
        exception that occurred in the logout() call

        :param int attempts: number of attempts
        :param int sleep_time: time to sleep before attempts
        :param int timeout: Timeout valus passed into the login() method when reconnecting
        :return: None

        **Example**

        >>> import libs.comms.mitg_telnet
        >>> connection = libs.comms.mitg_telnet.TelnetController("mitg.cisco.com","LedZepelin","stairway","Prompt#")
        >>> connection.reconnect()

        """
        logger.debug("Attempting to reconnect...")
        # prompt mode should not be in Telnet Module???
        # self.prompt_mode = "normal"
        self.set_prompt(self.prompt)

        if self.state != "Idle":
            # If the state is not idle, then we need to logout
            try:
                self.logout()
            except Exception as err:
                logger.warning("An error occurred when closing connection {0}, proceeding...".format(err))
                raise eme.EngTelnetError("An error occurred when closing connection {0}, proceeding...".format(err))

        success = False
        for attempt in range(0, attempts):
            try:
                self.login(timeout=timeout)
                success = True
                break
            except eme.EngMibuException as err:
                logger.debug("{0}, re-trying ({1}) ...".format(err, attempt + 1))
            if attempt < attempts - 1:
                time.sleep(sleep_time)
        if not success:
            raise eme.EngTelnetError("Unable to re-connect after {0} attempts".format(attempts))

    def send_cmd(self, command, prompt_msg, timeout=10):
        """
        Send the command.
        :param str command: Command to run.
        :param str prompt_msg: String containing expected prompt
        :param int timeout: Timeout in seconds to wait for the command to complete. Default is 10.

        :raises eme.EngTelnetError: Failure to run the command.
        :raises eme.EngTelnetError: Provided Prompt string is not valid type.

        """
        # Write the command
        try:
            logger.debug("RC: CMD:{0} TO:{1} Prompt {2} ".format(command, timeout, prompt_msg))
            cmd = "{0}\n".format(command)
            self.write(cmd.encode())
        except:
            logger.error("Error {0}".format(traceback.format_exc()))
            raise eme.EngTelnetError("{0} Failure running command {1}".format(self.host_name, command))

    def run_command(self, command, prompt_str=None, timeout=10,
                    wait_for_prompt=True, disable_retry=False):
        """
        This method will perform the work of running a command on the host. The
        function will send the command over and wait for the appropriate prompt
        string to be returned. The function will then process and send back the
        output strings returned by the host while running the command.

        See comment in mitg_ssh.py, SshController's class header on empty-response anomally, and the process
        to recover via retrying.


        :param str command: Command to run.
        :param str prompt_str: This is the prompt string to use for the command.
                               If one is not passed in then the method will use the current prompt string.
                               This is used to override the current prompt string
        :param int timeout: Timeout in seconds to wait for the command to complete. Default is 10
        :param bool wait_for_prompt: Default is True, if we need to wait for the prompt
        :param bool disable_retry: If True, run_command will not retry for the empty-response anomally

        :return: Returns the output from the command returned by the Host
        :rtype: str
        :raises eme.EngTelnetError: Failure to run the command.
        :raises eme.EngTelnetError: Provided Prompt string is not valid type.
        :raises eme.EngTelnetError: If Telnet expect call returns and error.
                                    This method will catch these errors and return a run time


        **Example**

        """
        if not self.state == "Connected":
            raise eme.EngTelnetError("Connection not in Connected state, "
                                     "state is: {0}, command: {1}".format(self.state, command))

        prompt_msg = "(passed): {0}".format(prompt_str) if prompt_str else ": {0}".format(self.prompt)
        if command:
            self.send_cmd(command, prompt_msg, timeout)
        else:
            logger.debug("RC: CMD:None")

        if not wait_for_prompt:
            logger.warning("Do not wait for prompt, return after timeout {0}".format(timeout))
            time.sleep(timeout)
            return

        # Set up expected response prompts:
        prompt_list = []
        # If the caller passes a string into the function use that string as the prompt
        if prompt_str is not None:
            # Copy the provided prompt string into a list
            if isinstance(prompt_str, str):
                prompt_list.append(comm_utils.create_esc_prompt(prompt_str))
            elif isinstance(prompt_str, list):
                prompt_list = list(prompt_str)
            else:
                err = "Error: Unknown Prompt String type in CLI command {0} Type {1}".format(command, type(prompt_str))
                logger.error(err)
                raise eme.EngTelnetError(err)
        else:
            if self.esc_prompt:
                if isinstance(self.esc_prompt, str):
                    prompt_list.append(self.esc_prompt)
                else:
                    prompt_list = self.esc_prompt
            else:
                raise eme.EngTelnetError("Escaped prompt is not defined, no prompt")
        # Convert the prompt(s) to encoded format:
        try:
            logger.debug("run_cmd prompt_list: {0}".format(prompt_list))
            plist = []
            for pmpt in prompt_list:
                plist.append(pmpt.encode())
        except TypeError:
            logger.error("Error {0}".format(traceback.format_exc()))
            raise eme.EngTelnetError("{0}, Failure running command, TypeError".format(self.host_name))


        # Prep in case retry is needed:
        chatty = comm_utils.chatty_command(command)
        retries = 1 if not chatty or disable_retry else 2
        self.in_read_retry = False
        tmo = timeout
        response_preretry = None
        force_retry = False #set True for self-testing only

        for loop in range(retries):

            if loop > 0:
                logger.debug("RETRYING COMMAND {0}".format(command))
                # retry the command, but use a shorter timeout, as this comamnd has already given us (some) response
                self.in_read_retry = True
                tmo = 2

            # Wait for the prompt
            try:
                # FYI, to test retry, force a fake empty-response here. Make sure you change the line:
                #                    response += "[local]swch22"
                # to match the expected prompt.
                if force_retry and command is not None and "show version" in command:
                    #create a fake empty response with the command, newline, and prompt
                    idx = 0
                    match_obj = " "
                    response = command
                    response += os.linesep
                    response += "[local]swch22" #change this to match expected prompt
                    response = response.encode()
                    force_retry = False
                else:
                    # Read (any) response:
                    [idx, match_obj, response] = self.expect(plist, tmo)
            except EOFError:
                # I belive this means the telnet session has closed, vs the non-fatal timeout where no data was read.
                logger.error("Failure running Cmd {0}, Rcvd EOFError".format(command))
                raise eme.EngTelnetError("{0}, Failure running command, EOFError".format(self.host_name))
            except Exception as err:
                logger.error("Error {0}".format(traceback.format_exc()))
                raise eme.EngTelnetError("{0}, Failure running command {1}: {2}".format(self.host_name, command, err))

            if idx == -1:
                # expect() got a timeout
                if loop != 0:
                    # If we're in retry:
                    # - In the first loop, timeouts are valid
                    # - In the second+ loop, the retry (i.e., the repeat call to expect()) itself may result in a
                    #   timeout, even though there wasn't a timeout on the first expect() call.
                    #   In this case, revert to the original response from the first loop. That is, pretend we didn't
                    #   retry.
                    response = response_preretry
                else:
                    # timeout && first loop: no prompt match
                    logger.warning("FAILURE to match prompt(s) {0}: Cmd is {1}".format(prompt_list, command))
                    if not match_obj and response:
                        # If no match, expect() will return (-1, None, data), where 'data' is the bytes received so
                        # far, if any (and data may be empty-string if timeout occured).
                        logger.warning("Buffer not empty: <{0}>".format(response.decode(errors='ignore')))
                    self.logout()
                    raise eme.EngTimeoutError(prompt_list, command, timeout)
            elif loop != 0:
                logger.debug("RETRIED COMMAND SUCCEEDED {0}".format(command))

            if isinstance(response, bytes):
                response = response.decode(errors='ignore')

            logger.debug("RC Cmd:{0} Results:{1}".format(command, response))

            if not command:
                # We don't retry if there was no command, and we don't clean it either.
                return response

            if not self.logged_in or not command:
                # Pre-log-in, the 'responses' don't need to be cleaned up, because they are in response to things
                # like the password, which isn't even echo'ed back.
                # Also, no cmd-retries either, for several reasons, including that password looks like an
                # empty response.
                # And no cleanup nor retry for empty commands either
                break

            response = self.__clean_output(command, prompt_list, response)

            if not chatty or (response is not None and not response.isspace() and response != ""):
                # Either no response is expected, or we got a non-empty response
                break
            response_preretry = response

        self.in_read_retry = False
        return response

    def get_promptlist(self):
        """
        This function will return the prompt list of the telnet session

        :return: prompt list
        :rtype: list

        """
        prompt_list = []
        if isinstance(self.prompt, str):
            prompt_list.append(self.prompt)
        else:
            prompt_list = self.prompt

        return prompt_list

    def set_prompt(self, prompt):
        """
        This function will set the prompt string to the telnet session

        :param str/list prompt: Update the current prompt string for the object
        :return: None

        **Example**

        .. note:: This will change the prompt for the connection.  Commands run after
        this call will use the NEW prompt

        """
        prompt_list = []
        if isinstance(prompt, str):
            prompt_list.append(prompt)
        else:
            prompt_list.extend(prompt)
        self.prompt = prompt_list
        self.esc_prompt = []
        for pmpt in self.prompt:
            self.esc_prompt.append(comm_utils.create_esc_prompt(pmpt))
        logger.debug("Prompt is now {0}  Esc {1}".format(self.prompt, self.esc_prompt))

    def add_prompt(self, prompt):
        """
        This function will add to the existing prompt string to the telnet session

        :param str|list prompt: Extend the current prompt string for the object
        :return: None

        **Example**

        .. note:: This will change the prompt for the connection.  Commands run after
        this call will use the NEW prompt

        """
        if not self.prompt or not self.esc_prompt:
            raise eme.EngOutputError("Prompt or Esc prompt "
                                     "not set: {0}, Esc: {1}".format(self.prompt, self.esc_prompt))
        if not isinstance(self.prompt, list) or not isinstance(self.esc_prompt, list):
            raise eme.EngOutputError("Prompt or Esc prompt "
                                     "not in the right format: {0}, Esc: {1}".format(self.prompt,
                                                                                     self.esc_prompt))
        if isinstance(prompt, str):
            self.prompt.append(prompt)
            self.esc_prompt.append(comm_utils.create_esc_prompt(prompt))
        else:
            for pmpt in prompt:
                self.prompt.append(pmpt)
                self.esc_prompt.append(comm_utils.create_esc_prompt(pmpt))
        logger.debug("Prompt is now {0}  Esc {1}".format(self.prompt, self.esc_prompt))

    def execute_command(self, command, prompt_str=None, timeout=120, check_errors=True):
        """
        Runs a command, reconnect if necessary and optionally checks for errors
        this command wraps around run_command coming from the lower level libraries

        :param str command: Command string
        :param str prompt_str: Prompt string to be used for this command.  Overrides the one to the connection
        :param int timeout: Timeout to wait for the command to comlete
        :param bool check_errors: Check for errors

        :return: Command output
        :rtype: str
        :raises eme.EngTelnetError: If connection is not in the connected state
        :raises eme.EngTelnetError: Failure running the command
        :raises eme.EngOutputError: If the result/ouput was not clean (invalid cmd, etc)

        **Example**

        """
        if not self.state == "Connected":
            raise eme.EngTelnetError("Connection not in Connected state, "
                                     "state is: {0}, command: {1}".format(self.state, command))
        try:
            res = self.run_command(command, prompt_str=prompt_str, timeout=timeout)
        except eme.EngMibuException as err:
            raise eme.EngTelnetError("Error when running command {0}".format(err))

        # This will generate an EngOutputError exception if there's an error
        comm_utils.check_output_for_errors(command, cmd_output=res, check_errors=check_errors)

        return res
