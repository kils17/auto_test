"""Module containing a number of methods to parse the VPP safe commands.
Currently there is a total of 3 VPP commands that can be run from
the Linux prompt.  These commands make use of the shared memory
mechanism and will not disrupt VPP by grabing the barrier sync flag.
"""
import re
import argparse
import logging
import gen_const as gen_const

# pylint: disable=line-too-long

logger = logging.getLogger(__name__)


def update_if_stats_dict(if_dict, res_dict, if_num, worker_id, num_pkts, counter, bytes_flg=False, num_bytes="0"):
    """This method will be given the interface & result dictionaries.  The
    method will use the interface dictionary to determine interface index
    to the actual interface name.  The results dictionary is passed in and
    this method will update this dictionary.  The res_dict dictionary will
    be updated within the method.

    :param dict if_dict: Interface dictionary   mapping between IF index to name
    :param dict res_dict: Results dictionary.  Method will update this dictionary
    :param str if_num: Interface ID/Number in string form
    :param str worker_id: VPP worker ID
    :param str num_pkts: Number of packets for the given counter
    :param str num_pkts: The number of packets for the given entry
    :param bool bytes_flg: Flag to determine if there is a bytes value in the record
    :param str num_bytes: The number of bytes in ther record

    :return: None
    """

    # Get the Interface Name from IF dictionary
    if_name = if_dict[if_num]

    # Create the dictionary if needed
    if if_name not in res_dict.keys():
        res_dict[if_name] = dict()

    # Get the counter name
    cntr_name = counter.split('/')[-1].strip()

    # Create counter dict if needed
    if cntr_name not in res_dict[if_name].keys():
        res_dict[if_name][cntr_name] = dict()

    # Add the counter to the dict
    res_dict[if_name][cntr_name][worker_id] = dict()
    res_dict[if_name][cntr_name][worker_id]['pkts'] = int(num_pkts)
    if bytes_flg:
        res_dict[if_name][cntr_name][worker_id]['bytes'] = int(num_bytes)

    # Determine the total counter for all VPP worker threads
    if 'tot_pkts' not in res_dict[if_name][cntr_name].keys():
        res_dict[if_name][cntr_name]['tot_pkts'] = 0
    res_dict[if_name][cntr_name]['tot_pkts'] += int(num_pkts)

    if bytes_flg:
        if 'tot_bytes' not in res_dict[if_name][cntr_name].keys():
            res_dict[if_name][cntr_name]['tot_bytes'] = 0
        res_dict[if_name][cntr_name]['tot_bytes'] += int(num_bytes)

def parse_vpp_if_stats(cmd_out):
    """This method be given the multi line string from the Linux cmd
    vpp_get_stats dump /if       display interface counters
    This method will create a dictionary with all the output values
    and pass this back to the caller.

    :param str cmd_out: Ouput of vpp_get_stats dump /if command

    :return: Dictionary containing information from the VPP command
    :rtype: dict
    """

    # Creat if-dict & Results dictionary
    if_dict = dict()
    res_dict = dict()

    # Loop through the output line by line
    for line in cmd_out.splitlines():

        # First check for the interface name section
        match = re.search(r'\[(\d+)]: (\S+) /if/names', line)
        if match:
            if_dict[match.group(1)] = match.group(2)
            continue

        # Check for all other lines.  The format is:
        # [IF @ WT]: X packets COUNTER
        match = re.search(r'\[(\d+) @ (\d+)]: (\d+) packets (\S+)', line)
        if match:
            update_if_stats_dict(if_dict, res_dict, match.group(1), match.group(2),
                                 match.group(3), match.group(4))

            continue

        match = re.search(r'\[(\d+) @ (\d+)]: (\d+) packets, (\d+) bytes (\S+)', line)
        if match:
            update_if_stats_dict(if_dict, res_dict, match.group(1), match.group(2),
                                 match.group(3), match.group(5), True, match.group(4))
            continue
        print('Error:  line {} not parsed'.format(line))

    return res_dict

