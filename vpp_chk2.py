"""This module can be run as a stand-alone script to moniter some health
and status of a UP. The module leverages a number
of PYATS SW.  The module has an interactive mode that will allow the user to
clear counters etc.  This module is to be run on a UP of a CUPs platform
"""
import re
import sys
import os
import time
import argparse
from datetime import datetime
import logging
import gen_const as gen_const
import safe_vpp as safe_vpp
import operator
import yaml
import connection as comms_connection


import pprint










def parse2_show_histogram_verbose(cmd_out):
    """
    Parse the command output and get dictionary output of cli: 'vppctl "show histogram"'
    Parsed dictionary will look like below:

    `Example`::
    expected_values =
    {(1, 0): {'main-loop-0': [('205.6ns', 7158),
    ('205.6ns', 9),
    ('411.2ns', 672078884),
    ('822.5ns', 798776),
    ('1.6us', 86907)]}}

    :param str cmd_out: output of 'vppctl "show histogram"'
    :return: Dictionary containing parsed output of cli.
    :rtype: dict
    """
    parsed_output = {}
    lines_not_parsed = []
    # Regex to match
    node_name_regex = r'^(\S+)$'
    sample_bucket_value_regex = r'(\d+\.\d+(?:ns|us|ms|s|m|h|d))\s+(\d+)'
    card_cpu_regex = r'Card (?P<card>\d+), CPU (?P<cpu>\d+):'
    sample_bucket_line = r'Bucket\s+Samples'
    date_time_regex = r'\w+\s+\w+\s+\d+\s+[:\d\s]+EDT'
    total_time_regex = r'^Tot dT,V\s+(\d+\.\d+(?:cl|ns|us|ms|s|m|h|d))\s+(\d+)'
    total_time2_regex = r'^Total dT\s+(\d+\.\d+(?:cl|ns|us|ms|s|m|h|d))'
    minmax_dT_regex = r'(Min|Max) dT\s+(\d+\.\d+(?:cl|ns|us|ms|s|m|h|d))'
    minmax_vec_regex = r'(Min|Max) V\s+(\d+)'
    skip_lines = [date_time_regex, sample_bucket_line, r'-{3,}']

    fptr = open('/tmp/cli_hist','w')
    fptr.write('DJP {0}'.format(cmd_out))
    fptr.close()
        

    # Initialize variable
    node_name = None
    card = cpu = None
    sample_date_list = []
    for line in cmd_out.splitlines():
        line = line.strip()

        # Skip empty line
        if not line:
            continue

        # Skip below lines:
        # i. date_time_regex : 'Monday July 08 04:25:33 EDT 2019'
        # ii. sample_bucket_line: 'Bucket           Samples'
        # iii. '---------------'
        if any(re.search(pattern, line) for pattern in skip_lines):
            continue

        # Check if line matches with 'Card 4, CPU 0: show histogram'
        card_match = re.search(card_cpu_regex, line)
        if card_match:
            # Get card and cpu value. Create entry in parsed_output
            card, cpu = int(card_match.group('card')), int(card_match.group('cpu'))
            parsed_output[(card, cpu)] = {}
            continue

        # Check if line matches with node_name. eg. 'main-loop-0'
        node_name_match = re.search(node_name_regex, line)
        if node_name_match:

            # Check if card & cpu values are determined
            if not card:
                # Assign card, cpu value provided from verify_cli params
                # verify_cli is called for cups without card and cpu info
                card, cpu = 1, 0

                # Create the card/cpu dictionary
                parsed_output[(card,cpu)] = {}

            # Deterine the Thread ID
            thread_match = re.search(r'\S+-(\d+)',line)
            if thread_match:
                thread_id = int(thread_match.group(1))

            # Check if thread ID is in dictionary
            if thread_id not in parsed_output[(card, cpu)]:
                parsed_output[(card, cpu)][thread_id] = {}
            parsed_output[(card, cpu)][thread_id][node_name_match.group(1)] = {}
            cur_node_dict = parsed_output[(card, cpu)][thread_id][node_name_match.group(1)]

            continue

        # The check for total time/vec  min/max values are checked before
        # the bucket line.  The bucket check was passing on some of the
        # max, min/max values

        # Check if the line has the total values/vector
        total_time_match = re.search(total_time_regex, line)
        if total_time_match:
            cur_node_dict['Total_dT'] = total_time_match.group(1)
            cur_node_dict['Total_vec'] = int(total_time_match.group(2))
            continue

        # Check if the line has the total time
        total_time_match = re.search(total_time2_regex, line)
        if total_time_match:
            cur_node_dict['Total_dT'] = total_time_match.group(1)
            continue

        # Check if the line has min/max dT
        minmax_dT_match = re.search(minmax_dT_regex, line)
        if minmax_dT_match:
            if minmax_dT_match.group(1) == 'Min':
                cur_node_dict['min_dt'] = minmax_dT_match.group(2)
            else:
                cur_node_dict['max_dt'] = minmax_dT_match.group(2)
            continue

        # Check if the line has min/max vectors
        minmax_vec_match = re.search(minmax_vec_regex, line)
        if minmax_vec_match:
            if minmax_vec_match.group(1) == 'Min':
                cur_node_dict['min_vec'] = minmax_vec_match.group(2)
            else:
                cur_node_dict['max_vec'] = minmax_vec_match.group(2)
            continue

        # Check if line matches with sample date. eg. '<205.6ns            7158'
        sample_data_match = re.search(sample_bucket_value_regex, line)
        if sample_data_match:
            # Get sample data and append to sample_date_list
            bucket_data, sample_value = sample_data_match.group(1), int(sample_data_match.group(2))

            # Check if the line has a greater than or lesser than character and add
            # it to the bucket data
            if line[0] == '>' or line[0] == '<':
                bucket_data = line[0] + bucket_data

            # Add the bucket key to the dict, if not present
            if 'bucket' not in cur_node_dict:
                cur_node_dict['bucket'] = list()
            cur_node_dict['bucket'].append((bucket_data, sample_value))
            continue

        # Line does not match with any pattern. Add to lines_not_parsed
        lines_not_parsed.append(line)

    logger.debug("Parsed output for CLI output is->\n{0}".format(pprint.pformat(parsed_output)))
    if lines_not_parsed:
        logger.warning("Some lines haven't matched while parsing please check."\
                           "lines didn't parsed are ->\n{0}".format(lines_not_parsed))

    return parsed_output


def get_per_cpu_facility_instances(cpu_dict, facility, card_state="Active"):
    """Returns a list of instances for a given facility

    :param cpu_dict: Dictionary of CPUs to roll through
    :param str facility: Task facility
    :param card_state: State of card.
    :return: list of instances
    :rtype: list
    """

    instance_list = []
    for cpu in cpu_dict:
        # duplicated code:
        facility_dict = cpu_dict[cpu]
        for resource_facility in facility_dict:
            if resource_facility == facility:
                for task_instance in facility_dict[facility]:
                    # Check for state of instance so that we don't return Standby Sessmgrs
                    instance_state = facility_dict[facility][task_instance]['state']
                    if card_state == 'Active':
                        if instance_state != 'S':
                            instance_list.append(task_instance)
                    else:
                        instance_list.append(task_instance)

    return instance_list


def __get_per_cpu_facility_instances(cpu_dict, facility, card_state="Active"):
    """Returns a list of instances for a given facility

    :param cpu_dict: Dictionary of CPUs to roll through
    :param str facility: Task facility
    :param card_state: State of card.
    :return: list of instances
    :rtype: list
    """

    instance_list = []
    for cpu in cpu_dict:
        # duplicated code:
        facility_dict = cpu_dict[cpu]
        for resource_facility in facility_dict:
            if resource_facility == facility:
                for task_instance in facility_dict[facility]:
                    # Check for state of instance so that we don't return Standby Sessmgrs
                    instance_state = facility_dict[facility][task_instance]['state']
                    if card_state == 'Active':
                        if instance_state != 'S':
                            instance_list.append(task_instance)
                    else:
                        instance_list.append(task_instance)

    return instance_list


def parse_show_histogram_verbose(cmd_out):
    """
    Parse the command output and get dictionary output of cli: 'vppctl "show histogram"'
    Parsed dictionary will look like below:

    `Example`::
    expected_values =
    {(1, 0): {'main-loop-0': [('205.6ns', 7158),
    ('205.6ns', 9),
    ('411.2ns', 672078884),
    ('822.5ns', 798776),
    ('1.6us', 86907)]}}
    
    :param str cmd_out: output of 'vppctl "show histogram"'
    :return: Dictionary containing parsed output of cli.
    :rtype: dict
    """
    parsed_output = {}
    lines_not_parsed = []
    # Regex to match
    node_name_regex = r'^(\S+)$'
    sample_bucket_value_regex = r'(\d+\.\d+(?:ns|us|ms|s|m|h|d))\s+(\d+)'
    card_cpu_regex = r'Card (?P<card>\d+), CPU (?P<cpu>\d+):'
    sample_bucket_line = r'Bucket\s+Samples'
    date_time_regex = r'\w+\s+\w+\s+\d+\s+[:\d\s]+EDT'
    total_time_regex = r'^Tot dT,V\s+(\d+\.\d+(?:cl|ns|us|ms|s|m|h|d))\s+(\d+)'
    total_time2_regex = r'^Total dT\s+(\d+\.\d+(?:cl|ns|us|ms|s|m|h|d))'
    minmax_dT_regex = r'(Min|Max) dT\s+(\d+\.\d+(?:cl|ns|us|ms|s|m|h|d))'
    minmax_vec_regex = r'(Min|Max) V\s+(\d+)'
    skip_lines = [date_time_regex, sample_bucket_line, r'-{3,}']

    fptr = open('/tmp/cli_hist','w')
    fptr.write('DJP {0}'.format(cmd_out))
    fptr.close()
        

    # Initialize variable
    node_name = None
    card = cpu = None
    sample_date_list = []
    for line in cmd_out.splitlines():
        line = line.strip()

        # Skip empty line
        if not line:
            continue

        # Skip below lines:
        # i. date_time_regex : 'Monday July 08 04:25:33 EDT 2019'
        # ii. sample_bucket_line: 'Bucket           Samples'
        # iii. '---------------'
        if any(re.search(pattern, line) for pattern in skip_lines):
            continue

        # Check if line matches with 'Card 4, CPU 0: show histogram'
        card_match = re.search(card_cpu_regex, line)
        if card_match:
            # Get card and cpu value. Create entry in parsed_output
            card, cpu = int(card_match.group('card')), int(card_match.group('cpu'))
            parsed_output[(card, cpu)] = {}
            continue

        # Check if line matches with node_name. eg. 'main-loop-0'
        node_name_match = re.search(node_name_regex, line)
        if node_name_match:

            # Check if card & cpu values are determined
            if not card:
                card, cpu = 1, 0

                # Create the card/cpu dictionary
                parsed_output[(card,cpu)] = {}

            # Deterine the Thread ID
            thread_match = re.search(r'\S+-(\d+)',line)
            if thread_match:
                thread_id = int(thread_match.group(1))

            # Check if thread ID is in dictionary
            if thread_id not in parsed_output[(card, cpu)]:
                parsed_output[(card, cpu)][thread_id] = {}
            parsed_output[(card, cpu)][thread_id][node_name_match.group(1)] = {}
            cur_node_dict = parsed_output[(card, cpu)][thread_id][node_name_match.group(1)]

            continue

        # The check for total time/vec  min/max values are checked before
        # the bucket line.  The bucket check was passing on some of the
        # max, min/max values

        # Check if the line has the total values/vector
        total_time_match = re.search(total_time_regex, line)
        if total_time_match:
            cur_node_dict['Total_dT'] = total_time_match.group(1)
            cur_node_dict['Total_vec'] = int(total_time_match.group(2))
            continue

        # Check if the line has the total time
        total_time_match = re.search(total_time2_regex, line)
        if total_time_match:
            cur_node_dict['Total_dT'] = total_time_match.group(1)
            continue

        # Check if the line has min/max dT
        minmax_dT_match = re.search(minmax_dT_regex, line)
        if minmax_dT_match:
            if minmax_dT_match.group(1) == 'Min':
                cur_node_dict['min_dt'] = minmax_dT_match.group(2)
            else:
                cur_node_dict['max_dt'] = minmax_dT_match.group(2)
            continue

        # Check if the line has min/max vectors
        minmax_vec_match = re.search(minmax_vec_regex, line)
        if minmax_vec_match:
            if minmax_vec_match.group(1) == 'Min':
                cur_node_dict['min_vec'] = minmax_vec_match.group(2)
            else:
                cur_node_dict['max_vec'] = minmax_vec_match.group(2)
            continue

        # Check if line matches with sample date. eg. '<205.6ns            7158'
        sample_data_match = re.search(sample_bucket_value_regex, line)
        if sample_data_match:
            # Get sample data and append to sample_date_list
            bucket_data, sample_value = sample_data_match.group(1), int(sample_data_match.group(2))

            # Check if the line has a greater than or lesser than character and add
            # it to the bucket data
            if line[0] == '>' or line[0] == '<':
                bucket_data = line[0] + bucket_data

            # Add the bucket key to the dict, if not present
            if 'bucket' not in cur_node_dict:
                cur_node_dict['bucket'] = list()
            cur_node_dict['bucket'].append((bucket_data, sample_value))
            continue

        # Line does not match with any pattern. Add to lines_not_parsed
        lines_not_parsed.append(line)

    logger.debug("Parsed output for CLI output is->\n{0}".format(pprint.pformat(parsed_output)))
    if lines_not_parsed:
        logger.warning("Some lines haven't matched while parsing please check."\
                           "lines didn't parsed are ->\n{0}".format(lines_not_parsed))

    return parsed_output


