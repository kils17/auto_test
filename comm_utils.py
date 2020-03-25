""" Module containing Comms Utility Support
"""
import logging
import re
import eng_mibu_exceptions as eme


logger = logging.getLogger(__name__)


def chatty_command(command):
    """
    Return true if the specified command contains any of the chatty command substrings, that is, if command will
    result in any output from the system. For example, 'show' commands apply here, while 'exit' and 'conf' do not.
    Chatty_commands will be retried if they get no response on the first attempt.
    :param string command: the command to check
    return bool: return True if the command contains any of the specified chatty command substrings
    """
    chatty_cmds = ["show"]
    return any(substr in command for substr in chatty_cmds) if command else False


def create_esc_prompt(prompt_str):
    """
    This function will take a string and return a string with the required
    characters escaped to be used for prompt matching on the connection.

    :param str prompt_str: prompt string

    :return: Prompt string with characters escaped
    :rtype: str

    """
    return prompt_str.\
        replace('[', r'\[').\
        replace(']', r'\]').\
        replace('#', r'\#').\
        replace('(', r'\(').\
        replace(')', r'\)').\
        replace('/', r'\/').\
        replace('$', r'\$')


def strip_output(command, response):
    """
    This method will remove/strip the first instance of 'command' from the response.

    :param str command: The command string that was run
    :param str response: Output from the command
    :return: The stripped output from the command
    :rtype: str

    """
    # remove command from response, WARNING: it might be spread over multiple lines
    lines = response.splitlines(keepends=True)
    prev_line = ""
    count = 0
    found = False
    for line in lines:
        count += 1
        line = "{0}{1}".format(prev_line, line.strip("\r\n"))
        # search if command is found
        if command in line:
            found = True
            break
        elif count > 4:
            break
        else:
            prev_line = "{0}{1}".format(prev_line, line)
    # rebuild response string
    if not found:
        logger.debug("Command {0} not found in buffer ___{1}___".format(command, response))
        count = 0

    response = "".join(lines[count:])

    return response

def check_output_for_errors(command, cmd_output, check_errors=True):
    """
    Verify that the cmd output does not contain well-known errors.

    :param str command: Command string
    :param str cmd_output: the results of 'command'
    :param bool check_errors: Check for errors
    :raises eme.EngOutputError
    """
    if not check_errors or not cmd_output:
        return

    error_string = ["(ERROR|ERROR_UNRECOVERED|Error|error|404):.*", "RTNETLINK answers:(.*)",
                    "Unknown command -(.*)", r"\% Invalid command at '\^' marker", "Failure: (.*)"]
    # only first two lines are chceked
    lines = cmd_output.splitlines()[0:4]
    for line in lines:
        for err in error_string:
            res_obj = re.search(r'{0}'.format(err), line)
            if res_obj:
                raise eme.EngOutputError("ERROR, cmd {0}, error: {1}".format(command, res_obj.group()))