def parse_vpp_sys(cmd_out):
    """This method be given the multi line string from the Linux cmd
    vpp_get_stats dump /sys       display sys counters
    This method will create a dictionary with all the output values
    and pass this back to the caller.

    :param str cmd_out: Ouput of vpp_get_stats dump /err command

    :return: Dictionary containing information from the VPP command
    :rtype: dict
    """

    # Creat node_id_dict
    node_id_dict = dict()
    ret_dict = dict()

    # Global counters contained in the CLI output
    glbl_sys_cntrs = ['vector_rate', 'input_rate', 'last_update', 'last_stats_clear', 'heartbeat']

    # First get the Node Ids.  This information is used to generate the results
    # dictionary.  The node IDs occur at the end of the output
    for line in cmd_out.splitlines():

        # First check for the interface name section
        match = re.search(r'\[(\d+)]: (\S+) /sys/node/names', line)
        if match:
            node_id_dict[match.group(1)] = match.group(2)
            continue

    # Now go through and process the other items, line by line
    for line in cmd_out.splitlines():

        # Skip over any node name entries.  Process in the loop above
        if re.search(r'\[(\d+)]: (\S+) /sys/node/names', line):
            continue

        # The following check will identify the lines where the output has the format:
        # [If_idx @ VPP_wt]: num_packets packets /sys/node/XX
        match = re.search(r'\[(\d+) @ (\d+)]: (\d+) packets /sys/node/(\S+)', line)
        if match:
            # Check if the node index is valid
            if match.group(1) not in node_id_dict.keys():
                ## DJP print('Error: node Id {} is not valid'.format(match.group(1)))
                continue

            # Get the node name
            node_name = node_id_dict[match.group(1)]

            # Check if the node name is a dictionary
            if node_name not in ret_dict.keys():
                ret_dict[node_name] = dict()

            # Check if the node name has the sys item
            if match.group(4) not in ret_dict[node_name].keys():
                ret_dict[node_name][match.group(4)] = dict()
            sys_dict = ret_dict[node_name][match.group(4)]

            # Add the worker thread ID if needed
            if match.group(2) not in sys_dict.keys():
                sys_dict[match.group(2)] = dict()
            sys_dict[match.group(2)] = int(match.group(3))

            if 'tot_pkts' not in sys_dict.keys():
                sys_dict['tot_pkts'] = 0
            sys_dict['tot_pkts'] += int(match.group(3))
            continue
        # Check for various system counters
        match = re.search(r'(\d+\.\d+) /sys/([a-zA-Z_]+)', line)
        if match:
            if match.group(2) in glbl_sys_cntrs:
                ret_dict[match.group(2)] = float(match.group(1))
                continue
        print('Error unknown line {}'.format(line))

    return ret_dict

def print_vpp_errors(err_dict, cache_err_dict=None, cache_tod=None):
    '''Method to print out any known critical & frag VPP errros.  The
    caller can send a cached content of the VPP errors in a dict.

    Returned Error dictionary has the following format
    {Error_node:{error_str:{worker_thread:number_of_packets}}}

    :param dict err_dict: Error dictionary created from the error CLI output
    :param dict cache_err_dict: Cached error dictionary taken earlier

    :return: None
    '''

    # Create the header line format.  This will only be printed if
    # there is 1 line of output
    header_line = '{0:<28s} {1:20s} {2:20s}'.format('Node Name',
                                                    'Error Str',
                                                    'Number of Pkts')
    hdr_printed = False  # Header printed flag

    # Get the critical & Fragmentation error lists
    crit_err_list = gen_const.VPPCriticalErrors.VPP_CRITICAL_ERRORS.val
    frag_err_list = gen_const.VPPCriticalErrors.VPP_FRAGMENTATION_ERRORS.val

    # Walk the dictionary and print out any critical errors
    for node_name, err_string_dict in err_dict.items():
        for err_string in err_string_dict.keys():

            # Check if the error string is one of the critical ones
            if err_string in crit_err_list:
                # Check that the value is non-zero
                if err_string_dict[err_string]['tot_pkts']:
                    if not hdr_printed:
                        hdr_printed = True
                        print(header_line)

                    # Was there a clear, which will have a cached error dict
                    if cache_err_dict:
                        try:
                            tot_pkts = err_string_dict[err_string]['tot_pkts'] - \
                                cache_err_dict[node_name][err_string]['tot_pkts']
                        except KeyError:
                            tot_pkts = err_string_dict[err_string]['tot_pkts']
                    else:
                        tot_pkts = err_string_dict[err_string]['tot_pkts']

                    # Print those errors that are non-zero
                    if tot_pkts:
                        print('{0:<24s} {1:<24s} {2:12,d}'.format(node_name,
                                                                  err_string,
                                                                  tot_pkts))
            elif err_string in frag_err_list:
                if err_string_dict[err_string]['tot_pkts']:
                    if not hdr_printed:
                        hdr_printed = True
                        print(header_line)

                    if cache_err_dict:
                        try:
                            tot_pkts = err_string_dict[err_string]['tot_pkts'] - \
                                cache_err_dict[node_name][err_string]['tot_pkts']
                        except KeyError:
                            tot_pkts = err_string_dict[err_string]['tot_pkts']
                    else:
                        tot_pkts = err_string_dict[err_string]['tot_pkts']

                    # Only print errors that are non-zero
                    if tot_pkts:
                        print('{0:<24s} {1:<24s} {2:12,d}'.format(node_name,
                                                                  err_string,
                                                                  tot_pkts))