def parse_show_task_resources(cmd_out):

    """
    Private Method
    :param cmd_out: Command output of 'show task resources'
    :return: Parsed output of CLI  'show task resources'

    Dictionary is multi-level.  1st level is the Card Slot (1-based), 2nd level is CPU number (0-based)
    3rd level is the proclet name, 4th level is the proclet instance value.
    the remaining level is the resource parameters

    {'1': {'0': {'diamproxy': {'53': {'memory_used': '50.42M',
    'status': 'good',
    'state': '-',
    'session_alloc': '--',
    'cputime_alloc': '90%',
    'sessions_used': '--',
    'memory_alloc': '250.0M',
    'files_alloc': '2500',
    'files_used': '721',
    'cputime_used': '0.8%'}}},
    'hwmgr':     {'11': {'memory_used': '10.75M',
    'status': 'good',
    'state': '-',
    'session_alloc': '--',
    'cputime_alloc': '15%',
    'sessions_used': '--',
    'memory_alloc': '15.00M',
    'files_alloc': '500',
    'files_used': '11',
    'cputime_used': '0.1%'}}},
    'sessmgr':   {'590': {'memory_used': '458.5M',
    'status': 'good',
    'state': 'I',
    'session_alloc': '12000',
    'cputime_alloc': '100%',
    'sessions_used': '4450',
    'memory_alloc': '900.0M',
    'files_alloc': '500',
    'files_used': '26',
    'cputime_used': '4.2%'},
    '2': {'1': {'diamproxy': {'51': {'memory_used': '50.42M',
    'status': 'good',
    'state': '-',
    'session_alloc': '--',
    'cputime_alloc': '90%',
    'sessions_used': '--',
    'memory_alloc': '250.0M',
    'files_alloc': '2500',
    'files_used': '529',
    'cputime_used': '0.7%'}}},
    ..................................................................................................
    ..................................................................................................
    ..................................................................................................
    }

    :rtype: dictionary
    
    """

    # Init the returned dictionary
    task_resources = {}

    if cmd_out == "No matching tasks":
        # returning an empty dictionary
        return task_resources

    # Get re strings for all components
    card_re = r'\s?(\d+)/'
    cpu_re = r'(\d)\s+'
    facility_re = r'([\w\.]*)\s+'
    task_instance_re = r'(\d+)\s+'
    cputime_used_re = r'([\d\.\-%]*)\s+'
    cputime_alloc_re = r'([\d\.\-%]*)\s+'
    memory_used_re = r'([\d\-\.KMG]*)\s+'
    memory_alloc_re = r'([\d\-\.KMG]*)\s+'
    files_used_re = r'([\d\-]*)\s+'
    files_alloc_re = r'([\d\-]*)\s+'
    sessions_used_re = r'([\d\-\.km]*)\s+'
    sessions_alloc_re = r'([\-\.\dkm]*)\s'
    state_re = r'([\-SIB]*)\s+'
    status_re = r'([\w]+)'
    # Expected final Regex
    master_re = re.compile('{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}'.format(card_re,
                                                                                   cpu_re,
                                                                                   facility_re,
                                                                                   task_instance_re,
                                                                                   cputime_used_re,
                                                                                   cputime_alloc_re,
                                                                                   memory_used_re,
                                                                                   memory_alloc_re,
                                                                                   files_used_re,
                                                                                   files_alloc_re,
                                                                                   sessions_used_re,
                                                                                   sessions_alloc_re,
                                                                                   state_re,
                                                                                   status_re))

    for line in cmd_out.splitlines():
        if '/' in line:

            # Check if the line has a match.  If no match get the next line of output
            obj = master_re.search(line)
            if not obj:
                continue

            # Get all fields from the output of the show resources command
            card = int(obj.group(1))
            cpu = int(obj.group(2))
            facility = obj.group(3)
            task_instance = int(obj.group(4))
            cputime_used = obj.group(5)
            cputime_alloc = obj.group(6)
            memory_used = obj.group(7)
            memory_alloc = obj.group(8)
            files_used = obj.group(9)
            files_alloc = obj.group(10)
            sessions_used = obj.group(11)
            session_alloc = obj.group(12)
            state = obj.group(13)
            status = obj.group(14)

            # Storing all attributes of an instance in a dict called 'instance_attrib'.
            # We will now build up the final dictionary 'task_resources' from here
            # as there could be multiple entries for same Card,CPU,Facility.
            # e.g.
            #     1/0 sessmgr          8 0.4% 100% 195.6M 900.0M   35  500     0 12000 I   good
            #     1/0 sessmgr         17 0.4% 100% 196.2M 900.0M   35  500     0 12000 I   good
            #     1/0 sessmgr         33 0.4% 100% 196.0M 900.0M   35  500     0 12000 I   good
            #     1/0 aaamgr          51 0.2%  95% 41.65M 250.0M   14  500    --    -- -   good

            instance_attrib = {'cputime_used': cputime_used, 'cputime_alloc': cputime_alloc,
                               'memory_used': memory_used, 'memory_alloc': memory_alloc,
                               'files_used': files_used, 'files_alloc': files_alloc,
                               'sessions_used': sessions_used, 'session_alloc': session_alloc,
                               'state': state, 'status': status}

            # If  task_resources is empty, we add everything. Else we check each component whether its there or not
            # there and accordingly perform dictionary update procedure on our task_resources dictionary.
            if not task_resources:
                task_resources = {
                    card: {
                        cpu: {
                            facility: {
                                task_instance: instance_attrib}}}}
            else:
                if card in task_resources:
                    if cpu in task_resources[card]:
                        facility_dict = task_resources[card][cpu]
                        if facility in facility_dict:
                            if task_instance in facility_dict[facility]:
                                logger.debug('Task instance {0} of facility {1} '
                                             'already exists'.format(task_instance, facility))
                            else:
                                facility_dict[facility].update({task_instance: instance_attrib})
                        else:
                            facility_dict.update({facility: {task_instance: instance_attrib}})
                    else:
                        task_resources[card].update({cpu: {
                                    facility: {task_instance: instance_attrib}}})
                else:
                    task_resources.update({card: {
                                cpu: {facility: {task_instance: instance_attrib}}}})
        else:
            # Get the Total row
            match = re.search(r'Total\s+(\d+)\s+(\d+\.\d+%)\s+(\d+\.\d+[GMK]?)\s+(\d+)\s+(\d+[km]?)', line)
            if match and task_resources:
                # Add the total info to the dict
                task_resources['Total'] = {'num_inst':match.group(1),
                                           'cputime_used':match.group(2),
                                           'memory_used':match.group(3),
                                           'files':match.group(4),
                                           'sessions_used':match.group(5)}

    return task_resources


def _verify_data_type(value):
    """
    Method for verifying whether incoming string is float or int or string.
    Return appropriate data type after converstion.
    After regex pattern match is done field & its value will be in string even though in actual
    CLI output its int or float type. So Checking the type & returning that string in that format.

    :param str value: value extracted after regex pattern match

    :return: Returns either int or float or string as per type match output
    :rtype: int or float or string
    
    """
    converted_val = None
    try:
        # Converting string to int data type. If no valueError exception is generated it means
        # value can be convertible to int so converting it to int & return.
        converted_val = int(value)
    except ValueError:
        try:
            if value.isalnum():
                #values such as '00e5309' were getting converted to float as 0.0.
                #So to fix this, If value is alphanumeric, for ex: callid = '00e53009', return value as string,
                return value
            # Value is not int. Try to convert it float. If valueError exception is generated that means
            # value can't be converted to int & float so return it as string
            converted_val = float(value)
        except ValueError:
            # Return value as string
            converted_val = value
    return converted_val


def parse_mix_alligned_tabular_output(cli_output,
                                      header_fields=None,
                                      label_fields=None,
                                      index=0,
                                      custom_line_pattern=None,
                                      table_terminal_pattern=None,
                                      skip_line=None,
                                      convert_value_format=False):

    r"""
    Method to parse tabular output using regex patterns. By default, it will fetch values from output by considering space as
    separator. However, custom regex patterns can be supplied to this method, which will be applied on CLI output to fetch values.

    This method can be useful for CLI outputs which do not have consistent indentation across all columns,
    for which parse_tabular_show_output method cannot be used.

    The return value will be a tuple of parsed-dict and unmatched-lines-list.

    `Example`::

    show_sample_output ='''
    Name                 State         Calls          Vectors        Suspends         Clocks       Vectors/Call
    VirtualFunctionEthernet0/6/0-o   active                  1               1               0          4.35e3            1.00
    acl-plugin-fa-cleaner-process  event wait                0               0               1          1.60e4            0.00
    cdp-process                     any wait                 0               0               1          9.04e6            0.00
    '''

    from libs.boxer.generic_parser import GenericCliParser
    
    parser_obj = GenericCliParser()
    headers = ["Name", "State", "Calls", "Vectors", "Suspends", "Clocks", "Vectors/Call"]
    labels = ["Name", "State", "Calls", "Vectors", "Suspends", "Clocks", "Vectors/Call"]
    line_pattern = r'([\S]+)\s+([a-z\s]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d\.e]+)\s+([\d\.]+)'

    parsed_output, lines_not_parsed = self.parse_mix_alligned_tabular_output(cli_output=cli_output=show_sample_output,
    header_fields=headers,
    label_fields=labels,
    custom_line_pattern=line_pattern)

    will print ``parsed_output`` ::

    {'VirtualFunctionEthernet0/6/0-o': {'Calls': 1,
    'Clocks': 4350.0,
    'Name': 'VirtualFunctionEthernet0/6/0-o',
    'State': 'active',
    'Suspends': 0,
    'Vectors': 1,
    'Vectors/Call': 1.0},
    'acl-plugin-fa-cleaner-process': {'Calls': 0,
    'Clocks': 16000.0,
    'Name': 'acl-plugin-fa-cleaner-process',
    'State': 'event wait',
    'Suspends': 1,
    'Vectors': 0,
    'Vectors/Call': 0.0},
    'cdp-process': {'Calls': 0,
    'Clocks': 9040000.0,
    'Name': 'cdp-process',
    'State': 'any wait',
    'Suspends': 1,
    'Vectors': 0,
    'Vectors/Call': 0.0}}

    :param str cli_output:
    Actual show command output.

    :param list header_fields:
    List of column headings to parse. Mandatory parameter.

    :param list label_fields:
    If specified, then the return dict will contain these keys
    instead of those specified in `header_fields`. There must be a
    corresponding entry in `label_fields` for each entry in
    `header_fields`.

    :param int index: int or list of int
    Defaults to the first field (0). If more fields are required to
    guarantee uniqueness pass a list of indices in `index` and that
    many dictionaries will be returned keyed by the given field values
    at those indices.

    :param str custom_line_pattern:
    If specified, this is pattern will be used to parse each line in
    output and fetch values from each column. It needs to be ensured
    that given pattern can correctly match column values.
    NOTE: For lines which have non-default format, especially if the
    value in a column can have multiple space-separated words,
    the matching line-pattern should be provided through this
    parameter.

    :param str table_terminal_pattern:
    If specified, this is the pattern to terminate the search for
    results.

    :param str/list skip_line:
    If specified, then any line matching this pattern will be skipped.

    :param bool convert_value_format:
    A flag to convey if the value found in CLI output should be converted
    to appropriate format, or return in str format as found in output.
    Default: False


    :return:
    Parsed results are obtained by applying regex patterns to CLI output.
    Parser identifies different values in output by considering space as
    column separator. If custom regex patterns are supplied to this method,
    the custom pattern will be applied on CLI output to fetch values.

    The parsed dictionary will be nested with primary keys corresponding
    to value in the column specified by `index` parameter, and its child
    dictionary having all values found per line. Each key in child dict
    will be indexed by the corresponding `header_fields` name (or
    `label_fields` name if specified).
    
    Returns a tuple of:
    - dict of parsed output
    - list of lines which could not be parsed

    :rtype: tuple
    """

    #### Perform input validations
    ## header_fields should always be a list
    if not isinstance(header_fields, list):
        raise eme.EngArgumentValueError("`header_fields` is expected to be a list, " +
                                        "received '{0}' -- '{1}'".format(type(header_fields).__name__, header_fields))

    ## if label_fields is provided, it should always be a list, and same length as header_fields
    if label_fields is not None:
        if not isinstance(label_fields, list):
            raise eme.EngArgumentValueError("`label_fields` is expected to be a list, " +
                                            "received '{0}' -- '{1}'".format(type(label_fields).__name__, label_fields))
        if len(header_fields) != len(label_fields):
            raise eme.EngArgumentValueError("Length of `label_fields` and `header_fields` do not match." +
                                            "\n`label_fields`: {0}\n`header_fields`: {1}".format(label_fields, header_fields))

    ## Pre-process value of `index` and store it as a list
    if isinstance(index, int):
        index_list = [index]
    elif isinstance(index, list):
        index_list = index
    else:
        raise eme.EngArgumentValueError(str(index) + " is not an int or list of ints")

    ## Initialize method variables
    parsed_dict = ListDict()
    lines_not_parsed = []
    ## If 'label_fields' is provided, use these labels to form keys of parsed_dict to populate parsed attribute-values.
    ## Else use 'header_fields' to form keys of parsed_dict.
    if label_fields:
        attrib_labels = label_fields
    else:
        attrib_labels = header_fields
    num_of_labels = len(attrib_labels)


    ## NOTE: For line-patterns which do not fit into default pattern, especially if the value in a column can have multiple
    ##       space-separated words, the matching line-pattern should be provided through `custom_line_pattern` parameter.
    ## If custom regex pattern is provided, use it to parse output
    if custom_line_pattern is not None:
        line_pattern = custom_line_pattern
    ## Initialize default regex patterns
    else:
        ## A word pattern will identify words with any character, including special chars, until a space appears.
        word_regex = r'([\S]+)'
        space_regex = r'\s+'
        ## By default, form a line-pattern assuming each column will have a single word (word_regex) as value;
        ##     Eg: VirtualFunctionEthernet0/6/0-o   active           1        1       0     4.35e3     1.00
        ## and the number of words in each line will be equal to number of labels identified in 'attrib_labels'
        ##     Eg: attrib_labels = ['Name', 'State', 'Calls', 'Vectors', 'Suspends', 'Clocks', 'Vectors/Call']
        line_pattern = "".join([word_regex, space_regex] * (num_of_labels - 1))
        line_pattern = "".join([line_pattern, word_regex])


    ## Split entire output by lines
    splitted_data = cli_output.splitlines()

    ## Parse each line using regex pattern and fetch values for each column of tabular output
    for line in splitted_data:
        ## Skip empty lines or timestamps line
        ##   Tuesday March 20 17:02:53 IST 2018
        if not line or re.search(r'^\w+\s+\w+\s+\d+\s+\d+:\d+:\d+\s+[\w\-\_]+\s\d+$|Time elapsed', line):
            continue
        ## Skip parsing the line if it matches with pattern `skip_line`
        if skip_line:
            skip_matched = False
            if isinstance(skip_line, list):
                for skip_regex in skip_line:
                    if re.search(skip_regex, line):
                        skip_matched = True
                        break
            elif isinstance(skip_line, str):
                if re.search(skip_line, line):
                    skip_matched = True
            if skip_matched:
                continue
        ## Stop parsing any further if `table_terminal_pattern` pattern is hit
        if table_terminal_pattern and re.search(table_terminal_pattern, line):
            break

        ## Search 'line_pattern' in each line
        srch_obj = re.search(line_pattern, line)
        if srch_obj:
            ## Fetch all values from found groups as a tuple
            found_values = srch_obj.groups()
            ## Make sure that number of 'found_values' is same as number of 'num_of_labels',
            ##   else this line cannot be populated with incorrectly parsed values.
            if len(found_values) != num_of_labels:
                logger.warning("Expected num of values: {0}, found: {1}. Could not parse line: '{2}'".format(num_of_labels,
                                                                                                             len(found_values),
                                                                                                             line))
                lines_not_parsed.append(line)
                continue

            ## Construct a key-path by appending all values from 'found_values' which are requested by `index` parameter
            path_to_add = []
            for idx in index_list:
                path_to_add.append(found_values[idx].strip())

            ## Process each attrib-value pair and populate 'parsed_dict'
            for attrib, value in zip(attrib_labels, found_values):
                ## Form complete path using 'path_to_add' and label mentioned in 'attrib_labels' corresponding to each value
                attrib_path = tuple(path_to_add) + (attrib, )
                ## Since all values were fetched as string, need to strip them off whitespaces and
                ##   convert them to appropriate data type before populating
                if convert_value_format:
                    value = self._verify_data_type(value.strip())
                else:
                    value = value.strip()
                ## Append each value in 'parsed_dict' at identified 'attrib_path'
                parsed_dict.append((attrib_path, value))

        else:
            ## Record all unmatched lines
            lines_not_parsed.append(line)

    ## Return the entire parsed dict. Reconstruct the ListDict back into regular python dict before returning.
    return parsed_dict.reconstruct(), lines_not_parsed


