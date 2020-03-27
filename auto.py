

import os
import argparse
import yaml
import connection as comms_connection
import time
import pprint


CONFDIR = 'config'
TESTDIR = 'test'
RESULTDIR = 'result'


class DeviceInterrogate:

    def __init__(self,host='',hostfile='',name=''):
        self.name = name
        self.host = host
        self.hostfile = hostfile

        self.fp =  open('{0}/{1}_{2}.txt'.format(RESULTDIR, self.name, self.host),'w')
        self.connect_device(self.hostfile)

        print ("Device {0}[{1}] connected".format(self.host, self.hostfile))


    def connect_device(self, yaml_file):
        """Method to connect to a device given a YAML file.  This method will
        attempt to connect to the 1 or the first device int YAML file.  This is
        a quick way of connecting.

        :param str yaml_file: Name of yaml file for the device one wants to connect

        :return: Return the device object if connected
        :rtype: dev_object
        """

        # Get the full path of the testbed yaml file.  Then create the device
        cwd = os.getcwd()

        yaml_filename = yaml_file
        try:
            with open('{0}/{1}'.format(CONFDIR, yaml_filename), 'r') as file:
                self.yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
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
        #conn_object = comms_connection.VPCConnection(conn_info_dict)
        conn_object = comms_connection.LinuxDeviceConnection(conn_info_dict)

        conn_object.login()
        self.chassis_prompt = conn_object.cli_prompt
        #conn_object.enable_priv_mode()

        self.conn_obj = conn_object

        return conn_object




DEV_OBJS = []

def connect_device(testname, host):
    global DEV_OBJ

    dev_obj = DeviceInterrogate(name=testname, host=host.get('host'), hostfile=host.get('hostfile'))
    DEV_OBJS.append(dev_obj)


def stop_test():
    global DEV_OBJS

    for id in range(len(DEV_OBJS)):
        DEV_OBJS[id].fp.close()

    # stop monpro threads
    DEV_OBJS[0].conn_obj.stop_mon_command()


def get_dev_obj(host):
    global DEV_OBJS

    id = 0
    for id in range(len(DEV_OBJS)):
        if DEV_OBJS[id].host == host:
            return DEV_OBJS[id]

    return None
        


def do_more(res, dev_obj):
    callids = []

    # extract the callids
    for line in (res.split('\n')):
        words = " ".join(line.split()).split(" ")
        if len(words[0]) > 0:
            if words[0][0] == 'y':
                callids.append(words[1])


    # run additional command
    for callid in callids:
        dev_obj.conn_obj.run_command('show subs user-plane-only full callid {0}'.format(callid), write_fp=dev_obj.fp)
        dev_obj.conn_obj.run_command('show subs user-plane-only callid {0} pdr full all'.format(callid), write_fp=dev_obj.fp)
        dev_obj.conn_obj.run_command('show subs user-plane-only callid {0} far full all'.format(callid), write_fp=dev_obj.fp)
        dev_obj.conn_obj.run_command('show subs user-plane-only callid {0} qer full all'.format(callid), write_fp=dev_obj.fp)
        dev_obj.conn_obj.run_command('show subs user-plane-only callid {0} urr full all'.format(callid), write_fp=dev_obj.fp)


def do_ping(proc, dev_obj):
    up_dev = get_dev_obj('up_cli')
    res = up_dev.conn_obj.run_command("show subs imsi {0}".format(proc.get('imsi')))

    destips = []
    
    # extract the destips
    for line in (res.split('\n')):
        words = " ".join(line.split()).split(" ")
        if len(words[0]) > 0:
            if words[0][0] == 'y':
                destips.append(words[4])


    # run ping command
    for destip  in destips:
        cmd = "{0} {1}".format(proc.get('cmd'), destip)
        print("PING: ", cmd)
        dev_obj.conn_obj.ping_command(cmd, write_fp=dev_obj.fp)



def run_test(testfile):
    global DEV_OBJS

    testitem = {}

    with open('{0}/{1}'.format(TESTDIR, testfile), 'r') as f:
        testitem = yaml.load(f, Loader=yaml.FullLoader)

    print("[ Test Begin:", testfile, "]")
 
    DEV_OBJS.clear()

    ############################################################################
    # read description
    ############################################################################
    testname = testitem.get('test_description')[0].get('name')


    ############################################################################
    # do preparation
    ############################################################################
    for host in testitem.get('test_prepartion'):
        connect_device(testname, host)

    print("Total:", len(DEV_OBJS))


    ############################################################################
    # do procedure
    ############################################################################

    for proc in testitem.get('test_procedure'):
        print("host: ", proc)
        dev_obj = get_dev_obj(proc.get('host'))


        for loop in range(proc.get('loop')):
            if proc.get('proc_type') == 'show_cli':
               res =  dev_obj.conn_obj.run_command(proc.get('cmd'), write_fp=dev_obj.fp)
               if proc.get('more') == True:
                   # show subs user-plane-only command with callid
                   do_more(res,  dev_obj) 
    
            elif proc.get('proc_type') == 'sim_cli':
                dev_obj.conn_obj.run_command(proc.get('cmd'), write_fp=dev_obj.fp)
            elif proc.get('proc_type') == 'sim_ctl':
                dev_obj.conn_obj.run_control(proc.get('cmd'), write_fp=dev_obj.fp)
            elif proc.get('proc_type') == 'gx_cli':
                dev_obj.conn_obj.run_command(proc.get('cmd'), write_fp=dev_obj.fp)
            elif proc.get('proc_type') == 'mon_pro':
                dev_obj.conn_obj.mon_command(proc.get('cmd'), write_fp=dev_obj.fp, option=proc.get('option'))
            elif proc.get('proc_type') == 'ping_cli':
                do_ping(proc, dev_obj)

            time.sleep(proc.get('wait'))
    






def do_test(ARGS):
    testlist = {}

    with open(ARGS.yaml_file[0], 'r') as f:
        testlist = yaml.load(f, Loader=yaml.FullLoader)

    pprint.pprint(testlist)

    print("# of item: ", len(testlist['test_list']))

    for i in range(len(testlist['test_list'])):

        print("[ Test Begin: Waiting for 3 sec ]")
        time.sleep(3)

        # start test
        run_test(testlist['test_list'][i])

        # stop test
        stop_test()

        print("[ Test End: wait for 5 sec ]")
        time.sleep(5)



if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description="parser")

    # Get input files.  This is a list
    PARSER.add_argument('-f', '--file', nargs='+',
                        dest='yaml_file',
                        help='List of Device YAML file(s)',
                        action='store',
                        required=True)


    # do the parsing
    ARGS = PARSER.parse_args()


    # start test!
    do_test(ARGS)