def parse_vpp_err(cmd_out):
    """This method be given the multi line string from the Linux cmd
    vpp_get_stats dump /err       display VPP errors
    This method will create a dictionary with all the output values
    and pass this back to the caller.

    :param str cmd_out: Ouput of vpp_get_stats dump /err command

    :return: Dictionary containing information from the VPP command
    :rtype: dict
    """

    # Creat node_id_dict
    ret_dict = dict()

    # First get the Node Ids
    for line in cmd_out.splitlines():

        # First check for the interface name section
        match = re.search(r'\[@(\d+)] (\d+) /err/(.*)/(.*)', line)
        if match:
            # Add the node name
            if match.group(3) not in ret_dict.keys():
                ret_dict[match.group(3)] = dict()

            # Add the reason
            if match.group(4) not in ret_dict[match.group(3)].keys():
                ret_dict[match.group(3)][match.group(4)] = dict()

            # Create an entry in the dictionary
            ret_dict[match.group(3)][match.group(4)][match.group(1)] = int(match.group(2))

            # Compuate the total packets.  The output has counters per VPP worker thread
            # This block will aggregate the error count across all VPP worker threads
            if 'tot_pkts' not in ret_dict[match.group(3)][match.group(4)].keys():
                ret_dict[match.group(3)][match.group(4)]['tot_pkts'] = 0
            ret_dict[match.group(3)][match.group(4)]['tot_pkts'] += int(match.group(2))
            continue
        print('Error unknown line {}'.format(line))

    return ret_dict

def print_avg_pkt_size(if_dict, cache_if_dict):
    '''Method to compute and print out the average packet sizes.  This method
    will be given the dictionary created from the vpp_get_stats dump /if output.
    The dictionary will have packet & byte counters per interface.  This
    method will take this data and compute the average packet size and output
    this data to the user.

    :param dict if_dict: Interface dictionary

    :return: None
    :rtype: dict
    '''

    # Print out a header for this section
    print('\n**** Average Packet Size   Computed using interface counters ****')

    # Create the header line
    header_line = '{0:36s} {1:20s} {2:20s}'.format(' Interface Name',
                                                   'Rcv avg. Pkt Size',
                                                   'Tx Avg. Pkt Size')
    hdr_printed = False    # Header printed flag

    # Loop through the interfaces
    for if_name in if_dict.keys():

        # Set the interface name printed flag to False
        rx_avg = tx_avg = 0

        # Check if the interface has Rx & Tx packets
        if if_dict[if_name]['rx']['tot_pkts']:
            rx_avg = round(if_dict[if_name]['rx']['tot_bytes']/if_dict[if_name]['rx']['tot_pkts'])
        if if_dict[if_name]['tx']['tot_pkts']:
            tx_avg = round(if_dict[if_name]['tx']['tot_bytes']/if_dict[if_name]['tx']['tot_pkts'])

        if not hdr_printed:
            print(header_line)
            hdr_printed = True
        # Print the rx and tx average packet sizes
        print('{0:36s} {1:16d} {2:18d}'.format(if_name, rx_avg, tx_avg))