def get_data_segment(data,
                     start_demarc,
                     end_demarc=None):
    """
    Method used for getting selected data segement from the CLI output.
    Based on start demarcation & end demarcation particular data segemnt will be
    extracted from data chunk.

    `Example`::

            sample_output = '''==CAE-Readdressing:==
                Requests CAE-Readdressed:                                        0
                Responses CAE-Readdressed:                                       0
                Requests having MVG xheader inserted:                            0
                Total CAE-Readdressed Uplink Bytes:                              0
                Total CAE-Readdressed Uplink Packets:                            0
                Total CAE-Readdressed Downlink Bytes:                            0
                Total CAE-Readdressed Downlink Packets:                          0
                Total Charging action hit - Req. Readdr.:                        0
                Total Charging action hit - Resp. Readdr:                        0
                Proxy Disable Success:                                           0
                Flows connected to CAE:                                          0
                  ==CAE Readdressing Error Conditions:==
                Total connect failed to CAE:                                     0
                Req. Readdr. - pipelined case:                                   0
                Skipped Resp. Readdr. - pipelined req:                           0
                Req. Readdr. - Socket Mig. failed:                               0
                Skipped Resp. Readdr. - partial resp hdr:                        0
            '''

           split_op = getDataSegment(sample_output, 'CAE-Readdressing:','CAE Readdressing Error Conditions'')
           print(split_op)

        will print `split_op` `Example` ::

                Requests CAE-Readdressed:                                        0
                Responses CAE-Readdressed:                                       0
                Requests having MVG xheader inserted:                            0
                Total CAE-Readdressed Uplink Bytes:                              0
                Total CAE-Readdressed Uplink Packets:                            0
                Total CAE-Readdressed Downlink Bytes:                            0
                Total CAE-Readdressed Downlink Packets:                          0
                Total Charging action hit - Req. Readdr.:                        0
                Total Charging action hit - Resp. Readdr:                        0
                Proxy Disable Success:                                           0
                Flows connected to CAE:                                          0



        :param str data: CLI output string from which selected data is to be extracted. Mandatory
        :param str start_demarc:
            Start demarcation. Can be string or combination of regex & string.
            From this data segement will be extracted. Mandatory
        :param str end_demarc:
            End demarcation. Till this string lines will be captured from start
            demarcation. If not provided end of data will be considered as end_demarcation

        :return: String which will be having lines/data segement extracted from input data.
        :rtype: string

        """

    # End Demarcation validation
    if not end_demarc:
        logger.debug("End Demarcation not supplied, Assuming end of output")

    output = list()
    start_found = False
    line_count = 0
    position = 0
    final_data = ""
    data = data.splitlines()
    compile_obj_start = re.compile(start_demarc)
    if end_demarc:
        # If end demarcation is present create compile regex object for end demarcation
        compile_obj_end = re.compile(end_demarc)
    for line in data:
        # Check every line with start demarcation regex. If matched set start_found flag true.
        # & set position index to that line.
        # Then search for end demarcation regex if found select lines from position to current
        # line count.
        if start_found:
            if not end_demarc:
                output = data[position:]
                break
            elif compile_obj_end.search(line):
                output = data[position:line_count]
                position = 0
                break
        elif compile_obj_start.search(line):
            position = line_count
            start_found = True
        line_count = line_count + 1
    if not output and start_found:
        output = data[position:]

    # Converting back the list of lines extracted to string format.
    final_data = '\n'.join(output)

    return final_data

def __parse_show_vpp_errors_verbose(self, cmd_out):
    """
    Parse & get dictionary output of cli
    vppctl "show errors verbose"
    sample chassis ouput:
    
    Count                    Node                         Reason        Index
    Thread 0 (vpp_main):
    2986             ip6-icmp-input                 valid packets    1344
    2986             ip6-icmp-input             router advertisement 1360
    2986             ip6-icmp-input             router advertisement 1361
                 1                ip6-input                unknown ip protocol 1541
       Thread 1 (vpp_wk_0):
                 4             ethernet-input                   no error       1197
        Total:
                 4             ethernet-input                   no error         1197
              2986             ip6-icmp-input                 valid packets      1344
              2986             ip6-icmp-input             router advertisement   1360
              2986             ip6-icmp-input             router advertisement   1361
                 1                ip6-input                unknown ip protocol   1541

        Dictionary:
            {'Thread 0': {'ip6-icmp-input': {'router advertisement': {'Count': 2984,
                                                                      'Index': 1361,
                                                                      'Node': 'ip6-icmp-input',
                                                                      'Reason': 'router '
                                                                                'advertisement'},
                                             'valid packets': {'Count': 2984,
                                                               'Index': 1344,
                                                               'Node': 'ip6-icmp-input',
                                                               'Reason': 'valid '
                                                                         'packets'}},
                          'ip6-input': {'unknown ip protocol': {'Count': 1,
                                                                'Index': 1541,
                                                                'Node': 'ip6-input',
                                                                'Reason': 'unknown ip '
                                                                          'protocol'}}},
             'Thread 1': {'ethernet-input': {'no error': {'Count': 4,
                                                          'Index': 1197,
                                                          'Node': 'ethernet-input',
                                                          'Reason': 'no error'}}},
             'Total': {'ethernet-input': {'no error': {'Count': 4,
                                                       'Index': 1197,
                                                       'Node': 'ethernet-input',
                                                       'Reason': 'no error'}},
                       'ip6-icmp-input': {'router advertisement': {'Count': 2984,
                                                                   'Index': 1361,
                                                                   'Node': 'ip6-icmp-input',
                                                                   'Reason': 'router '
                                                                             'advertisement'},
                                          'valid packets': {'Count': 2984,
                                                            'Index': 1344,
                                                            'Node': 'ip6-icmp-input',
                                                            'Reason': 'valid packets'}},
                       'ip6-input': {'unknown ip protocol': {'Count': 1,
                                                             'Index': 1541,
                                                             'Node': 'ip6-input',
                                                             'Reason': 'unknown ip '
                                                                       'protocol'}}}}

        :param str cmd_out: output of 'vppctl "show errors"'
        :return: Dictionary containing parsed output of cli.
        :rtype: dict
        """

    cnt = cmd_out.count("Thread")
    logger.debug("Thread count= {0}".format(cnt))
    headers = ["Count", "Node", "Reason", "Index"]
    labels = ["Count", "Node", "Reason", "Index"]
    line_pattern = r'(\d+)\s+([\S]+)\s+([\w\s\(\)]+)\s+(\d+)'
    parse_dict = {}

    segment_demarcations = []
    for thread in range(cnt):
        segment_demarcations.append("Thread " + str(thread))
    segment_demarcations.extend(["Total", None])

    pprint.pformat(segment_demarcations)

    lines_didnt_matched = []

    for idx in range(len(segment_demarcations) - 1):
        start = segment_demarcations[idx]
        end = segment_demarcations[idx + 1]

        # fetch data-segment using 'start' and 'end' demarcations
        seg = get_data_segment(data=cmd_out, start_demarc=start, end_demarc=end)

        # parse each segment
        skip_line = start
        actual_output, unmatched_lines = \
            self.parse_mix_alligned_tabular_output(seg, skip_line=skip_line,
                                                   header_fields=headers, label_fields=labels,
                                                   custom_line_pattern=line_pattern, index=[1, 2])

        parse_dict[start] = actual_output
        if unmatched_lines:
            lines_didnt_matched.append(unmatched_lines)

    if lines_didnt_matched:
        logger.error("Some lines did not match while parsing, please check: {0}".format(lines_didnt_matched))
    else:
        logger.debug("CLI output is parsed properly")

    logger.debug("Parsed output:\n{0}".format(pprint.pformat(parse_dict)))

    actual_output = parse_dict
    return actual_output







# Create global stream list.  Used to determine Stream operation rates
STREAM_LIST = list()

# pylint: disable=anomalous-backslash-in-string,line-too-long,global-statement

logger = logging.getLogger(__name__)

LAST_CLEAR_INTERFACE = None
LAST_CLEAR_ERR = None

LAST_CLEAR_SAFE_INTERFACE = None
LAST_CLEAR_SAFE_ERR = None
LAST_CLEAR_SAFE_SYS = None
CACHE_PERF_DICT = None
CACHE_ERR_DICT = None
CACHE_IF_DICT = None

UP_KEY_MAPPING = {'HTTP':{'ul_pkts':'Total Uplink Pkts',
                          'dl_pkts':'Total Downlink Pkts',
                          'ul_bytes':'Total Uplink Bytes',
                          'dl_bytes':'Total Downlink Bytes',},
                  'SHTTP':{'ul_pkts':'Total Uplink Pkts',
                           'dl_pkts':'Total Downlink Pkts',
                           'ul_bytes':'Total Uplink Bytes',
                           'dl_bytes':'Total Downlink Bytes',}}