def get_agg_pkts(perf_dict, node_list):
    '''Method to look for specific node counters

    :param dict perf_dict: Dictionary
    :param list node_list: Node list strings to catch agg counters

    return: List with the aggregated packet counters for the nodes
    :rtype: list
    '''

    # init the node list
    ret_list = list()
    idx = 0

    # Loop through the list of nodes
    for node_id in node_list:

        if node_id in node_list:
            if 'vectors' in perf_dict[node_id].keys():
                if 'tot_pkts' in perf_dict[node_id]['vectors'].keys():
                    ret_list.append(perf_dict[node_id]['vectors']['tot_pkts'])
                    fptr = open('/tmp/dd','w')
                    fptr.write('DJP {0}'.format(perf_dict))
                    fptr.close()
                    



        idx += 1
    return ret_list

def print_packet_flow(perf_dict, cache_perf_dict):
    '''Method to print out packet flow data.  Packets flow through VPP first coming
    into the dpdk-input node.  A packet may then be hashed and handoff to a different
    worker thread.  Then the mobility processing, or conduit processing will happen
    across the VPP worker threads.  This method prints this information to the user
    to provide some insight into how packets are traversing VPP.

    :param dict perf_dict: Performance dictionary.  Created from the /sys output

    :return: None
    '''

    # Print header for this section
    print('\n**** Packet Flow by Thread ****')

    # Create the header string, which will be printed out if any data needs to be printed
    header_line = '{0:8s} {1:>22s} {2:>10s} {3:>9s} {4:>9s} {5:>12s}'.format('Thread',
                                                                             'Input Pkts',
                                                                             'Input',
                                                                             'PPS',
                                                                             'HH',
                                                                             'Conduit')

    header_line2 = '{0:>42s} {0:>20s} {0:>10s}'.format('Perc')
    hdr_printed = False

    # The following Node names are used to determine packet flow
    # dpdk-input   This is the input node when packets come in from DPDK
    # fastpath-handoff-exec  Hash and handoff node
    # fastpath-executive  Conduit packet processing

    # Init node worker thread lists
    dpdk_wt_list = list(perf_dict['dpdk-input']['vectors'].keys())
    dpdk_wt_list.sort()

    # Get the time window the data represents
    time_window = perf_dict['last_update']
    print('**Time Window    {} Seconds'.format(time_window))

    # Print string format for the data
    format_str = '{0:8s} {1:24,} {2:8.2f}% {3:10.2f} {4:>8.2f}% {5:8.2f}%'

    # Print the output up to the largest worker thread ID
    for wt_id in dpdk_wt_list:
        thread_pkts = perf_dict['dpdk-input']['vectors'][wt_id]

        # Compute the percentage of packets per worker thread for the dpdk-input node
        if perf_dict['dpdk-input']['vectors']['tot_pkts']:
            percentage_pkts = 100.0 * (float(thread_pkts)/float(perf_dict['dpdk-input']['vectors']['tot_pkts']))
        else:
            percentage_pkts = 0.0

        # Compute how many of incoming packets per worker thread is hash and handoff
        if thread_pkts:
            hh_perc = perf_dict['fastpath-handoff-exec']['vectors'][wt_id]/thread_pkts * 100.0
        else:
            hh_perc = 0.0

        # Determine the percentage of packets entering the conduit per worker thread
        if perf_dict['fastpath-executive']['vectors']['tot_pkts']:
            fp_exec_perc = 100.0 * float(perf_dict['fastpath-executive']['vectors'][wt_id])/float(perf_dict['fastpath-executive']['vectors']['tot_pkts'])
        else:
            fp_exec_perc = 0.0

        if not hdr_printed:
            hdr_printed = True
            print(header_line)
            print(header_line2)

        # Print out a line for each worker thread
        print(format_str.format(wt_id, thread_pkts, percentage_pkts,
                                thread_pkts/time_window, hh_perc,
                                fp_exec_perc))


def print_if_errors(if_dict, cache_if_dict):
    """This method will be given the dictoinary created from the /if output.
    This method will print any and all errors/warnings from the interface
    output.  This will include rx-miss etc.

    :param dict if_dict: Interface dictionary

    :return: None
    """

    # Print out the section message
    print('\n**** Interface Errors ****')

    # Create the list of error names that will be printed
    error_names = ['drops', 'tx-error', 'rx-miss', 'rx-no-buf', 'rx-error']

    # Create the header line for the data
    header_line = '{0:36s} {1:12s} {2:12s}'.format('Interface', 'Counter', 'Packets/Miss-Perc')
    hdr_printed = False

    # Loop through the interfaces and print out some content
    for if_name in if_dict.keys():
        if_printed = False # Interface printed line

        #  Determine if the Interface is the main port, not VLAN
        intf_port_flg = (if_name.startswith('VirtualFun') or if_name.startswith('FortyGig')) and '.' not in if_name

        # Print out the number of Rx packet counters for main NIC
        # ports
        if intf_port_flg and 'rx' in if_dict[if_name].keys():
            # Print header if need be
            if not hdr_printed:
                print(header_line)
                hdr_printed = True

            # Get the previous cached value
            prev_val = 0
            if cache_if_dict:
                try:
                    prev_val = cache_if_dict[if_name]['rx']['tot_pkts']
                except KeyError:
                    prev_val = 0

            # Print the interface line if need be
            if not if_printed:
                print('{0:36s} {1:12s} {2:12}'.format(if_name,
                                                      'rx-pkts',
                                                      if_dict[if_name]['rx']['tot_pkts']-prev_val))
                if_printed = True
            else:
                print('{0:36s} {1:12s} {2:12}'.format('',
                                                      'rx-pkts',
                                                      if_dict[if_name]['rx']['tot_pkts']-prev_val))

        # Print out any error counters
        for err_name in error_names:
            if err_name in if_dict[if_name].keys():

                # Check if the error is non-zero
                if if_dict[if_name][err_name]['tot_pkts']:
                    if not hdr_printed:
                        print(header_line)
                        hdr_printed = True

                    # Subtract cached value if present
                    prev_val = 0
                    if cache_if_dict:
                        try:
                            prev_val = cache_if_dict[if_name][err_name]['tot_pkts']
                        except KeyError:
                            prev_val = 0

                    if not if_printed:
                        print('{0:36s} {1:12s} {2:12}'.format(if_name, err_name, if_dict[if_name][err_name]['tot_pkts']-prev_val))
                        if_printed = True
                    else:
                        print('{0:36s} {1:12s} {2:12}'.format('', err_name, if_dict[if_name][err_name]['tot_pkts']-prev_val))


        # Determine the percentage of loss due to Rx_miss
        # over the rx packet counter
        if (if_name.startswith('VirtualFun') or if_name.startswith('FortyGig')) and '.' not in if_name:
            if 'rx-miss' in if_dict[if_name].keys():
                # Compute number of miss percentage

                prev_miss = 0
                prev_rx_pkts = 0
                # First lets compute the previous rx-misses & total rx pkts.
                if cache_if_dict:
                    # Get previous rx-misses
                    try:
                        prev_miss = cache_if_dict[if_name]['rx-miss']['tot_pkts']
                    except KeyError:
                        pass

                    # Get previous rx packets
                    try:
                        prev_rx_pkts = cache_if_dict[if_name]['rx']['tot_pkts']
                    except KeyError:
                        pass

                # Compute the rx packet count
                rx_miss_count = int(if_dict[if_name]['rx-miss']['tot_pkts']) - int(prev_miss)
                rx_pkt_count = int(if_dict[if_name]['rx']['tot_pkts']) - int(prev_rx_pkts)

                per_miss =  rx_miss_count/(rx_miss_count + rx_pkt_count) * 100.0
                print('{0:36s} {1:12s} {2:12.6f}'.format('', 'rx-miss perc',
                                                         per_miss))




if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description="parser")

    # Add Input file to parse
    PARSER.add_argument('-f', '--file', dest='in_file',
                        help='stats output file',
                        action='store',
                        required=True)

    # do the parsing
    ARGS = PARSER.parse_args()

    # Open the input file
    FILE_FD = open(ARGS.in_file, mode='r')
    ALL_LINES = FILE_FD.read()
    FILE_FD.close()

    VPP_SYS_DICT = parse_vpp_sys(ALL_LINES)
    print_packet_flow(VPP_SYS_DICT)
    ##print(VPP_SYS_DICT)

    ###VPP_SYS_DICT = vpp_if_stats(all_lines)
    ###print_if_errors(VPP_SYS_DICT)
    ###print_avg_pkt_size(VPP_SYS_DICT)

    #VPP_SYS_DICT = vpp_sys(all_lines)
    #print_packet_flow(VPP_SYS_DICT)

    ##VPP_SYS_DICT = parse_vpp_err(all_lines)
    ##print_vpp_errors(VPP_SYS_DICT)

    ##pprint.pprint(VPP_SYS_DICT)