class VppInterogate():
    """
    This class is the VPP Interogate class.  

    :return: None

    """

    def __init__(self):
        '''Class init'''

        self.last_hist_clear_tod = None   # Last TOD that VPP clear histogram cmd was executed
        self.hist_cmd_tod = None   # Time of last show histogram cmd was run

        self.fptr = open('vpp_chk.out','w')
        self.orig_stdout = None
        self.redirect = False
        self.print_fname = None
        self.fopen = None

    def vpp_pkt_path(self, pkt_path):
        """This method will take the output of VPP show run with a select
        nodes (dpdk-input, fastpath-handoff-exec & fastpath-executive) and
        determine the amount of traffic coming into each VPP worker thread,
        what the percentage of incoming traffic is being hashed and handoffed
        & the amount of conduit traffic being processed by each VPP worker thread

        :param str pkt_path: Multi line string of the show run output
        
        :return: Dictionary containing pkt info per VPP worker thread & time window
        :rtype: dict,float
        """

        worker = -1  # Init number of VPP workers
        ret_dict = dict()
        time_found = False
        time_val = 0.0

        # Loop through the multi-line input
        for line in pkt_path.split('\n'):

            # Perform a match on the output format of vpp show run
            match = re.search(r'^(\S+)\s+(\S+)\s+(\d+)\s+(\d+)', line)
            if match:
                # dpdk-input is the VPP node that will perform initial packet processing
                if match.group(1) == 'dpdk-input':
                    worker += 1

                    # Update the total number of packets coming into VPP
                    if 'tot_pkts' not in ret_dict:
                        ret_dict['tot_pkts'] = int(match.group(4))
                    else:
                        ret_dict['tot_pkts'] += int(match.group(4))

                    # Update the number of incoming packets by worker
                    if worker not in ret_dict.keys():
                        ret_dict[worker] = {'pkts':int(match.group(4))}

                # Check for handoff node
                elif match.group(1) == 'fastpath-handoff-exec':

                    # Update the total number of packets that were HH
                    if 'tot_hh' not in ret_dict:
                        ret_dict['tot_hh'] = int(match.group(4))
                    else:
                        ret_dict['tot_hh'] += int(match.group(4))

                    # Update the number of HH packets for this worker
                    ret_dict[worker]['hh'] = int(match.group(4))

                # This is the conduit  or mobility packet processing node
                elif match.group(1) == 'fastpath-executive':

                    # Update the total number of packets going through the conduit
                    if 'tot_conduit' not in ret_dict:
                        ret_dict['tot_conduit'] = int(match.group(4))
                    else:
                        ret_dict['tot_conduit'] += int(match.group(4))

                    # Update the worker with how many packets went through
                    # conduit
                    ret_dict[worker]['conduit'] = int(match.group(4))

            else:
                if not time_found:
                    match = re.search(r'^Time ([\d.]+)', line)
                    if match:
                        time_found = True
                        time_val = float(match.group(1))


        return ret_dict, time_val

    def get_interface_errors(self, interface_dict):
        """Method to collect 'important' error counts from VPP.  If any counter
        is non-zero, the method will print out the interface & counter.  This method
        currently prints out interface errors

        :param dict interface_dict: Dictionary returned from the VPP show interface

        :return None:
        """

        # Get the miss, drop and Tx error counters per interface name
        miss_dict = self.get_cntr(interface_dict)
        drop_dict = self.get_cntr(interface_dict, 'drops')
        tx_err_dict = self.get_cntr(interface_dict, 'tx-error')

        # Loop through all the dictionaries and print any non-zero 'important'
        # error counters
        for dict_name, type_name in [(miss_dict, 'rx-miss'),
                                     (drop_dict, 'drops'),
                                     (tx_err_dict, 'tx-errors')]:
            if dict_name.keys():
                for int_name, val in dict_name.items():
                    print("Interface: {0}  {1}: {2}".format(int_name,
                                                            type_name,
                                                            val))

    def intf_avg_pkt_size(self, vpp_int_dict):
        """Method to determine the avg. pkt size on the various interfaces.  The
        average packet sizes are returned to the caller in a dictionary

        :param dict vpp_int_dict: Dictionary returned from the VPP show interface

        :return: Dictionary containing the average Rx/Tx packet sizes in bytes
        :rtype: dict
        """

        # Init the return dictionary
        ret_dict = dict()

        #Loop through the interface dictionary & look for counter_name
        for int_name, int_dict in vpp_int_dict.items():
            # Check if Counter is a key
            if 'Counter' in int_dict:
                counter_dict = int_dict['Counter']

                if int_name not in ret_dict.keys():
                    ret_dict[int_name] = dict()

                if 'rx packets' in counter_dict.keys() and 'rx bytes' in counter_dict.keys():
                    ret_dict[int_name]['rx_size'] = counter_dict['rx bytes']/counter_dict['rx packets']

                if 'tx packets' in counter_dict.keys() and 'tx bytes' in counter_dict.keys():
                    ret_dict[int_name]['tx_size'] = counter_dict['tx bytes']/counter_dict['tx packets']

        return ret_dict

    def get_cntr(self, interface_dict, counter_name='rx-miss'):
        """Method that will walk the interface dictionary and look for a
        specific error couner passed in the counter_name param.  This
        method will then return a dictionary by interface name & counter

        :param dict interface_dict: Dictionary output from show interface method
        :param str counter_name: Counter name to look for

        :return: Dictionary of all interfaces that have a non-zero error counter
        :rtype: dict
        """

        # Init the return dictionary
        ret_dict = dict()

        if not isinstance(counter_name, str):
            raise Exception('Counter name should by string: {0}'.format(type(counter_name)))

        #Loop through the interface dictionary & look for counter_name
        for int_name, int_dict in interface_dict.items():
            # Check if Counter is a key
            if 'Counter' in int_dict:
                if counter_name in int_dict['Counter']:
                    ret_dict[int_name] = int_dict['Counter'][counter_name]

        return ret_dict


    def connect_device(self, yaml_file):
        """Method to connect to a device given a YAML file.  This method will
        attempt to connect to the 1 or the first device int YAML file.  This is
        a quick way of connecting.

        :param str yaml_file: Name of yaml file for the device one wants to connect

        :return: Return the device object if connected
        :rtype: dev_object
        """

        print("KKK: VppInterogate.connect_device()", yaml_file)

        # Get the full path of the testbed yaml file.  Then create the device
        cwd = os.getcwd()

        yaml_filename = yaml_file
        try:
            with open(yaml_filename, 'r') as file:
                self.yaml_dict = yaml.load(file)
        except FileNotFoundError:
            raise RuntimeError("Did not find OR could not open YAML file {0}".format(yaml_filename))

        (user, passwd, prompt, protocol, host, ts_port, sys_hostname, linux_prompt, serial, privilege_password, console, subnet_mask) = (self.yaml_dict['username'], self.yaml_dict['password'], self.yaml_dict['prompt'], self.yaml_dict['protocol'], self.yaml_dict['hostname'], None, self.yaml_dict['sys_hostname'], self.yaml_dict['linux_prompt'],None, 'boxer', None, None)

        # Get the connection info
        conn_info_dict = {"conn_name": 'primary',
                          "user_name": user,
                          "password": passwd,
                          "prompt": prompt,
                          "proto": protocol,
                          "host": host,
                          "ts_port": ts_port,
                          "system_hostname": sys_hostname,
                          "linux_prompt": linux_prompt,
                          "console": console,
                          "privilege_password" : privilege_password,
                          "serial": serial,
                          "subnet_mask" : subnet_mask}

        # vpcsi_device.py   line 62
        conn_object = comms_connection.VPCConnection(conn_info_dict)

        print("KKK: VppInterogate.connect_device() 2", conn_object)
        conn_object.login()
        self.chassis_prompt = conn_object.cli_prompt
        conn_object.enable_priv_mode()

        self.conn_obj = conn_object

        return conn_object
        

    def get_vpp_show_errors(self, device_obj):
        """Method that will get the output of the vpp show errors verbose.  The
        counters are then matched against a list of critical and frag errors.  If
        there is a non-zero counter that matches the above list, the method will
        print a message with the error type and the number of occurences.

        :param device_object device_obj: Device object of the device under test

        :return: None
        """

        # Run the show errors command
        ## vpp_err_dict = device_obj.cli_obj.vpp_show_errors.verify_cli("show errors verbose", get_parsed_output=True)
        device_obj.linux_mode()
        cmd_out = device_obj.run_command('vppctl "show errors verbose"')
        vpp_err_dict = __parse_show_vpp_errors_verbose
        device_obj.cli_mode()
        

        # Get the critical & Fragmentation error lists
        crit_err_list = gen_const.VPPCriticalErrors.VPP_CRITICAL_ERRORS.val
        frag_err_list = gen_const.VPPCriticalErrors.VPP_FRAGMENTATION_ERRORS.val

        err_dict = dict() # Create an error dictionary

        # Walk the dictionary output from the VPP show errors verbose command
        for _, thread_dict in vpp_err_dict.items():
            for _, node_dict in thread_dict.items():
                for reason_str, error_info in node_dict.items():

                    # Check if the error reason matches one of the critical errors
                    if reason_str in crit_err_list:
                        # Compute the aggreagate counter
                        if reason_str in err_dict:
                            err_dict[reason_str] += int(error_info['Count'])
                        else:
                            err_dict[reason_str] = int(error_info['Count'])

                    # Check if the error reason matches one of the frag error list
                    if reason_str in frag_err_list:
                        if reason_str in err_dict:
                            err_dict[reason_str] += int(error_info['Count'])
                        else:
                            err_dict[reason_str] = int(error_info['Count'])

        # Print out any critical and/or frag errors
        if not err_dict:
            print('\nThere are no critical Errors detected')
        else:
            # Print header
            print('\n**Found some VPP error counters**')
            print('  Error Type {0:18s} Number'.format(' '))
            for reason_str, num_items in err_dict.items():
                print('{0:<24s} {1:,d}'.format(reason_str, num_items))

    def parse_show_up(self, up_stats):
        """Method that will parse the boxer CLI  show user-plane-service statistics analyzer all
        CLI command.  The parser will generate a dictionary from the output of the command

        :param str up_stats: CLI output

        :return: dict
        """
        ret_dict = dict()

        # Capture the following sections from the output
        section_list = [('IPV4 Flow Statistics', 'IPV4'),
                        ('IPV6 Flow Statistics', 'IPV6'),
                        ('ICMPV4 Flow Statistics', 'ICMPV4'),
                        ('ICMPV6 Flow Statistics', 'ICMPV6'),
                        ('Udp Flow Statistics', 'UDP'),
                        ('TCP Flow Statistics', 'TCP'),
                        ('FTP Session Stats', 'FTP'),
                        ('DNS Sessioin Stats', 'DNS_Sess'),
                        ('DNS Over TCP', 'DNS_TCP'),
                        ('EDNS Over UDP', 'EDNS'),
                        ('Secure HTTP Session Stats', 'SHTTP'),
                        ('ECHO Reauest', 'Echo_Req'),
                        ('HTTP Session Stats', 'HTTP')]
        fastpath_sec_str = "FastPath Statistics"

        # Init various params
        cur_section = None
        fastpath_sec = False
        ul_dl_sec = False

        # Walk the output by line
        for line in up_stats.splitlines():

            # Check for a blank line:
            if not line.strip():
                fastpath_sec = False  #Not in fastpath section anymore
                ul_dl_sec = False
                continue

            fastpath_line = False #Used to detect if this line is fastpath line later

            # Check if a new section is discovered.  Fastpath section will match
            match = re.search(r'^\s+([a-zA-Z0-9 ]+):[\s]{0,4}$', line)
            if match:

                # Check if this is Fastpath stats section
                if cur_section:

                    if match.group(1).strip() == fastpath_sec_str:
                        # Note that this section is fastpath
                        fastpath_sec = True
                        ret_dict[cur_section]['FP'] = dict()
                        fastpath_line = True

                if not fastpath_line:
                    # Check for new section block
                    for sec_id, dict_id in section_list:
                        if sec_id == match.group(1):
                            cur_section = dict_id
                            if cur_section in ret_dict.keys():
                                print("Error: section {} was already in dict".format(sec_id))
                                sys.exit(1)
                            ret_dict[cur_section] = dict()
                            break
                    continue

            # Current section will idenitfy the block section of the cmd output
            if cur_section:

                # Check for FP uplink downlink section
                match = re.search(r'\s+Uplink\s+:\s+Downlink\s+:', line)
                if match:
                    ul_dl_sec = True
                    if fastpath_sec:
                        ret_dict[cur_section]['FP']['UL'] = dict()
                        ret_dict[cur_section]['FP']['DL'] = dict()
                    else:
                        ret_dict[cur_section]['UL'] = dict()
                        ret_dict[cur_section]['DL'] = dict()
                    continue

                # Determine the dictionary section to update
                if fastpath_sec:
                    up_dict = ret_dict[cur_section]['FP']
                else:
                    up_dict = ret_dict[cur_section]

                # Check if a new section is discovered.  Fastpath section will match
                match_list = re.findall(r'[a-zA-Z ]+:\s+\d+', line)
                if match_list:
                    if ul_dl_sec:
                        # There needs to be 2 matches
                        if len(match_list) != 2:
                            print('Ulink & Dlink section with not 2 matches')
                            sys.exit(1)

                        for idx in range(0, 2):
                            match = re.search(r'(.*):\s+(\d+)', match_list[idx])
                            if idx == 0:
                                up_dict['UL'][match.group(1).strip()] = int(match.group(2).strip())
                            else:
                                up_dict['DL'][match.group(1).strip()] = int(match.group(2).strip())

                    elif fastpath_sec:

                        num_items = len(match_list)
                        for idx in range(0, num_items):
                            match = re.search(r'(.*):\s+(\d+)', match_list[idx])
                            up_dict[match.group(1).strip()] = int(match.group(2).strip())

                    else:
                        num_items = len(match_list)
                        for idx in range(0, num_items):
                            match = re.search(r'(.*):\s+(\d+)', match_list[idx])
                            up_dict[match.group(1).strip()] = int(match.group(2).strip())

        return ret_dict

    def get_up_counters(self, sec_id, up_dict):
        """Method that will extract the specific counter type (sec_id) from the
        dictionary (up_dict).  The method will return the uplink & downlink pkt
        & byte counters  for FP and SMGR.

        :param str sec_id:  Section ID to collect data
        :param dict up_dict: UP counter dictionary

        :return: A dictionary of FP & SMGR counters
        :rtype: dictionary
        """

        # Get the UL and DL pkt & byte counters
        ul_pkts = up_dict[sec_id][UP_KEY_MAPPING[sec_id]['ul_pkts']]
        ul_bytes = up_dict[sec_id][UP_KEY_MAPPING[sec_id]['ul_bytes']]
        dl_pkts = up_dict[sec_id][UP_KEY_MAPPING[sec_id]['ul_pkts']]
        dl_bytes = up_dict[sec_id][UP_KEY_MAPPING[sec_id]['ul_bytes']]

        # SHTTP does not have FP stats counters
        if sec_id == 'SHTTP':
            return {'ul_pkts':ul_pkts,
                    'ul_bytes':ul_bytes,
                    'dl_pkts':dl_pkts,
                    'dl_bytes': dl_bytes}

        fp_ul_pkts = up_dict[sec_id]['FP']['UL']['Total FP Pkts']
        fp_ul_bytes = up_dict[sec_id]['FP']['UL']['Total FP Bytes']
        fp_dl_pkts = up_dict[sec_id]['FP']['DL']['Total FP Pkts']
        fp_dl_bytes = up_dict[sec_id]['FP']['DL']['Total FP Bytes']

        return {'ul_pkts':ul_pkts,
                'ul_bytes':ul_bytes,
                'dl_pkts':dl_pkts,
                'dl_bytes': dl_bytes,
                'fp_ul_pkts': fp_ul_pkts,
                'fp_ul_bytes':fp_ul_bytes,
                'fp_dl_pkts':fp_dl_pkts,
                'fp_dl_bytes':fp_dl_bytes}

    def print_up_block(self, sec_id, up_dict):
        '''This method will print the up services block

        :param str sec_id: This is the section ID to print out
        :param dict up_dict: UP counter dictionary

        :return: None    This method will print out data
        '''

        # Format Ulink string used in the print
        format_str = 'UL {0:16}  {1:20} {2:5}  {3:16} {4:20} {5:5} {6:8}'

        # If section is HTTP or SHTTP
        if sec_id == 'HTTP' or sec_id == 'SHTTP':

            # Get the UL and DL counters
            cntr_dict = self.get_up_counters(sec_id, up_dict)

            # Compute the avg packet sizes
            if cntr_dict['ul_pkts']:
                ul_avg_pkt_size = round(cntr_dict['ul_bytes']/cntr_dict['ul_pkts'])
            else:
                ul_avg_pkt_size = 0

            if 'fp_ul_pkts' in cntr_dict.keys() and  cntr_dict['fp_ul_pkts']:
                ul_fp_avg_pkt_size = round(cntr_dict['fp_ul_bytes']/cntr_dict['fp_ul_pkts'])
            else:
                ul_fp_avg_pkt_size = 0

            # Determine the percentage of offload
            if 'fp_ul_pkts' in cntr_dict.keys() and cntr_dict['ul_pkts']:
                fp_offload = round(cntr_dict['fp_ul_pkts']/cntr_dict['ul_pkts'] * 100)
            else:
                fp_offload = 0

            # SHTTP does not have any FP stats
            fp_ul_pkts = 0
            fp_ul_bytes = 0
            if 'fp_ul_pkts' in cntr_dict.keys():
                fp_ul_pkts = cntr_dict['fp_ul_pkts']
            if 'fp_ul_bytes' in cntr_dict.keys():
                fp_ul_bytes = cntr_dict['fp_ul_bytes']

            print(format_str.format(cntr_dict['ul_pkts'],
                                    cntr_dict['ul_bytes'],
                                    ul_avg_pkt_size,
                                    fp_ul_pkts,
                                    fp_ul_bytes,
                                    ul_fp_avg_pkt_size,
                                    fp_offload))

            # Now print out the DL infor
            # Compute the avg packet sizes
            if cntr_dict['dl_pkts']:
                dl_avg_pkt_size = round(cntr_dict['dl_bytes']/cntr_dict['dl_pkts'])
            else:
                dl_avg_pkt_size = 0

            # Determine the percentage of offload
            if 'fp_dl_pkts' in cntr_dict.keys() and cntr_dict['dl_pkts']:
                fp_offload = round(cntr_dict['fp_dl_pkts']/cntr_dict['dl_pkts'] * 100)
            else:
                fp_offload = 0

            if 'fp_dl_pkts' in cntr_dict.keys() and  cntr_dict['fp_dl_pkts']:
                dl_fp_avg_pkt_size = round(cntr_dict['fp_dl_bytes']/cntr_dict['fp_dl_pkts'])
            else:
                dl_fp_avg_pkt_size = 0

            # SHTTP does not have any FP stats
            fp_dl_pkts = 0
            fp_dl_bytes = 0
            if 'fp_dl_pkts' in cntr_dict.keys():
                fp_dl_pkts = cntr_dict['fp_dl_pkts']
            if 'fp_dl_bytes' in cntr_dict.keys():
                fp_dl_bytes = cntr_dict['fp_dl_bytes']

            format_str = 'DL {0:16}  {1:20} {2:5}  {3:16} {4:20} {5:5} {6:8}'
            print(format_str.format(cntr_dict['dl_pkts'],
                                    cntr_dict['dl_bytes'],
                                    dl_avg_pkt_size,
                                    fp_dl_pkts,
                                    fp_dl_bytes,
                                    dl_fp_avg_pkt_size,
                                    fp_offload))


    def print_up_sec_hdr(self):
        '''Method to print out a specific section header
        '''

        # Create and print out the UP section header
        format_str = 'Dir  {0:>14s} {1:>20s} {2:>10s} {3:>10s} {4:>20s} {5:>10s} {6:>8s}'
        print(format_str.format('SM Pkts',
                                'SM Bytes',
                                'Avg_size',
                                'FP_Pkts',
                                'FP_Bytes',
                                'Avg_size',
                                'Per_off'))


    def print_up_info(self, up_dict):
        '''Method that will print the contents of the UP

        :param dictionary up_dict: User plane dictionary

        :return: None
        '''
        # List of sections
        sections = ['IPV4',
                    'IPV6',
                    'UDP',
                    'TCP',
                    'SHTTP',
                    'HTTP']

        print('\n** Userplane services section **')
        self.print_up_sec_hdr()

        traffic_det_dict = dict()  # Traffic details dictionary

        # Loop through the sections
        for sec_id in sections:

            if sec_id == 'SHTTP' or sec_id == 'HTTP':
                print('  ** Analyzer {}'.format(sec_id))
                self.print_up_block(sec_id, up_dict)
                continue

            print(' ****  Analyzer {}'.format(sec_id))

            key_vals = ('Total Pkts', 'Total Bytes')
            pkt_byte_key = {'UDP':('Total Udp Pkts', 'Total Udp Bytes'),
                        'TCP':('Total TCP Pkts', 'Total TCP Bytes')}
            if sec_id in pkt_byte_key.keys():
                key_vals = pkt_byte_key[sec_id]

            # Print both UL and DL numbers
            for dir_str in ['UL', 'DL']:

                format_str = '{0} {1:16}  {2:20} {3:5}  {4:16} {5:20} {6:5} {7:8}'
                if up_dict[sec_id][dir_str][key_vals[0]]:
                    ul_avg_pkt_size = round(up_dict[sec_id][dir_str][key_vals[1]]/up_dict[sec_id][dir_str][key_vals[0]])
                else:
                    ul_avg_pkt_size = 0

                ## Update the traffic details dict
                if sec_id not in traffic_det_dict.keys():
                    traffic_det_dict[sec_id] = dict()
                if dir_str not in traffic_det_dict[sec_id].keys():
                    traffic_det_dict[sec_id][dir_str] = dict()
                traffic_det_dict[sec_id][dir_str]['pkt'] = up_dict[sec_id][dir_str][key_vals[0]]
                traffic_det_dict[sec_id][dir_str]['byte'] = up_dict[sec_id][dir_str][key_vals[1]]

                if up_dict[sec_id]['FP'][dir_str]['Total FP Pkts']:
                    ul_fp_avg_pkt_size = round(up_dict[sec_id]['FP'][dir_str]['Total FP Bytes']/up_dict[sec_id]['FP'][dir_str]['Total FP Pkts'])
                else:
                    ul_fp_avg_pkt_size = 0

                # Determine the percentage of offload
                if up_dict[sec_id][dir_str][key_vals[0]]:
                    fp_offload = round(up_dict[sec_id]['FP'][dir_str]['Total FP Pkts']/up_dict[sec_id][dir_str][key_vals[0]] * 100)
                else:
                    fp_offload = 0

                print(format_str.format(dir_str,
                                        up_dict[sec_id][dir_str][key_vals[0]],
                                        up_dict[sec_id][dir_str][key_vals[1]],
                                        ul_avg_pkt_size,
                                        up_dict[sec_id]['FP'][dir_str]['Total FP Pkts'],
                                        up_dict[sec_id]['FP'][dir_str]['Total FP Bytes'],
                                        ul_fp_avg_pkt_size,
                                        fp_offload))

        # Collect the IP related info
        ip4_ul_pkt = int(traffic_det_dict['IPV4']['UL']['pkt'])
        #ip4_ul_bytes = int(traffic_det_dict['IPV4']['UL']['byte'])
        ip4_dl_pkt = int(traffic_det_dict['IPV4']['DL']['pkt'])
        #ip4_dl_bytes = int(traffic_det_dict['IPV4']['DL']['byte'])

        ip6_ul_pkt = int(traffic_det_dict['IPV6']['UL']['pkt'])
        #ip6_ul_bytes = int(traffic_det_dict['IPV6']['UL']['byte'])
        ip6_dl_pkt = int(traffic_det_dict['IPV6']['DL']['pkt'])
        #ip6_dl_bytes = int(traffic_det_dict['IPV6']['DL']['byte'])

        # Compute the UL,DL and total pkt counters for IP
        tot_ip_ul_pkts = ip4_ul_pkt + ip6_ul_pkt
        tot_ip_dl_pkts = ip4_dl_pkt + ip6_dl_pkt
        tot_ip_pkts = tot_ip_ul_pkts + tot_ip_dl_pkts

        # Compute the UL,DL and total bytes counters for IP
        ##tot_ip_ul_bytes = ip4_ul_bytes + ip6_ul_bytes
        ##tot_ip_dl_bytes = ip4_dl_bytes + ip6_dl_bytes
        ##tot_ip_bytes = tot_ip_ul_bytes + tot_ip_dl_bytes

        # Print out the IP details
        print('*** Details using IP counters ***')
        str_format = '{0}\n{1:>8} {2:>8}\n{3:8.2f} {4:8.2f}'
        if tot_ip_pkts:
            print(str_format.format('UL/DL breakout using PKT Cntrs',
                                    'UL Perc', 'DL Perc',
                                    tot_ip_ul_pkts/tot_ip_pkts,
                                    tot_ip_dl_pkts/tot_ip_pkts))
        else:
            print(str_format.format('UL/DL breakout using PKT Cntrs',
                                    'UL Perc', 'DL Perc', 0, 0))

        str_format = '{0}\n{1:>16} {2:>16}\n{3:16.2f} {4:16.2f}'
        if tot_ip_ul_pkts:
            print(str_format.format('UL Breakout using PKT Cntrs',
                                    'IPv4 UL Perc', 'IPv6 UL Perc',
                                    ip4_ul_pkt/tot_ip_ul_pkts,
                                    ip6_ul_pkt/tot_ip_ul_pkts))
        else:
            print(str_format.format('UL Breakout using PKT Cntrs',
                                    'IPv4 UL Perc', 'IPv6 UL Perc', 0, 0))

        str_format = '{0}\n{1:>16} {2:>16}\n{3:16.2f} {4:16.2f}'
        if tot_ip_dl_pkts:
            print(str_format.format('DL Breakout using PKT Cntrs',
                                    'IPv4 DL Perc', 'IPv6 DL Perc',
                                    ip4_dl_pkt/tot_ip_dl_pkts,
                                    ip6_dl_pkt/tot_ip_dl_pkts))
        else:
            print(str_format.format('DL Breakout using PKT Cntrs',
                                    'IPv4 DL Perc', 'IPv6 DL Perc', 0, 0))

        # Compute various protcol counters
        tcp_ul_pkt = int(traffic_det_dict['TCP']['UL']['pkt'])
        ##tcp_ul_bytes = int(traffic_det_dict['TCP']['UL']['byte'])
        tcp_dl_pkt = int(traffic_det_dict['TCP']['DL']['pkt'])
        ##tcp_dl_bytes = int(traffic_det_dict['TCP']['DL']['byte'])

        udp_ul_pkt = int(traffic_det_dict['UDP']['UL']['pkt'])
        ##udp_ul_bytes = int(traffic_det_dict['UDP']['UL']['byte'])
        udp_dl_pkt = int(traffic_det_dict['UDP']['DL']['pkt'])
        ##udp_dl_bytes = int(traffic_det_dict['UDP']['DL']['byte'])

        tot_udp_pkts = udp_ul_pkt + udp_dl_pkt
        tot_tcp_pkts = tcp_ul_pkt + tcp_dl_pkt
        tot_prot_ul_pkts = udp_ul_pkt + tcp_ul_pkt
        tot_prot_dl_pkts = udp_dl_pkt + tcp_dl_pkt

        # Print out the PROT details
        print('*** Details using Proto PKT counters ***')
        str_format = '{0}\n{1:>8} {2:>8}\n{3:8.2f} {4:8.2f}'
        if (tot_udp_pkts + tot_tcp_pkts):
            print(str_format.format('UL/DL TCP/UDP breakout using PKT Cntrs',
                                    'UDP Proto Perc', 'TCP Proto Perc',
                                    tot_udp_pkts/(tot_udp_pkts + tot_tcp_pkts),
                                    tot_tcp_pkts/(tot_udp_pkts + tot_tcp_pkts)))
        else:
            print(str_format.format('UL/DL TCP/UDP breakout using PKT Cntrs',
                                    'UDP Proto Perc', 'TCP Proto Perc', 0, 0))

        str_format = '{0}\n{1:>16} {2:>16}\n{3:16.2f} {4:16.2f}'
        if tot_prot_ul_pkts:
            print(str_format.format('UL Breakout using PKT Cntrs',
                                    'UDP UL Perc', 'TCP UL Perc',
                                    udp_ul_pkt/tot_prot_ul_pkts,
                                    tcp_ul_pkt/tot_prot_ul_pkts))
        else:
            print(str_format.format('UL Breakout using PKT Cntrs',
                                    'UDP UL Perc', 'TCP UL Perc', 0, 0))

        str_format = '{0}\n{1:>16} {2:>16}\n{3:16.2f} {4:16.2f}'
        if tot_prot_dl_pkts:
            print(str_format.format('DL Breakout using PKT Cntrs',
                                    'UDP DL Perc', 'TCP DL Perc',
                                    udp_dl_pkt/tot_prot_dl_pkts,
                                    tcp_dl_pkt/tot_prot_dl_pkts))
        else:
            print(str_format.format('DL Breakout using PKT Cntrs',
                                    'UDP DL Perc', 'TCP DL Perc', 0, 0))

    def proc_userplane_stats_analyzer(self, device_obj):
        """Method that will get the userplane stats

        :param device_object device_obj: Device object of the device under test

        :return: None
        """

        # Run the show userplane stats command
        up_stats = device_obj.run_command("show user-plane-service statistics analyzer all")
        up_dict = self.parse_show_up(up_stats)

        self.print_up_info(up_dict)

        ##yaml_dict = yaml.load(up_stats)

        #print('DJPDJP {}'.format(up_dict))

        ##print('YAML load\n{}\n'.format(yaml_dict))

        ##print('CLI OUTPUT\n{}\n'.format(up_stats))
        ##print(yaml.dump(up_dict, default_flow_style=False))

    def get_stream_info(self, ups_fapi_dict):
        """Method that will parse the boxer CLI  show user-plane-service statistics fapi all
        CLI command

        :param str up_stats: CLI output
        
        :return: dict
        """

        ret_dict = dict()
        # Walk the dictionary for each SMGR
        for smgr_inst, smgr_dict in ups_fapi_dict.items():

            # Each param below will be a 4-tuple with  Req, SuccessRsp, FailRsp, Timeout
            str_add = smgr_dict['str add']
            str_del = smgr_dict['str delete']
            str_mod = smgr_dict['str modify']

            ret_dict[smgr_inst] = (str_add, str_del, str_mod)

        return ret_dict

    def print_stream_info(self, smgr_dict):
        """Method that will parse the boxer CLI  show user-plane-service statistics fapi all
        CLI command

        :param str up_stats: CLI output

        :return: dict
        """

        print('\n*** Stream info ***')
        hdr_format = '{0:8} {1:>16} {2:>16} {3:>16} {4:>16}'
        hdr_str = hdr_format.format('SMGR Inst',
                                    'Stream Add',
                                    'Stream Del',
                                    'Stream Mod',
                                    'Active Stream')
        # Print the Section HDR
        print(hdr_str)

        # Init the total variables
        tot_str_add, tot_str_del, tot_str_mod, tot_str_active = (0,)*4

        # Print out the stream related data from each SMGR Instance
        format_str = '{0:8} {1:>16} {2:>16} {3:>16} {4:>16}'
        for smgr_inst in sorted(smgr_dict.keys(), key=int):
            str_tuple = smgr_dict[smgr_inst]
            active_stream = int(str_tuple[0][0]) - int(str_tuple[1][0])

            tot_str_add += int(str_tuple[0][0])
            tot_str_del += int(str_tuple[1][0])
            tot_str_mod += int(str_tuple[2][0])
            tot_str_active += active_stream
            print(format_str.format(smgr_inst,
                                    str_tuple[0][0], str_tuple[1][0],
                                    str_tuple[2][0], active_stream))

        # Print the totals
        print(format_str.format('Total',
                                tot_str_add, tot_str_del,
                                tot_str_mod, tot_str_active))

    def print_delta_stream(self, streams_list):
        """Method that will print stream add,delete rates.  The streams_list
        is a list where each entry contains a tuple (datetime, stream_info_dict)

        :param str streams_list: List of time stamps and stream info

        :return: None
        """
        print('\n*** Stream Rate info ***')
        hdr_format = '{0:16} {1:16} {2:>16} {3:>16} {4:>16}'
        hdr_str = hdr_format.format('Time Window',
                                    'SMGR Inst',
                                    'Str Add Rate',
                                    'Str Del Rate',
                                    'Str Mod Rate')
        print(hdr_str)

        format_str = '{0:16} {1:16} {2:>16.2f} {3:>16.2f} {4:>16.2f}'

        # Init current time
        cur_time = None

        # Loop through the list of stream data.
        for stream_entry in streams_list:

            # Get the current time.  The 0th entry will be the last capture
            # and also get the stream info baseline
            if not cur_time:
                cur_time = stream_entry[0]
                cur_stream_info = stream_entry[1]
                continue

            # Capture the time stamp and stream info for 2nd entry on
            time_stamp = stream_entry[0]
            stream_info_dict = stream_entry[1]

            # Compute the timestamp delta
            time_delta = cur_time - time_stamp
            print(time_delta)
            num_seconds = time_delta.total_seconds()

            for smgr_inst in sorted(stream_info_dict.keys(), key=int):
                str_tuple = stream_info_dict[smgr_inst]
                # Compute the stream add rate
                str_add_rate = (int(cur_stream_info[smgr_inst][0][0]) -\
                                    int(str_tuple[0][0]))/num_seconds
                str_del_rate = (int(cur_stream_info[smgr_inst][1][0]) -\
                                    int(str_tuple[1][0]))/num_seconds
                str_mod_rate = (int(cur_stream_info[smgr_inst][2][0]) -\
                                    int(str_tuple[2][0]))/num_seconds

                print(format_str.format('', smgr_inst,
                                        str_add_rate, str_del_rate,
                                        str_mod_rate))

    def print_fapi_errs(self, up_stats_dict):
        """Method that will parse the boxer CLI  show user-plane-service statistics fapi all
        CLI command

        :param str up_stats: CLI output

        :return: dict
        """

        # The list of FAPI table names. These are keys in the UP dictionary
        fapi_table_keys = ['Stream-Stats',
                           'TEP',
                           'HCF',
                           'NHFWD',
                           'LC',
                           'Quota',
                           'Policer',
                           'Policer-Bucket']

        hdr_str = False
        hdr_line = '{0:16s} {1:12s} {2:16s} {3:16s}'.format('SMGR Instance', 'TBL', 'Used', 'Alloc')
        format_str = '{0:16s} {1:12s} {2:16s} {3:16s}'


        # Loop over the userplane dictionary.
        for smgr_inst, smgr_dict in up_stats_dict.items():
            # Check if state is not open
            if smgr_dict['state'] != 'OPEN':
                print('SMGR Instance {0} FAPI connection is {1}'.format(smgr_inst,
                                                                        smgr_dict['State']))

            # Check if Used Rows is 80% or more than the Max rows
            for tbl_key in fapi_table_keys:
                if int(smgr_dict[tbl_key][2])*.8 < int(smgr_dict[tbl_key][4]):

                    if not hdr_str:
                        print('\n**** FAPI Table Usage Info ***')
                        print(hdr_line)
                        hdr_str = True
                    print(format_str.format(smgr_inst,
                                            tbl_key,
                                            smgr_dict[tbl_key][2],
                                            smgr_dict[tbl_key][4]))



    def print_task_info(self, device_obj):
        """Method that will parse the boxer CLI  show user-plane-service statistics fapi all
        CLI command

        :param str up_stats: CLI output

        :return: dict
        """
        # Get the task resources
        # Print the SMGR info
        print('\n*** Task Resources ***')
        print('Session Manager')

        task_smgr_cli = device_obj.run_command("show task resources facility sessmgr all")
        print(task_smgr_cli)

        ##task_res_dict = device_obj.cli_obj.get_show_task_resources()
        cmd_out = device_obj.run_command("show task resources")
        task_res_dict = parse_show_task_resources(cmd_out)

        # Attempt to print the VPP resources
        if 1 in task_res_dict.keys() and 0 in task_res_dict[1].keys() and 'vpp_main' in task_res_dict[1][0].keys():
            vpp_task_dict = task_res_dict[1][0]['vpp_main']
            vpp_task_list = list(vpp_task_dict.keys())
            if len(vpp_task_list) == 1:
                vpp_key = vpp_task_list[0]
                print('\n**VPP Process')

                print('{0:16} {1:16} {2:16}'.format("Mem Used", "Mem Alloc", "Proc Used"))
                vpp_str_format = '{0:16} {1:16} {2:16}'
                print(vpp_str_format.format(vpp_task_dict[vpp_key]['memory_used'],
                                            vpp_task_dict[vpp_key]['memory_alloc'],
                                            vpp_task_dict[vpp_key]['cputime_used']))

        print('\n**Summary of all tasks')

        if 'Total' in task_res_dict.keys():
            tot_info = task_res_dict['Total']
            str_format = '{0:16} {1:16} {2:16} {3:16}'
            print(str_format.format('Num Instances', 'CPU Load',
                                    'Mem Usage', 'Num Files'))
            print(str_format.format(tot_info['num_inst'], tot_info['cputime_used'],
                                    tot_info['memory_used'], tot_info['files']))

    def parse_ups_fapi(self, cmd_out):
        """Method that will parse the boxer CLI  show user-plane-service statistics fapi all
        CLI command

        :param str up_stats: CLI output

        :return: dict
        """

        ret_dict = dict()
        cur_dict = None
        cmd_notif_sec = False
        for line in cmd_out.splitlines():
            match = re.search(r'Session Manager : (\d+)', line)
            if match:
                smgr_instance = match.group(1)
                cmd_notif_sec = False

                if smgr_instance in ret_dict.keys():
                    print('Error: Smgr instance {} already exists in dictionary'.format(smgr_instance))
                    sys.exit(1) #DJP

                # Add SMGR instance to the dictionary
                ret_dict[smgr_instance] = dict()
                cur_dict = ret_dict[smgr_instance]

            match = re.search(r'FAPI-Client-Info: Key: ([0-9a-fA-Fx]+), State: (\w+), Thread: (\d+), (Numa: (\d), )?Version: (\d+)', line)
            if match:
                cur_dict['key'] = match.group(1)
                cur_dict['state'] = match.group(2)
                cur_dict['thread'] = match.group(3)
                if match.group(5):
                    cur_dict['numa'] = match.group(5)
                cur_dict['version'] = match.group(6)

                continue

            match = re.search(r'(Streams|Tables):\s+(\d+)', line)
            if match:
                cur_dict[match.group(1)] = match.group(2)
                continue

            match = re.search(r'\s+(\d+)\s+([\w-]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
            if match:
                # Add the table data to the dict.  The value is a tuple (tableId, col_size, maxrows, allocrows, usedrows)
                cur_dict[match.group(2)] = (match.group(1), match.group(3),
                                            match.group(4), match.group(5),
                                            match.group(6))
                continue

            if re.search(r'Command/Notification\s+Req/Notif\s+Success Resp', line):
                cmd_notif_sec = True
                continue

            if cmd_notif_sec:
                match = re.search(r'([a-zA-Z ]+)\(shm\)\s+(\d+)\s+(\d+)\s+(\d+)\s+(N/A|\d+)', line)
                if match:
                    # Add a tuple for the command info.  (Req/Notif, SeccessRsp, RailRsp, Timeout)
                    cur_dict[match.group(1).strip()] = (match.group(2), match.group(3),
                                                        match.group(4), match.group(5))
        return ret_dict

    def proc_userplane_stats_fapi(self, device_obj):
        """Method that will get the userplane fapi stats

        :param device_object device_obj: Device object of the device under test

        :return: None
        """

        # Run the show userplane stats command
        cmd_out = device_obj.run_command("show user-plane-service statistics fapi all")
        cmd_time = datetime.now()
        ups_fapi_dict = self.parse_ups_fapi(cmd_out)
        return (ups_fapi_dict, cmd_time)

    def blocking_hist(self, hist_dict, card=1, cpu=0):
        '''Method to extract the blocking node info for VPP thread 0 (main thread)

        :param dict hist_dict: Show histogram dictionary
        :param int card: Card number
        :param int cpu: CPU number

        :rtype: List of lists
        '''

        # Get the card/cpu dict
        if (card, cpu) not in hist_dict.keys():
            return None
        
        # Check if the card/cpu dict has a thread 0 data
        if 0 not in hist_dict[(card, cpu)].keys():
            return None

        # Get the VPP main thread dict
        main_thread_dict = hist_dict[(card, cpu)][0]
        ret_list = list()

        # Loop through all the node info in the main thread 
        for node_name in main_thread_dict.keys():

            # Only check blocking node names
            if 'block' in node_name:
                # Reset the number of events
                num_times = 0

                # compute the total number of times
                bucket_list = main_thread_dict[node_name]['bucket']
                for bucket_entry in bucket_list:
                    num_times += bucket_entry[1]

                tot_dt = None
                min_dt = None
                max_dt = None
                if 'Total_dT' in main_thread_dict[node_name].keys():
                    tot_dt = main_thread_dict[node_name]['Total_dT']
                if 'min_dt' in main_thread_dict[node_name].keys():
                    min_dt = main_thread_dict[node_name]['min_dt']
                if 'max_dt' in main_thread_dict[node_name].keys():
                    max_dt = main_thread_dict[node_name]['max_dt']

                ret_list.append((node_name, num_times, tot_dt, min_dt, max_dt))

        ret_list.sort(key = operator.itemgetter(1), reverse = True)
        return ret_list

    def print_blocking(self, main_list):
        '''Method to print out the blocking node information from the VPP main thread

        '''

        # Identify node entry print format
        main_print_format = r'{0:<60s} {1:>3s} {2:>12s} {3:>12d} {4:>12s} {5:>12s} {6:>12s} {7:>12s}'
        main_hdr_format = r'{0:<60s} {1:>3s} {2:>12s} {3:>12s} {4:>12s} {5:>12s} {6:>12s} {7:>12s}'

        # Identify the block as the Blockin node details
        print('\n********************************************')
        print('***** VPP Main Thread Blocking details *****\n')

        # Print out the key of the columns
        print('KEY:')
        print('  Node Name - VPP Node')
        print('  Per - Time percentage.  Total dT/time_since_last_hist_cleared')
        print('  Avg dT - Average time node ran.  Total/Num_Calls')
        print('  Num Calls - Number of times this node was called')
        print('  Total dT - Total Accumlated time run for this node')
        print('  Min Time - The minimum time for a given run of the node')
        print('  Max Time - The maximum time for a given run of the node')
        print('  Call Period - The period of node\n')

        # Determine if time window is known
        if self.last_hist_clear_tod:
            delta_time = self.hist_cmd_tod - self.last_hist_clear_tod
            print('** Histogram data represents {0} of time'.format(delta_time))

            num_seconds = delta_time.total_seconds()

        # Print the header
        print(main_hdr_format.format('Node Name', 'Per', 'Avg dT', 
                                     'Num Calls', 'Total dT',
                                     'Min Time', 'Max Time',
                                     'Call Period'))

        # Loop through all the node info
        for node_info in main_list:
            # Compute the avg node duration per call
            avg_time = self.compute_avg(node_info[2], node_info[1])
            if not avg_time:
                avg_time = '-'

            # Compute the call period if the last clear hist TOD is known
            if self.last_hist_clear_tod:
                call_per = self.compute_avg(num_seconds, node_info[1])
            else:
                call_per = '-'

            # Compute the number of secs from the total dT value
            per_time = '-'
            if self.last_hist_clear_tod:
                dt_secs = self.convert_dt_to_sec(node_info[2])
                per_time = int(round(float(r'{0:6.1f}'.format(dt_secs/num_seconds * 100.0))))

            print(main_print_format.format(node_info[0],
                                           str(per_time),
                                           avg_time,
                                           node_info[1],
                                           node_info[2],
                                           node_info[3],
                                           node_info[4],
                                           call_per))

    def compute_avg(self, tot_time, num_calls):
        '''Method to compute the average time of a specific node call.  The
        tot_time is a string representing total time.  The num_calls is the number
        of times the call was called

        :param str tot_time: The total dT time in string form
        :param int num_calls: The number of times the node method was called

        :return: Return the average time per call
        :rtype: Str
        '''


        if isinstance(tot_time, str):
            # Convert time to seconds
            time_in_sec = self.convert_dt_to_sec(tot_time)
        elif isinstance(tot_time, float):
            time_in_sec = tot_time
        else:
            return None

        if time_in_sec:
            avg_time = time_in_sec/num_calls
            dt_avg_time = self.convert_sec_to_dt(avg_time)
            return dt_avg_time
        return None

    def print_hist(self, hist_dict, num_thread_entries = 'all'):
        '''Method to print out the ordered histogram dictionary contents

        '''

        # Identify node entry print format
        node_print_format = r'{0:<40s} {1:>3s} {2:>12s} {3:>16d} {4:>12s} {5:>12s} {6:>12s} {7:>8} {8:>5s} {9:>5s} {10:>16s}'
        hist_hdr = r'{0:<40s} {1:>3s} {2:>12s} {3:>16s} {4:>12s} {5:>12s} {6:>12s} {7:>8s} {8:>5s} {9:>5s} {10:>16s}'

        # Loop through each Thread
        print('*********************************')
        print('***** VPP Histogram details *****')

        if self.last_hist_clear_tod:
            delta_time = self.hist_cmd_tod - self.last_hist_clear_tod
            print('** Histogram data represents {0} of time'.format(delta_time))

            num_seconds = delta_time.total_seconds()

        num_max_entries = 12
        if isinstance(num_thread_entries, int):
            num_max_entries = num_thread_entries
        num_max_entries = 12

        # Loop through the thread IDs
        for thread_id in hist_dict.keys():
            print('\n** VPP Thread {0} **'.format(thread_id))
            print(hist_hdr.format('Node Name', 'Per', 'Total Time',
                                  'Number Calls', 'Avg dT',
                                  'Min dT', 'Max dT', 
                                  'Avg Vec', 'MinV',
                                  'MaxV', 'Total Vec'))
            num_entries = 0

            # Loop through the node entries
            for node_tuple in hist_dict[thread_id]:
                num_entries += 1
                if num_entries > num_max_entries:
                    break  # Break when we hit the max number entries per node

                # Compute the average time per call
                avg_time = self.compute_avg(node_tuple[2], node_tuple[3])
                if not avg_time:
                    avg_time = '-'

                # Compute the average vector size
                if node_tuple[8] != '-':
                    avg_vec = r'{0:6.2f}'.format(float(node_tuple[8])/float(node_tuple[3]))
                else:
                    avg_vec = '-'

                # Compute the number of secs from the total dT value
                per_time = '-'
                if self.last_hist_clear_tod:
                    if node_tuple[2]:
                        dt_secs = self.convert_dt_to_sec(node_tuple[2])
                        per_time = int(round(float(r'{0:6.1f}'.format(dt_secs/num_seconds*100.0))))

                # Check if the total_dT, which is set in node_tuple[2] is set to None
                # If this value is None, set it to str -
                if not node_tuple[2]:
                    total_dT = '-'
                else:
                    total_dT = node_tuple[2]

                print(node_print_format.format(node_tuple[0],
                                               str(per_time),
                                               total_dT,
                                               node_tuple[3],
                                               avg_time,
                                               node_tuple[4],
                                               node_tuple[5],
                                               str(avg_vec),
                                               node_tuple[6],
                                               node_tuple[7],
                                               node_tuple[8]))

    def convert_dt_to_sec(self, dt_val):
        '''Method that will convert the dT value in the vppctl show histogram output.
        The dT value will have a number followed by units. The units can be
        cl,ns,us,ms,s,m,h,d .  This method will convert this number to a floating
        point value representing the number of seconds.

        :param string dt_val: This is the total time value in the show histogram output

        :return: Floating point value of seconds
        :rtype: float
        '''

        cl_time = 5e-10  # 2Ghz clock

        match = re.search(r'([\d.]+)(cl|ns|us|ms|s|m|h|d)',dt_val)
        if match:
            ret_val = float(match.group(1))

            if match.group(2) == 'cl':
                ret_val *= cl_time
            elif match.group(2) == 'ns':
                ret_val *= 1e-9
            elif match.group(2) == 'us':
                ret_val *= 1e-6
            elif match.group(2) == 'ms':
                ret_val *= 1e-3
            elif match.group(2) == 's':
                pass
            elif match.group(2) == 'm':
                ret_val *= 60
            elif match.group(2) == 'h':
                ret_val *= 3600
            elif match.group(2) == 'd':
                ret_val *= 86400
            return(ret_val)
        else:
            return(None)

    def convert_sec_to_dt(self, sec_val):
        '''Method that will convert the time in seconds to a dT value as a string.
        The dT value will have a number followed by units. The units can be
        cl,ns,us,ms,s,m,h,d .  This method will convert floating point number of
        seconds to dT value.

        :param float sec_val: This is the total time value in seconds

        :return: String time
        :rtype: str
        '''

        # First convet number into nsec.
        conv_val = sec_val * 1e9

        if int(conv_val) >=1 and int(conv_val) <= 999:
            conv_val = r'{0:.3f}'.format(conv_val) + 'ns'
            return conv_val
        conv_val /= 1e3
        if int(conv_val) >=1 and int(conv_val) <= 999:
            conv_val = r'{0:.3f}'.format(conv_val) + 'us'
            return conv_val
        conv_val /= 1e3
        if int(conv_val) >=1 and int(conv_val) <= 999:
            conv_val = r'{0:.3f}'.format(conv_val) + 'ms'
            return conv_val
        conv_val /= 1e3
        if int(conv_val) >=1 and int(conv_val) <= 999:
            conv_val = r'{0:.3f}'.format(conv_val) + 's'
            return conv_val
        conv_val /= 60
        if int(conv_val) >=1 and int(conv_val) <= 999:
            conv_val = r'{0:.3f}'.format(conv_val) + 'm'
            return conv_val
        conv_val /= 60
        if int(conv_val) >=1 and int(conv_val) <= 999:
            conv_val = r'{0:.3f}'.format(conv_val) + 'h'
            return conv_val

        return None

    def order_hist(self, hist_dict, card=1, cpu=0):
        '''Method to order the histogram dictionary by total time value.
        This is used to determine what VPP nodes are using most of the time

        :param dict hist_dict: Show histogram dictionary

        :rtype: List of lists
        '''

        # Get the card/cpu dict
        if (card, cpu) not in hist_dict.keys():
            return None
        
        card_cpu_dict = hist_dict[(card, cpu)]
        ret_dict = dict()

        # Walk each thread ID   and determine the ordered list by total dVT
        for thread_id in card_cpu_dict.keys():
            ret_dict[thread_id] = list()
            for node_name in card_cpu_dict[thread_id].keys():

                num_bucket_entries = 0  # Init the number of bucket entries
                min_dt = '-'
                max_dt = '-'
                min_vec = '-'
                max_vec = '-'
                total_vec = '-'
                num_bucket_entries = 0

                # Compute the number of bucket times
                if 'bucket' in card_cpu_dict[thread_id][node_name].keys():
                    for bucket_entry in card_cpu_dict[thread_id][node_name]['bucket']:
                        num_bucket_entries += bucket_entry[1]

                # Update the min & max dT  if keys exist
                if 'min_dt' in card_cpu_dict[thread_id][node_name].keys():
                    min_dt = card_cpu_dict[thread_id][node_name]['min_dt']
                if 'max_dt' in card_cpu_dict[thread_id][node_name].keys():
                    max_dt = card_cpu_dict[thread_id][node_name]['max_dt']

                if 'Total_dT' in card_cpu_dict[thread_id][node_name].keys():
                    total_dT = card_cpu_dict[thread_id][node_name]['Total_dT']
                    tot_sec = self.convert_dt_to_sec(total_dT)
                else:
                    total_dT = None
                    tot_sec = 0.0

                if 'max_vec' in card_cpu_dict[thread_id][node_name].keys():
                    max_vec = card_cpu_dict[thread_id][node_name]['max_vec']
                if 'min_vec' in card_cpu_dict[thread_id][node_name].keys():
                    min_vec = card_cpu_dict[thread_id][node_name]['min_vec']
                if 'Total_vec' in card_cpu_dict[thread_id][node_name].keys():
                    total_vec = str(card_cpu_dict[thread_id][node_name]['Total_vec'])

                # print('DJPAA {0}'.format(tot_sec))
                ret_dict[thread_id].append((node_name, tot_sec, 
                                            total_dT,
                                            num_bucket_entries,
                                            min_dt,
                                            max_dt,
                                            min_vec,
                                            max_vec,
                                            total_vec))

            # Now order the list
            ret_dict[thread_id].sort(key = operator.itemgetter(1), reverse=True)

        return ret_dict

    def collect_smgr(self, device_obj):
        '''Method to order the histogram dictionary by total time value.
        This is used to determine what VPP nodes are using most of the time

        :param dict hist_dict: Show histogram dictionary

        :rtype: List of lists
        '''
        cmd_out = device_obj.run_command("show port utilization table")
        self.fptr.write('**{0}\n{1}'.format('CMD: show port util table', cmd_out))
        cmd_out = device_obj.run_command("show task resources")
        self.fptr.write('**{0}\n{1}'.format('CMD: show task resources', cmd_out))
        cmd_out = device_obj.run_command("show profile facility sessmgr instance 8 depth 8")
        self.fptr.write('**{0}\n{1}'.format('CMD: show profile facility sessmgr instance 8 depth 8', cmd_out))
        cmd_out = device_obj.run_command("show user-plane-service statistics analyzer name tcp")
        self.fptr.write('**{0}\n{1}'.format('CMD: show user-plane-service statistics analyzer name tcp', cmd_out))
        cmd_out = device_obj.run_command("show user-plane-service statistics analyzer name http")
        self.fptr.write('**{0}\n{1}'.format('CMD: show user-plane-service statistics analyzer name http', cmd_out))
        cmd_out = device_obj.run_command("show user-plane-service statistics analyzer all")
        self.fptr.write('**{0}\n{1}'.format('CMD: show user-plane-service statistics analyzer all', cmd_out))

    def print_menu(self):
        """This method will print out the help menu of the interactive commands
        """

        help_str = '''h: Print Help Menu
q: Quit
c: Clear counters
d: Get all data'''
        print(help_str)

    def print_all_safe(self, device_obj):
        """Method to print all the information using VPP safe commands

        :param device_object device_obj: Device object of device under test

        :rtype: None
        """
        # Declare global stream list
        global STREAM_LIST

        # Run the LInux VPP interface commands
        device_obj.linux_mode()
        if_stats = device_obj.run_command("vpp_get_stats dump /if")
        device_obj.cli_mode()
        if_dict = safe_vpp.parse_vpp_if_stats(if_stats)
        safe_vpp.print_if_errors(if_dict, CACHE_IF_DICT)
        safe_vpp.print_avg_pkt_size(if_dict, CACHE_IF_DICT)

        #num_workers = self.process_num_threads(device_obj)
        self.get_num_smgrs(device_obj)

        device_obj.linux_mode()
        perf_stats = device_obj.run_command("vpp_get_stats dump /sys")
        perf_dict = safe_vpp.parse_vpp_sys(perf_stats)
        safe_vpp.print_packet_flow(perf_dict, CACHE_PERF_DICT)


        err_cmd_out = device_obj.run_command("vpp_get_stats dump /err")
        device_obj.cli_mode()
        err_dict = safe_vpp.parse_vpp_err(err_cmd_out)

        # DJPDJP
        #if CACHE_ERR_DICT:
        #    print('DJP writing data')
        #    fptr = open('/tmp/dd','w')
        #    fptr.write('DJP {0}'.format(CACHE_ERR_DICT))
        #    fptr.close()

        safe_vpp.print_vpp_errors(err_dict, CACHE_ERR_DICT)
        device_obj.cli_mode()

        # This block is to use the show run data to determine percentage
        # of offloaded packets using VPP counters

        # Certain Node counter print format
        cntr_node_fmt = '{0:^28} {1:^28} {2:^28}'

        list_nodes = ['adj-meh-rewrite-swap-dbia', 
                      'ip4-meh-imposition-dpo',
                      'ip6-meh-imposition-dpo']
        agg_node_cnts = safe_vpp.get_agg_pkts(perf_dict, list_nodes)
        print('\n*** Percentage of offload using VPP node counters ***')
        print(cntr_node_fmt.format('adj-meh-rewrite-swap-dbia', 
                                   'ip4-meh-imposition-dpo',
                                   'ip6-meh-imposition-dpo'))
        print(cntr_node_fmt.format(agg_node_cnts[0],
                                   agg_node_cnts[1],
                                   agg_node_cnts[2]))
        if agg_node_cnts[1] or agg_node_cnts[2]:
            print('Percentage of offloaded traffic: {0}%\n'.format(float(agg_node_cnts[0])/
                                                                   float(agg_node_cnts[1] + agg_node_cnts[2]) * 100.0))
        else:
            print('Percentage of offloaded traffic: No_PKTs sent to App\n')
            

        ##

        self.proc_userplane_stats_analyzer(device_obj)

        # Collect stream info
        fapi_dict, cmd_time = self.proc_userplane_stats_fapi(device_obj)

        # Detect if any tables are getting close to full
        self.print_fapi_errs(fapi_dict)

        # Extract the stream adds, modify & delete info from fapi dict
        stream_info_dict = self.get_stream_info(fapi_dict)

        self.print_stream_info(stream_info_dict)

        # Add the time & fapi dict
        STREAM_LIST.insert(0, (cmd_time, stream_info_dict))

        # Check if the stream list is non empty.
        if len(STREAM_LIST) > 1:
            self.print_delta_stream(STREAM_LIST)

        self.print_task_info(device_obj)

        # Get histogram data
        self.hist_cmd_tod = datetime.now()


        ##hist_dict = device_obj.cli_obj.vpp_misc_parser.verify_cli("show histogram verbose", get_parsed_output=True)
        device_obj.linux_mode()
        cmd_out = device_obj.run_command('vppctl "show histogram verbose"')
        hist_dict = parse_show_histogram_verbose(cmd_out)
        device_obj.cli_mode()

        # Get the ordered list by thread of the
        hist_order_dict = self.order_hist(hist_dict)
        self.print_hist(hist_order_dict, num_thread_entries = 100)

        # Get & print the blocking stats
        main_blocking_dict = self.blocking_hist(hist_dict)
        self.print_blocking(main_blocking_dict)

        # Collect all the smgr data
        self.collect_smgr(device_obj)
    

    def print_all(self, device_obj):
        """Method to print all the information

        :param device_object device_obj: Device object of device under test
        
        :rtype: None
        """
        # Get the ordered list by thread of the
        hist_order_dict = self.order_hist(parse2_output)
        self.print_hist(hist_order_dict, num_thread_entries = 100)
        os.exit(22)

        

        self.process_interface_data(device_obj)
        num_workers = self.process_num_threads(device_obj)
        self.get_num_smgrs(device_obj)
        self.get_pkt_flow_stats(device_obj, num_workers)
        self.get_vpp_show_errors(device_obj)

        self.proc_userplane_stats_analyzer(device_obj)

    def cache_vpp_stats(self, device_obj):
        '''
        '''
        global LAST_CLEAR_SAFE_INTERFACE
        global LAST_CLEAR_SAFE_ERR
        global LAST_CLEAR_SAFE_SYS
        global CACHE_PERF_DICT
        global CACHE_IF_DICT
        global CACHE_ERR_DICT

        # Cache the IF stats
        device_obj.linux_mode()

        if_stats = device_obj.run_command("vpp_get_stats dump /if")
        LAST_CLEAR_SAFE_INTERFACE = datetime.now()
        CACHE_IF_DICT = safe_vpp.parse_vpp_if_stats(if_stats)

        perf_stats = device_obj.run_command("vpp_get_stats dump /sys")
        LAST_CLEAR_SAFE_SYS = datetime.now()
        CACHE_PERF_DICT = safe_vpp.parse_vpp_sys(perf_stats)

        err_cmd_out = device_obj.run_command("vpp_get_stats dump /err")
        LAST_CLEAR_SAFE_ERR = datetime.now()
        CACHE_ERR_DICT = safe_vpp.parse_vpp_err(err_cmd_out)
        device_obj.cli_mode()
    

    def clear_counters(self, device_obj, counters='all'):
        """Method to clear the counters of the VPP instance

        :param device_object device_obj: Device object of device under test
        :param str counters: Identify which counters to clear

        :rtype: None
        """
        global LAST_CLEAR_INTERFACE
        global LAST_CLEAR_ERR
        device_obj.linux_mode()

        if counters == 'all':
            device_obj.run_command("vppctl clear run")
            LAST_CLEAR_INTERFACE = datetime.now()
            device_obj.run_command("vppctl clear interfaces")
            LAST_CLEAR_ERR = datetime.now()
            device_obj.run_command("vppctl clear errors")
        elif counters == 'run':
            device_obj.run_command("vppctl clear run")
        elif counters == 'interfaces':
            LAST_CLEAR_INTERFACE = datetime.now()
            device_obj.run_command("vppctl clear interfaces")
        elif counters == 'errors':
            LAST_CLEAR_ERR = datetime.now()
            device_obj.run_command("vppctl clear errors")

        device_obj.cli_mode()

    def clear_safe_counters(self, device_obj):
        """Method to clear the counters of the VPP instance

        :param device_object device_obj: Device object of device under test
        :param str counters: Identify which counters to clear

        :rtype: None
        """
        # Cache VPP stats
        self.cache_vpp_stats(device_obj)


    def clear_hist(self, device_obj):
        """Method to clear the VPP histogram counters.  This method will also
        capture the TOD of that the clear was executed

        :param device_object device_obj: Device object of device under test

        :rtype: None
        """
        device_obj.linux_mode()
        self.last_hist_clear_tod = datetime.now()
        device_obj.run_command("vppctl clear histogram")
        device_obj.cli_mode()

    def run_interactive_mode(self, device_obj):
        """Method to run the script in interactive mode.  User can run
        various commands

        :param device_object device_obj: Device Object of device under test

        :rtype: None
        """
        while True:

            if self.redirect:
                sys.stdout = VPP_INT_OBJ.orig_stdout
                VPP_INT_OBJ.fopen.close()

            in_val = input('Enter command :')
            if in_val == 'h':
                self.print_menu()
            if in_val == 'c':
                self.clear_counters(device_obj)
            if in_val == 'cs':
                self.clear_safe_counters(device_obj)
            if in_val == 'cr':
                self.clear_counters(device_obj, 'run')
            if in_val == 'ci':
                self.clear_counters(device_obj, 'interfaces')
            if in_val == 'ce':
                self.clear_counters(device_obj, 'errors')
            if in_val == 'ch':
                self.clear_hist(device_obj)
            if in_val == 'q':
                self.fptr.close()
                device_obj.logout()
                break
            if in_val == 'd':
                self.print_all(device_obj)
            if in_val == 's':

                if self.redirect:
                    VPP_INT_OBJ.fopen = open(VPP_INT_OBJ.print_fname, 'w')
                    sys.stdout = VPP_INT_OBJ.fopen
                    
                self.print_all_safe(device_obj)
            if in_val == 'ss':
                self.collect_smgr(device_obj)

    def get_pkt_flow_stats(self, device_obj, num_workers):
        """Method to print out the packet flow stats

        :param device_object device_obj: Device object of device under test
        :param int num_workers: Number of VPP workers

        :rtype: None
        """

        # Jump into Linux mode
        device_obj.linux_mode()

        # Run the show run command with a number of nodes to look for
        response = device_obj.run_command("vppctl show run | grep 'dpdk-input\|fastpath-handoff\|executive\|Time'")
        pkt_path_dict, time_window = self.vpp_pkt_path(response)

        # Print Header
        print('Packet Flow by Thread')
        print('**Time Window {0:12.2f} Seconds'.format(time_window))
        print('Thread :  Input Pkts:  Input Per  :  PPS  :    HH Per     :  Conduit per')

        # Loop through all VPP worker threads
        for th_idx in range(num_workers):

            # Compute the percentage of incoming packets per worker
            th_pkts = 0
            if th_idx in pkt_path_dict.keys() and 'pkts' in pkt_path_dict[th_idx].keys() and 'tot_pkts' in pkt_path_dict.keys():
                th_pkts = 100.0 * (float(pkt_path_dict[th_idx]['pkts'])/float(pkt_path_dict['tot_pkts']))

            # Compute the percentage of Hash and Handoff packets of what is coming
            # into each VPP worker thread
            hh_pkts = 0
            if th_idx in pkt_path_dict.keys() and 'hh' in pkt_path_dict[th_idx].keys() and 'pkts' in pkt_path_dict[th_idx].keys():
                hh_pkts = 100.0*(float(pkt_path_dict[th_idx]['hh'])/float(pkt_path_dict[th_idx]['pkts']))

            # Compute the percentage of packets going through the conduit
            cond_pkts = 0
            if th_idx in pkt_path_dict.keys() and 'conduit' in pkt_path_dict[th_idx].keys() and 'tot_pkts' in pkt_path_dict.keys():
                cond_pkts = 100.0*(float(pkt_path_dict[th_idx]['conduit'])/float(pkt_path_dict['tot_pkts']))

            print('{0}     {1:12,}    {2:8.2f}%     {3:5.2f}  {4:8.2f}%       {5:8.2f}%'.format(th_idx,
                                                                                                pkt_path_dict[th_idx]['pkts'],
                                                                                                th_pkts,
                                                                                                float(pkt_path_dict[th_idx]['pkts'])/time_window,
                                                                                                hh_pkts, cond_pkts))

        if 'tot_hh' in pkt_path_dict.keys() and 'tot_pkts' in pkt_path_dict.keys():
            print('Percentage HH:{0}'.format(100.0 * (float(pkt_path_dict['tot_hh'])/float(pkt_path_dict['tot_pkts']))))


    def get_num_smgrs(self, device_obj):
        """Method to get the number of SMGR instances that are running in
        the active role.  This method will print out the number of smgrs

        :param device_object device_obj: Device object of device under test

        :rtype: None
        """

        # Get the number of SMGR applications
        ##num_smgrs = device_obj.cli_obj.get_instances_for_facility('sessmgr')
        cmd_out = device_obj.run_command('show task resources facility sessmgr all')
        resources = parse_show_task_resources(cmd_out)

        instance_list = []
        for slot in resources:
            if not isinstance(slot, int):
                continue
            instance_list += get_per_cpu_facility_instances(resources[slot], 'sessmgr')

        print('Number of SMGRs: {0}'.format(len(instance_list)))


    def process_num_threads(self, device_obj):
        """Method to determine the number of VPP worker threads

        :param device_object device_obj: Device object of the device under test

        :return: Number of VPP worker threads
        :rtype: int
        """
        vpp_workers = 0
        vpp_thread = device_obj.cli_obj.vpp_misc_parser.verify_cli("show threads", get_parsed_output=True)
        for _, thread_dict in vpp_thread.items():
            if 'Name' in thread_dict.keys() and 'vpp_wk' in thread_dict['Name']:
                vpp_workers += 1
        print('VPP has {} workers'.format(vpp_workers))
        return vpp_workers


    def process_interface_data(self, device_obj):
        """Method to deterine the number of ports and the allocation of Rx
        queues.  The method will make use of the VPP show interface cmd

        :rtype: None
        """

        res_int = device_obj.cli_obj.vpp_show_interface.verify_cli('show interface', get_parsed_output=True)

        self.get_interface_errors(res_int)
        avg_pkt_size_dict = self.intf_avg_pkt_size(res_int)

        print('**** Average Packet Size   Taken from show interface packet/byte counters ****')
        print(' Interface Name                  Rcv Avg. Pkt Size    Tx Avg. Pkt Size')
        for int_name, avg_dict in avg_pkt_size_dict.items():
            if 'rx_size' in avg_dict.keys() and 'tx_size' in avg_dict.keys():
                print('{0:34}  {1:7.2f} bytes      {2:7.2f} bytes'.format(int_name,
                                                                          avg_dict['rx_size'],
                                                                          avg_dict['tx_size']))

        # Determine the number of Ports and the number of Rx queues
        rx_place_dict = device_obj.cli_obj.vpp_show_interface.verify_cli('show interface rx-placement', get_parsed_output=True)
        # Determine the number of Ports
        known_ports = dict()
        for _, thread_dict in rx_place_dict.items():
            for _, vpp_wrk_dict in thread_dict.items():
                for int_name, _ in vpp_wrk_dict['node']['dpdk-input'].items():
                    # Walk the keys to determine the ports
                    if int_name not in known_ports.keys():
                        known_ports[int_name] = 1
                    else:
                        known_ports[int_name] += 1

        print('Number of ports: {0}'.format(len(known_ports.keys())))
        for int_name, num_queues in known_ports.items():
            print('Interface {0} num Rx Queues:{1}'.format(int_name, num_queues))


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description="parser")

    # Get input files.  This is a list
    PARSER.add_argument('-f', '--file', nargs='+',
                        dest='yaml_file',
                        help='List of Device YAML file(s)',
                        action='store',
                        required=True)

    # Add optional interactive mode
    PARSER.add_argument('--inter', help='Run Interactive', action="store_true")

    # Operator can identify collection type
    PARSER.add_argument('-t, --type', dest='type_val',
                        help='Type of collection', action="store")

    # Operator can identify collection type
    PARSER.add_argument('--redirect',
                        help='Ridirect STD out to file', action="store_true")

    PARSER.add_argument('-v', '--vz', nargs='+',
                        dest='vz_test',
                        help='<slot> <cpu> <command> <seconds>',
                        action='store')
     # do the parsing
    ARGS = PARSER.parse_args()

    if ARGS.vz_test:
        VPP_INT_OBJ = VppInterogate()
        DEV_OBJ = VPP_INT_OBJ.connect_device(ARGS.yaml_file[0])



        ##slot = ARGS.vz_test[0]
        ##cpu = ARGS.vz_test[1]

        ##cmd = ''
        ##for word_item in ARGS.vz_test[2:-1]:
           ##  cmd += word_item + ' '
        ##cmd.lstrip()

        sleep_time = ARGS.vz_test[0]
        DEV_OBJ.linux_mode()
        ##DEV_OBJ.tel_card_cpu(slot,cpu)

        while(1):
            print(datetime.now())
            cmd_out = DEV_OBJ.run_command('cli vppctl \\\"show ip6-reas\\\" | grep Current')
            print(cmd_out)
            cmd_out = DEV_OBJ.run_command('cli vppctl \\\"show error\\\" | egrep "Card|reas"')
            print(cmd_out)
            ##cmd_out = DEV_OBJ.run_command(cmd)
            print(cmd_out)
            time.sleep(int(sleep_time))

        sys.exit()
        

    # Check if user adds type of collection
    col_type = None
    if ARGS.type_val:
        if ARGS.type_val == 'tmo1':
            col_type = 'tmo1'
        else:
            print('Unknown type value: {0}'.format(ARGS.type_val))
            print('Valid values are:(0)'.format('tmo1'))
            sys.exit()


    # Create the VPP object and connect to the first device
    # in the yaml_file arg param
    VPP_INT_OBJ = VppInterogate()
    DEV_OBJ = VPP_INT_OBJ.connect_device(ARGS.yaml_file[0])

    # Check if the user wants to redirect print output to file
    if ARGS.redirect:
        VPP_INT_OBJ.redirect = True
        VPP_INT_OBJ.orig_stdout = sys.stdout
        VPP_INT_OBJ.print_fname = './vpp_col.out'
        VPP_INT_OBJ.fopen = open(VPP_INT_OBJ.print_fname, 'w')
        sys.stdout = VPP_INT_OBJ.fopen

    if ARGS.inter:
        if len(ARGS.yaml_file) != 1:
            print('Error: User identifed multiple devices in interactive mode)')
            sys.exit(1)

        VPP_INT_OBJ.run_interactive_mode(DEV_OBJ)

    else:

        if col_type == 'tmo1':
            VPP_INT_OBJ.print_all_safe(DEV_OBJ)
            time.sleep(2)
            VPP_INT_OBJ.clear_safe_counters(DEV_OBJ)
            VPP_INT_OBJ.clear_hist()
            time.sleep(10)
            VPP_INT_OBJ.print_all_safe(DEV_OBJ)
        else:
            VPP_INT_OBJ.print_all_safe(DEV_OBJ)

        VPP_INT_OBJ.conn_obj.logout()

        if len(ARGS.yaml_file) > 1:
            for yaml_fn in ARGS.yaml_file[1:]:

                VPP_INT_OBJ = VppInterogate()
                DEV_OBJ = VPP_INT_OBJ.connect_device(yaml_fn)

                if col_type == 'tmo1':
                    VPP_INT_OBJ.print_all_safe(DEV_OBJ)
                    time.sleep(2)
                    VPP_INT_OBJ.clear_safe_counters(DEV_OBJ)
                    VPP_INT_OBJ.clear_hist()
                    time.sleep(10)
                    VPP_INT_OBJ.print_all_safe(DEV_OBJ)
                else:
                    VPP_INT_OBJ.print_all_safe(DEV_OBJ)

                VPP_INT_OBJ.conn_obj.logout()

    if ARGS.redirect:
        sys.stdout = VPP_INT_OBJ.orig_stdout
        VPP_INT_OBJ.fopen.close()
