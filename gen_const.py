"""Constants imported via several classes
"""

from enum import Enum, unique, IntEnum
import itertools

# Many tables in this file have bad-whitespace per pylint, but the tables are easier to read in the nicely
# tabulated form, so, overridding.
# pylint: disable=locally-disabled, bad-whitespace

@unique
class TestDef(Enum):
    """
        Deprecated: enum for test defines
    """
    ExampleTest    = ('0',   0, 'Not Currently Used')
    MpingTest      = ('1',   1, 'Single MPING')
    MpingCard      = ('2',   2, 'MPING')
    ARADPCISchan   = ('3',   3, 'PCI SChan')
    ARADBIST       = ('4',   4, 'BIST DRAM')
    ARADDDF2PRBS   = ('5',   5, 'ARAD DDF2 PRBS')
    TCAMDDF2PRBS   = ('6',   6, 'TCAM DDF2 PRBS')
    PingCard       = ('7',   7, 'PING')
    PingCardCP0    = ('8',   8, 'PING CP0')
    PingCardCP1    = ('9',   9, 'PING CP1')
    ARADFabricPRBS = ('10', 10, 'ARAD Fabric PRBS')
    ARADMDFPRBS    = ('11', 11, 'ARAD MDF PRBS')
    NPUBIST        = ('12', 12, 'BIST DRAM')

    def __init__(self, str_num, int_num, test_name):
        self.str_num = str_num
        self.int_num = int_num
        self.test_name = test_name

@unique
class ChassisTypes(Enum):
    """
    Enum of support chassis.
    """
    ASR5500 = 'ASR5500'
    ASR5000 = 'ASR5000'
    ASR5700 = 'ASR5700'
    VPC_DI  = 'VPC_DI'
    VPC_SI  = 'VPC_SI'
    IXIA    = 'ixia'
    STAROS  = 'starosdevice'
    UBUNTU  = 'ubuntudevice'
    REDHAT  = 'redhatdevice'
    VMWARE  = 'vmwaredevice'
    NEXUS   = 'nexusdevice'
    ASR9K   = 'asr9kdevice'
    CSR1K   = 'csr1kdevice'

    def __init__(self, chassis_type):
        self.val = chassis_type

@unique
class IxiaProtocols(Enum):
    """
    Enum of support Ixia Protocols.
    """
    TCP = 'tcp'
    UDP = 'udp'
    ICMP = 'icmp'
    BGP = 'bgp'
    OSPF = 'ospf'

    def __init__(self, proto):
        self.val = proto

@unique
class IxiaParameters(Enum):
    """
    Enum of support Ixia Protocols Parameters.
    """
    ICMP_TYPE = 'icmp_type'
    ICMP_CODE = 'icmp_code'
    ICMP_ID = 'icmp_id'
    ICMP_SEQ = 'icmp_seq'
    UDP_SRC_PORT = 'udp_src_port'
    UDP_DST_PORT = 'udp_dst_port'
    TCP_SRC_PORT = 'tcp_src_port'
    TCP_DST_PORT = 'tcp_dst_port'
    TCP_SEQ_NUM = 'tcp_seq_num'
    TCP_ACK_NUM = 'tcp_ack_num'
    TCP_WINDOW = 'tcp_window'
    TCP_URGENT_PTR = 'tcp_urgent_ptr'
    TCP_URG_FLAG = 'tcp_urg_flag'
    TCP_PSH_FLAG = 'tcp_psh_flag'
    TCP_SYN_FLAG = 'tcp_syn_flag'
    TCP_ACK_FLAG = 'tcp_ack_flag'
    TCP_RST_FLAG = 'tcp_rst_flag'
    TCP_FIN_FLAG = 'tcp_fin_flag'
    L4_PROTOCOL = 'l4_protocol'

    def __init__(self, proto):
        self.val = proto

TRAFFIC_PROTOCOLS_LIST = [IxiaProtocols.TCP.val, IxiaProtocols.UDP.val, IxiaProtocols.ICMP.val]
TRAFFIC_CONTROL_LIST = [IxiaProtocols.ICMP.val]
STATS_LIST = [IxiaProtocols.BGP.val]
NEIGBOUR_PROTOCOLS_LIST = [IxiaProtocols.OSPF.val, IxiaProtocols.BGP.val]
TCP_MAN_ARGS = [IxiaParameters.TCP_SRC_PORT.val, IxiaParameters.TCP_DST_PORT.val, IxiaParameters.TCP_SEQ_NUM.val,
                IxiaParameters.TCP_ACK_NUM.val, IxiaParameters.TCP_WINDOW.val, IxiaParameters.TCP_URGENT_PTR.val,
                IxiaParameters.TCP_URG_FLAG.val, IxiaParameters.TCP_PSH_FLAG.val, IxiaParameters.TCP_SYN_FLAG.val,
                IxiaParameters.TCP_ACK_FLAG.val, IxiaParameters.TCP_RST_FLAG.val, IxiaParameters.TCP_FIN_FLAG.val]

UDP_MAN_ARGS = [IxiaParameters.UDP_DST_PORT.val, IxiaParameters.UDP_SRC_PORT.val]

ICMP_MAN_ARGS = [IxiaParameters.ICMP_CODE.val, IxiaParameters.ICMP_ID.val, IxiaParameters.ICMP_SEQ.val,
                 IxiaParameters.ICMP_TYPE.val]

@unique
class IxiaNeighborParameters(Enum):
    """
    Enum of support Ixia Neighbour Parameters.
    """
    HANDLE = 'handle'
    LOCAL_IP_ADDR = 'local_ip_addr'
    REMOTE_IP_ADDR = 'remote_ip_addr'
    LOCAL_IPV6_ADDR = 'local_ipv6_addr'
    REMOTE_IPV6_ADDR = 'remote_ipv6_addr'
    LOCAL_ADDR_STEP = 'local_addr_step'
    REMOTE_ADDR_STEP = 'remote_addr_step'
    COUNT = 'count'
    MAC_ADDRESS_START = 'mac_address_start'
    NETMASK = 'netmask'
    NEIGHBOR_TYPE = 'neighbor_type'
    IP_VERSION = 'ip_version'
    NEXT_HOP_ENABLE = 'next_hop_enable'
    NEXT_HOP_IP = 'next_hop_ip'
    LOCAL_AS = 'local_as'
    LOCAL_AS_STEP = 'local_as_step'
    LOCAL_AS_MODE = 'local_as_mode'
    LOCAL_ROUTER_ID = 'local_router_id'
    VLAN_ID = 'vlan_id'
    VLAN_ID_MODE = 'vlan_id_mode'
    VLAN_ID_STEP = 'vlan_id_step'
    TCP_WINDOW_SIZE = 'tcp_window_size'
    UPDATE_INTERVAL = 'update_interval'
    UPDATES_PER_ITERATION = 'updates_per_iteration'
    RETRIES = 'retries'
    RETRY_TIME = 'retry_time'
    HOLD_TIME = 'hold_time'
    NEIGHBOR_TIME = 'neighbor_time'
    GRACEFUL_RESTART_ENABLE = 'graceful_restart_enable'
    RESTART_TIME = 'restart_time'
    STALE_TIME = 'stale_time'
    LOCAL_ROUTER_ID_ENABLE = 'local_router_id_enable'
    LOCAL_ROUTER_ID_STEP = 'local_router_id_step'
    IPV4_UNICAST_NLRI = 'ipv4_unicast_nlri'
    IPV6_MPLS_VPN_NLRI = 'ipv6_mpls_vpn_nlri'
    LOCAL_LOOPBACK_IP_ADDR = 'local_loopback_ip_addr'
    LOCAL_LOOPBACK_IP_ADDR_STEP = 'local_loopback_ip_addr_step'
    NO_WRITE = 'no_write'
    REMOTE_LOOPBACK_IP_ADDR = 'remote_loopback_ip_addr'
    REMOTE_LOOPBACK_IP_ADDR_STEP = 'remote_loopback_ip_addr_step'
    VLAN_USER_PRIORITY  = 'vlan_user_priority'
    ACTIVE_CONNECT_ENABLE = 'active_connect_enable'
    STAGGERED_START_ENABLE = 'staggered_start_enable'
    STAGGERED_START_TIME = 'staggered_start_time'
    SESSION_TYPE = 'session_type'
    MAC_ADDRESS_INIT = 'mac_address_init'
    INTF_IP_ADDR = 'intf_ip_addr'
    INTF_PREFIX_LENGTH = 'intf_prefix_length'
    NEIGHBOR_INTF_IP_ADDR = 'neighbor_intf_ip_addr'
    ROUTER_ID = 'router_id'
    AREA_ID = 'area_id'
    AREA_ID_STEP = 'area_id_step'
    AREA_TYPE = 'area_type'
    AUTHENTICATION_MODE = 'authentication_mode'
    DEAD_INTERVAL = 'dead_interval'
    HELLO_INTERVAL = 'hello_interval'
    INTERFACE_COST = 'interface_cost'
    NETWORK_TYPE = 'network_type'
    OPTION_BITS  = 'option_bits'

    def __init__(self, proto):
        self.val = proto

BGP_MAN_ARGS = [IxiaNeighborParameters.LOCAL_IP_ADDR.val, IxiaNeighborParameters.REMOTE_IP_ADDR.val,
                IxiaNeighborParameters.COUNT.val, IxiaNeighborParameters.MAC_ADDRESS_START.val,
                IxiaNeighborParameters.NETMASK.val, IxiaNeighborParameters.NEIGHBOR_TYPE.val,
                IxiaNeighborParameters.IP_VERSION.val, IxiaNeighborParameters.NEXT_HOP_ENABLE.val,
                IxiaNeighborParameters.NEXT_HOP_IP.val, IxiaNeighborParameters.LOCAL_AS.val,
                IxiaNeighborParameters.LOCAL_AS_MODE.val, IxiaNeighborParameters.TCP_WINDOW_SIZE.val,
                IxiaNeighborParameters.UPDATES_PER_ITERATION.val, IxiaNeighborParameters.RETRIES.val,
                IxiaNeighborParameters.RETRY_TIME.val, IxiaNeighborParameters.ACTIVE_CONNECT_ENABLE.val,
                IxiaNeighborParameters.STAGGERED_START_ENABLE.val, IxiaNeighborParameters.STAGGERED_START_TIME.val,
                IxiaNeighborParameters.HANDLE.val, IxiaNeighborParameters.LOCAL_IPV6_ADDR.val,
                IxiaNeighborParameters.REMOTE_IPV6_ADDR.val, IxiaNeighborParameters.LOCAL_ADDR_STEP.val,
                IxiaNeighborParameters.REMOTE_ADDR_STEP.val, IxiaNeighborParameters.LOCAL_AS_STEP.val,
                IxiaNeighborParameters.UPDATE_INTERVAL.val, IxiaNeighborParameters.LOCAL_ROUTER_ID.val,
                IxiaNeighborParameters.VLAN_ID.val, IxiaNeighborParameters.VLAN_ID_MODE.val,
                IxiaNeighborParameters.VLAN_ID_STEP.val, IxiaNeighborParameters.HOLD_TIME.val,
                IxiaNeighborParameters.GRACEFUL_RESTART_ENABLE.val, IxiaNeighborParameters.RESTART_TIME.val,
                IxiaNeighborParameters.STALE_TIME.val, IxiaNeighborParameters.RETRIES.val,
                IxiaNeighborParameters.LOCAL_ROUTER_ID_ENABLE.val, IxiaNeighborParameters.ACTIVE_CONNECT_ENABLE.val,
                IxiaNeighborParameters.MAC_ADDRESS_START.val, IxiaNeighborParameters.IPV4_UNICAST_NLRI.val,
                IxiaNeighborParameters.IPV6_MPLS_VPN_NLRI.val, IxiaNeighborParameters.LOCAL_LOOPBACK_IP_ADDR.val,
                IxiaNeighborParameters.LOCAL_LOOPBACK_IP_ADDR_STEP.val, IxiaNeighborParameters.LOCAL_ROUTER_ID_STEP.val,
                IxiaNeighborParameters.NO_WRITE.val, IxiaNeighborParameters.REMOTE_LOOPBACK_IP_ADDR.val,
                IxiaNeighborParameters.REMOTE_LOOPBACK_IP_ADDR_STEP.val, IxiaNeighborParameters.VLAN_USER_PRIORITY.val]


OSPF_MAN_ARGS = [IxiaNeighborParameters.SESSION_TYPE.val, IxiaNeighborParameters.COUNT.val,
                 IxiaNeighborParameters.MAC_ADDRESS_INIT.val, IxiaNeighborParameters.INTF_IP_ADDR.val,
                 IxiaNeighborParameters.INTF_PREFIX_LENGTH.val, IxiaNeighborParameters.NEIGHBOR_INTF_IP_ADDR.val,
                 IxiaNeighborParameters.ROUTER_ID.val, IxiaNeighborParameters.AREA_ID.val,
                 IxiaNeighborParameters.AUTHENTICATION_MODE.val, IxiaNeighborParameters.DEAD_INTERVAL.val,
                 IxiaNeighborParameters.HELLO_INTERVAL.val, IxiaNeighborParameters.INTERFACE_COST.val,
                 IxiaNeighborParameters.NETWORK_TYPE.val, IxiaNeighborParameters.OPTION_BITS.val]
@unique
class ImageTypes(Enum):
    """
    Enum for default image names.
    """
    ASR5500 = 'asr5500.bin'
    ASR5000 = 'asr5000.bin'
    VPC_DI  = 'qvpc-di.bin'
    VPC_SI  = 'qvpc-si.bin'

    def __init__(self, image_type):
        self.val = image_type

@unique
class ChassisCards(Enum):
    """
    Enum used to determine chassis type given certain card types.
    The chassis type will be determined if one of the cards exist in the show card output.
    """
    ASR5500 = (ChassisTypes.ASR5500.val, ['MIO1', 'MIO2'])
    ASR5000 = (ChassisTypes.ASR5000.val, ['SMC'])
    ASR5700 = (ChassisTypes.ASR5700.val, ['XX', 'XXX'])
    VPC_DI  = (ChassisTypes.VPC_DI.val, ['CFC'])
    VPC_SI  = (ChassisTypes.VPC_SI.val, ['VC'])

    def __init__(self, chassis_name, card_list):
        self.chassis_name = chassis_name
        self.card_list = card_list


# Device Families
ASR_FAMILY  = [ChassisTypes.ASR5000.val, ChassisTypes.ASR5500.val]
VPC_FAMILY  = [ChassisTypes.VPC_DI.val, ChassisTypes.VPC_SI.val]
MPC_FAMILY = ASR_FAMILY + VPC_FAMILY
LINUX_FAMILY = [ChassisTypes.STAROS.val, ChassisTypes.UBUNTU.val, ChassisTypes.REDHAT.val, ChassisTypes.VMWARE.val]
VIRSH_FAMILY = [ChassisTypes.UBUNTU.val, ChassisTypes.REDHAT.val]
# Adding startOsdevice family for tools devices
TOOLS_DEVICE_FAMILY = ChassisTypes.STAROS.val

# Yaml devices: device-types supported in YAML files
YAML_DEVICE_TYPES = MPC_FAMILY + LINUX_FAMILY + [ChassisTypes.NEXUS.val, ChassisTypes.IXIA.val]


@unique
class DiConnTypes(Enum):
    """
    Enum specifying connection types for DI systems.
    """
    CLI   = 'CLI'
    debug = 'debug'
    host  = 'host'  # This is where virsh and linux commands can be executed.

    def __init__(self, conn_type):
        self.val = conn_type


class VmBootParams(Enum):
    """
    Enum specifying various boot params for VPC Devices.
    """

    VPP_DEFAULT_PARAMS = ["FORWARDER_TYPE", "VPP_CPU_MAIN"]

    VPP_PARAMS = VPP_DEFAULT_PARAMS + ["VPP_CPU_WORKER_CNT", "VPP_CPU_WORKER_LIST", "VPP_DPDK_BUFFERS", "VPP_DPDK_RX_QUEUES",
                                       "VPP_DPDK_TX_QUEUES", "VPP_DPDK_RX_DESCS", "VPP_DPDK_TX_DESCS"]

    # Add IFTASK params here when support is added
    IFTASK_PARAMS = list()
    IFTASK_DEFAULT_PARAMS = list()

    # Combined VM BOOT PARAM LIST
    VM_BOOT_PARAMS = IFTASK_PARAMS + VPP_PARAMS
    VM_DEFAULT_PARAMS = IFTASK_DEFAULT_PARAMS + VPP_DEFAULT_PARAMS

    def __init__(self, param_type):
        self.val = param_type


@unique
class ChassisMode(IntEnum):
    """
    Enum to specify various modes supported in a chassis: boxer, linux, diags, cfe etc.
    """
    BOXER = 1
    LINUX = 2
    DIAG = 3
    CFE = 4

@unique
class ASRCardTypes(Enum):
    """
    Enum used to identify card types of the ASR5500 chassis.
    """
    DPC1 = ('DPC1')
    DPC2 = ('DPC2')
    MIO1 = ('MIO1')
    MIO2 = ('MIO2')
    PSC1 = ('PSC1')
    PSC2 = ('PSC2')
    PSC3 = ('PSC3')
    SMC = ('SMC')
    RCC = ('RCC')
    CFC = ('CFC')
    SFC = ('SFC')
    FC  = ('FC')  # pylint: disable=locally-disabled, invalid-name
    VC  = ('VC')  # pylint: disable=locally-disabled, invalid-name

    def __init__(self, card_name):
        self.card_name = card_name


@unique
class LogLevel(Enum):
    """
    Enum of message levels.
    """
    CRITICAL = (1, 'critical')
    ERROR = (2, 'error')
    WARNING = (3, 'warning')
    UNUSUAL = (4, 'unusual')
    INFO = (5, 'info')
    TRACE = (6, 'trace')
    DEBUG = (7, 'debug')

    def __init__(self, lvl_val, lvl_str):
        self.lvl_val = lvl_val
        self.lvl_str = lvl_str

@unique
class DeviceRole(Enum):
    """
    Enum of device roles.
    """
    UNSPECIFIED = (1, 'unspecified')
    CONTROLLER = (2, 'controller')
    FORWARDER = (3, 'forwarder')

    def __init__(self, role_val, role_str):
        self.role_val = role_val
        self.role_str = role_str

@unique
class DeviceFwdType(Enum):
    """
    Enum for Device Forwarding type IFTASK or VPP
    """

    IFTASK = 'iftask'
    VPP = 'VPP'
    LEGACY = 'LEGACY'

    def __init__(self, fwd_type):
        self.fwd_type = fwd_type

@unique
class CardTypes(Enum):
    """
    Enum of supported card types.
    """
    DPC1 = ('DPC',  'DPC1', 1, 2)
    DPC2 = ('DPC',  'DPC2', 2, 3)
    MIO1 = ('MMIO', 'MIO1', 1, 1)
    MIO2 = ('MMIO', 'MIO2', 2, 1)
    FSC1 = ('FSC',  'FSC1', 1, 0)
    FSC2 = ('FSC',  'FSC2', 2, 0)
    SSC  = ('SSC',  'SSC', None, 0)
    PSC1 = ('PSC',  'PSC1', 1, 2)
    PSC2 = ('PSC', 'PSC2', 1, 2)
    PSC3 = ('PSC', 'PSC3', 1, 2)
    SMC  = ('SMC', 'SMC', None, 1)
    RCC  = ('RCC', 'RCC', None, 0)
    CFC  = ('CFC',  'CFC', None, 1)
    SFC  = ('SFC',  'SFC', None, 1)
    FC   = ('FC',   'FC', None, 1)  # pylint: disable=locally-disabled, invalid-name
    VC   = ('VC',   'VC', None, 1)  # pylint: disable=locally-disabled, invalid-name

    def __init__(self, slot_type, card_name, rev, num_cpus):
        self.slot_type = slot_type
        self.card_name = card_name
        self.card_rev = rev
        self.num_cpus = num_cpus

# the strings in the list are the CardTypes.xx.name i.e. name of enum item
PROCESSING_CARD_TYPES = ['DPC1', 'DPC2', 'PSC1', 'PSC2', 'PSC3', 'SFC', 'FC', 'VC']
MANAGEMENT_CARD_TYPES = ['MIO1', 'MIO2', 'SMC', 'CFC', 'VC']
FABRIC_CARD_TYPES = ['FSC1', 'FSC2']

@unique
class CallModelToolStates(Enum):
    """
    Enum of call model states.
    """
    PRECONFIG = (0, 'PRECONFIG')
    CONFIG = (1, 'CONFIG')
    INIT = (2, 'INIT')
    INCR = (3, 'INCR')
    BAD = (4, 'BAD')
    GOOD = (5, 'GOOD')
    RECOVER = (6, 'RECOVER')
    DEAD = (7, 'DEAD')


@unique
class ReloadOptions(Enum):
    """
    Enum of reload options.
    """
    SYSTEM_RELOAD = (0, 'system-reload')
    STANDBY_MANAGEMENT_CARD = (1, 'standby-management-card')
    ALL_PROCESSING_CARDS = (2, 'all-processing-cards')
    ALL_PROC_CRDS_AND_STBY_MGT_CRD = (3, 'all-processing-cards-and-standby-management-card')
    RAND_ACTIVE_NONDEMUX_CARD = (4, 'random-active-non-demux-card')


    def __init__(self, reload_val, reload_opt):
        self.reload_val = reload_val
        self.reload_opt = reload_opt


@unique
class ReloadTriggers(Enum):
    """
    Enum of reload triggers.
    """
    CARD_REBOOT = (0, 'card-reboot')
    CARD_HIDE = (1, 'card-hide')

    def __init__(self, trigger_val, trigger_opt):
        self.trigger_val = trigger_val
        self.trigger_opt = trigger_opt


@unique
class SwitchoverTriggers(Enum):
    """
    Enum of switchover triggers.
    """
    PLANNED_SWITCHOVER = (0, 'planned-switchover')
    HATCPU_CRASH = (1, 'hatcpu-crash')
    SITMAIN_CRASH = (2, 'sitmain-crash')
    SCT_CRASH = (3, 'sct-crash')
    HATSYSTEM_CRASH = (4, 'hatsystem-crash')
    RCT_CRASH = (5, 'rct-crash')
    SITPARENT_CRASH = (6, 'sitparent-crash')
    KERNEL_CRASH = (7, 'kernel-crash')
    CONTROLPLANE_DOWN = (7, 'controlplane-down')
    SENSOR_VOLTAGE = (8, 'sensor-voltage')
    SENSOR_TEMPERATURE = (9, 'sensor-temperature')
    FABRIC_ERROR = (10, 'fabric-error')
    FABRIC_ETH_CTRL = (11, 'fabric-eth_ctrl')

    def __init__(self, trigger_val, trigger_opt):
        self.trigger_val = trigger_val
        self.trigger_opt = trigger_opt

@unique
class TrafficDirection(Enum):
    """
    Enum of traffic direction.
    """
    UPSTREAM = (0, 'upstream')
    DOWNSTREAM = (1, 'downstream')
    BIDIRECTIONAL = (2, 'bidirectional')

    def __init__(self, traffic_val, traffic_opt):
        self.traffic_val = traffic_val
        self.traffic_opt = traffic_opt

@unique
class MigrationTriggers(Enum):
    """
    Enum of migration triggers.
    """
    PLANNED_MIGRATION = (0, 'planned-migration')
    HIDE_SLOT = (1, 'hide-slot')
    HATCPU_CRASH = (2, 'hatcpu-crash')
    SITMAIN_CRASH = (3, 'sitmain-crash')
    SITPARENT_CRASH = (4, 'sitparent-crash')
    CONTROLPLANE_DOWN = (5, 'controlplane-down')
    KERNEL_CRASH = (6, 'kernel-crash')

    def __init__(self, trigger_val, trigger_opt):
        self.trigger_val = trigger_val
        self.trigger_opt = trigger_opt


@unique
class PortShutTriggers(Enum):
    """
    Enum of port shutdown triggers.
    """
    IP_POOL = (0, 'ip_pool', ['ip-pool'])
    INGRESS_CONTEXTS = (1, 'ingress_contexts', ['pgw', 'ha', 'ggsn', 'hsgw', 'sgw', 'epdg', 'pdsn'])
    EGRESS_CONTEXTS = (2, 'egress_contexts', ['mag', 'fa'])
    PGW = (3, 'pgw', ['pgw'])
    HAX = (4, 'ha',['ha'])
    SGW = (5, 'sgw',['sgw'])
    GGSN = (6, 'ggsn', ['ggsn'])

    def __init__(self, trigger_val, trigger_name, trigger_list):
        self.trigger_val = trigger_val
        self.trigger_name = trigger_name
        self.trigger_list = trigger_list

@unique
class VPCDIPortOptions(Enum):
    """
    Enum for port options on VPCDI
    """
    CONTROL = (0, 'control')
    SERVICE = (1, 'service')

    def __init__(self, port_val, port_opt):
        self.port_val = port_val
        self.port_opt = port_opt

@unique
class CardOptions(Enum):
    """
    Enum of card options.
    """
    SYSTEM_WIDE = (0, 'system-wide')
    ACTIVE_MANAGEMENT_CARD = (1, 'active-management-card')
    STANDBY_MANAGEMENT_CARD = (2, 'standby-management-card')
    ACTIVE_PROCESSING_CARD = (3, 'active-processing-card')
    STANDBY_PROCESSING_CARD = (4, 'standby-processing-card')
    DEMUX_PROCESSING_CARD = (5, 'demux-processing-card')

    def __init__(self, fail_val, fail_opt):
        self.fail_val = fail_val
        self.fail_opt = fail_opt


@unique
class AfioDeviceName(Enum):
    """
    Enum of afio devices.
    """
    MIO1 = ('petra-b')
    MIO2 = ('arad')

    def __init__(self, afio_device_name):
        self.afio_device_name = afio_device_name


@unique
class AfioFabricError(Enum):
    """
    Enum of afio fabric errors.
    """
    MIO_FABRIC_5 = (13)
    MIO_FABRIC_6 = (17)

    def __init__(self, slot_num):
        self.slot_num = slot_num
        self.tweak_cmd = 'tweak enable debug 559'


@unique
class AfioEthernetError(Enum):
    """
    Enum of afio ethernet errors.
    """
    MIO_ETHERNET_5 = (16)
    MIO_ETHERNET_6 = (20)

    def __init__(self, slot_num):
        self.slot_num = slot_num
        self.tweak_cmd5 = 'tweak enable debug-magic 105'
        self.tweak_cmd6 = 'tweak enable debug-magic 106'


@unique
class TaskFailureTriggers(Enum):
    """
    Enum of task failure triggers.
    """
    TASK_CRASH = (0, 'crash')
    TASK_KILL = (1, 'kill')
    INTERLAKEN_FAIL = (2, 'interlaken_fail')
    XAUI_FAIL = (3, 'xaui_fail')
    VOLTAGE = (4, 'voltage')
    TEMPERATURE = (5, 'temperature')
    ERROR = (6, 'error')
    ETH_CTRL = (7, 'eth_ctrl')
    FAILURE = (8, 'failure')

    def __init__(self, trigger_val, trigger_opt):
        self.trigger_val = trigger_val
        self.trigger_opt = trigger_opt


CARD_TYPE_TO_CONST = {CardTypes.MIO1.card_name: CardTypes.MIO1,
                      CardTypes.MIO2.card_name: CardTypes.MIO2,
                      CardTypes.DPC1.card_name: CardTypes.DPC1,
                      CardTypes.DPC2.card_name: CardTypes.DPC2,
                      CardTypes.FSC1.card_name: CardTypes.FSC1,
                      CardTypes.FSC2.card_name: CardTypes.FSC2,
                      CardTypes.SMC.card_name: CardTypes.SMC,
                      CardTypes.PSC1.card_name: CardTypes.PSC1,
                      CardTypes.PSC2.card_name: CardTypes.PSC2,
                      CardTypes.PSC3.card_name: CardTypes.PSC3,
                      CardTypes.RCC.card_name: CardTypes.RCC,
                      CardTypes.SSC.card_name: CardTypes.SSC,
                      CardTypes.CFC.card_name: CardTypes.CFC,
                      CardTypes.SFC.card_name: CardTypes.SFC,
                      CardTypes.FC.card_name: CardTypes.FC,
                      CardTypes.VC.card_name: CardTypes.VC}


class ComponentInfo(Enum):
    """
    Enum of component information.
    There is a dictionary that will map the component name to the constants.
    """
    BIOS2               = ('bios_a', True)
    BIOS3               = ('bios_a', True)
    BIOS3_SECURE        = ("bios_a", True)
    CFE_3               = ("cfe_flash_a", True)
    CFE_SCALE           = ("cfe_flash_a", True)
    MIO_BCF_FPGA        = ("bcf", False)
    MIO_CAF_FPGA        = ("caf", False)
    MIO_DUAL_XDCF_FPGA  = ("dcf_a", False)  # DJP there are two  dcf_a  and dcf_b
    MIO2_BCF2_FPGA      = ("bcf", False)
    MIO2_DPC2_CAF2_FPGA = ("caf", False)
    MIO2_CAF2_FPGA      = ("caf", False)
    MIO2_2CPAK_FPGA     = ("dcf_a", False)
    DPC_BCF_FPGA        = ("bcf", False)
    DPC_CAF_FPGA        = ("caf", False)
    DPC2_BCF2_FPGA      = ("bcf", False)
    DPC2_CAF2_FPGA      = ("caf", False)
    FSC_BCF_FPGA        = ("bcf", False)
    FSC2_BCF2_FPGA      = ("bcf", False)
    SSC_BCF_FPGA        = ("bcf", False)

    def __init__(self, str_name, per_cpu):
        self.str_name = str_name
        self.per_cpu = per_cpu

# In COMP_TYPE_CONST, the key name corresponds to a field in 'show version all'.
COMP_TYPE_CONST = {'BIOS2': ComponentInfo.BIOS2, 'BIOS3': ComponentInfo.BIOS3,
                   'BIOS3_SECURE': ComponentInfo.BIOS3_SECURE,
                   'CFE_3_ROM': ComponentInfo.CFE_3, 'MIO_BCF_FPGA': ComponentInfo.MIO_BCF_FPGA,
                   'MIO_CAF_FPGA': ComponentInfo.MIO_CAF_FPGA, 'MIO_DUAL_XDCF_FPGA': ComponentInfo.MIO_DUAL_XDCF_FPGA,
                   'MIO2_BCF2_FPGA': ComponentInfo.MIO2_BCF2_FPGA,
                   'MIO2_DPC2_CAF2_FPGA': ComponentInfo.MIO2_DPC2_CAF2_FPGA,
                   'MIO2_CAF2_FPGA': ComponentInfo.MIO2_CAF2_FPGA,
                   'MIO2_2CPAK_FPGA': ComponentInfo.MIO2_2CPAK_FPGA, 'DPC_BCF_FPGA': ComponentInfo.DPC_BCF_FPGA,
                   'DPC_CAF_FPGA': ComponentInfo.DPC_CAF_FPGA, 'DPC2_BCF2_FPGA': ComponentInfo.DPC2_BCF2_FPGA,
                   'DPC2_CAF2_FPGA': ComponentInfo.DPC2_CAF2_FPGA,
                   'FSC_BCF_FPGA': ComponentInfo.FSC_BCF_FPGA, 'FSC2_BCF2_FPGA': ComponentInfo.FSC2_BCF2_FPGA,
                   'SSC_BCF_FPGA': ComponentInfo.SSC_BCF_FPGA,
                   'CFE_SCALE': ComponentInfo.CFE_SCALE }


# Snoop search: hd raid super capacitor fault
#sd 0:0:0:0: [sdb]  <<vendor>> ASC=0x80 ASCQ=0x0ASC=0x80 ASCQ=0x0'
RAID_SUPER_CAPACITOR_ERROR = r'sd (\d:\d:\d:\d:) \[(sd\S)\]  <<vendor>> (ASC=0x80 ASCQ=0x0ASC=0x80 ASCQ=0x0)'

@unique
class SnoopErrBase(Enum):
    """
    Enum of base snoop errors.
    """
    INVENTORY_FAIL = (1, 'INVENTORY: Fail')
    FATAL_ENTER_DEAD_LOOP = (2, 'FATAL -- Enter Dead Loop ...')
    RAID_SUPER_CAPACITOR_ERROR = (3, RAID_SUPER_CAPACITOR_ERROR)

    def __init__(self, tag_val, tag_name):
        self.tag_val = tag_val
        self.tag_name = tag_name

@unique
class SRPPeerConn(Enum):
    """
    Enum for 'show srp statistics checkpoint verbose' 'peer conn' state.
    """
    READY = (1, 'Ready')
    CONN = (2, 'Conn')
    BLANK = (3, None)

    def __init__(self, tag_val, tag_name):
        self.tag_val = tag_val
        self.tag_name = tag_name

@unique
class SRPStates(Enum):
    """
    Enum of srp states.
    """
    ACTIVE = (1, 'Active')
    ACTIVE_PEND_STANDBY = (2, 'ActivePendingStandby')
    STANDBY = (3, 'Standby')
    INIT = (4, 'Init')

    def __init__(self, tag_val, tag_name):
        self.tag_val = tag_val
        self.tag_name = tag_name


class VPPCriticalErrors(Enum):
    """
    Enum of VPP Critical ERRORS
    """
    VPP_FRAGMENTATION_ERRORS = ['drops due to concurrent reassemblies limit',
                                'fragments dropped due to reassembly timeout']

    VPP_CRITICAL_ERRORS = ['blackholed packets', 'packets meh drop',
                           'meh bad proto', 'invalid quota row',
                           'unexpected hh to exec', 'no free tx slots',
                           'hold queue overflow', 'fp_q_full', 'dpdk Tx failure',
                           'mbuf alloc failure', 'mcbu skip tx slots'] + VPP_FRAGMENTATION_ERRORS

    VPP_WHITELIST_ERRORS = ['valid packets', 'router advertisements sent',
                            'router advertisements received',
                            'unknown ip protocol', 'no error']

    def __init__(self, error_list):
        self.val = error_list

class VPPNodes(Enum):
    """
    Enum for VPP Nodes
    """

    VPP_NODES = \
               ['adj-meh-rewrite',
                'adj-meh-rewrite-swap-dbia',
                'dpdk-input',
                'ethernet-input',
                'fastpath-6tuple-ip4',
                'fastpath-executive',
                'fastpath-handoff-exec',
                'gtpu4-lookup',
                'interface-output',
                'ip4-drop',
                'ip4-flowdb-dport-prelook',
                'ip4-flowdb-lookup',
                'ip4-input',
                'ip4-load-balance',
                'ip4-local',
                'ip4-lookup',
                'ip4-meh-imposition-dpo',
                'ip4-meh-imposition-plugin',
                'ip4-nh-fwd',
                'ip4-punt',
                'ip4-rewrite',
                'ip4-smp-egress',
                'ip4-smp-egress-extended',
                'ip4-smp-hcf',
                'ip4-smp-policer',
                'ip4-smp-pre-check',
                'ip4-udp-lookup',
                'meh-bia-lookup',
                'meh-disposition',
                'memif-input',
                'tcp4-input',
                'virtio-input',
               ]

    def __init__(self, vpp_nodes):
        self.val = vpp_nodes

@unique
class VPPPerfSamplingStates(Enum):
    """
    Enum of VPP Perf Sampling States.
    """
    ENABLE = (1, 'enable')
    DISABLE = (2, 'disable')

    def __init__(self, tag_val, tag_name):
        self.tag_val = tag_val
        self.tag_name = tag_name


class VPPPerfCounters(Enum):
    """
    Enum for VPP Performance measuring counters
    """

    COUNTER_SET = \
         ['instructions',
          'cpu-cycles',
          'uops_executed.thread',
          'resource_stalls.any',
          'instructions',
          'icache_16b.ifdata_stall',
          'icache_64b.iftag_miss',
          'icache_64b.iftag_stall',
          'cpu-cycles',
          'uops_executed.stall_cycles',
          'uops_issued.stall_cycles',
          'uops_retired.stall_cycles',
          'mem_load_retired.l1_hit',
          'mem_load_retired.l1_miss',
          'mem_load_retired.l2_miss',
          'mem_load_retired.l3_miss',
          'cpu-cycles',
          'instructions',
          'baclears.any',
          'machine_clears.count',
          'mem_inst_retired.all_loads',
          'mem_inst_retired.lock_loads',
          'mem_inst_retired.split_loads',
          'sq_misc.split_lock',
          'instructions',
          'cpu-cycles',
          'uops_executed.thread',
          'resource_stalls.any',
          'offcore_requests.all_requests',
          'offcore_requests.demand_code_rd',
          'offcore_requests.demand_data_rd',
          'offcore_requests.demand_rfo',
          'offcore_requests.demand_data_rd',
          'offcore_requests_outstanding.cycles_with_demand_data_rd',
          'offcore_requests.demand_rfo',
          'offcore_requests_outstanding.cycles_with_demand_rfo',
          'uops_executed.thread',
          'uops_dispatched_port.port_6',
          'uops_dispatched_port.port_7',
          'uops_executed.core_cycles_none',
          'mem_inst_retired.all_stores',
          'mem_inst_retired.split_stores',
          'mem_inst_retired.stlb_miss_stores',
          'sq_misc.split_lock',
          'instructions',
          'cpu-cycles',
          'uops_executed.thread',
          'resource_stalls.any',
          'mem_inst_retired.all_stores',
          'resource_stalls.sb',
          'offcore_requests_buffer.sq_full',
          'exe_activity.bound_on_stores',
          'br_inst_retired.all_branches',
          'br_inst_retired.conditional',
          'br_inst_retired.not_taken',
          'br_inst_retired.near_call',
          'uops_executed.thread',
          'uops_dispatched_port.port_3',
          'uops_dispatched_port.port_4',
          'uops_dispatched_port.port_5',
          'br_inst_retired.all_branches',
          'br_misp_retired.all_branches',
          'br_misp_retired.conditional',
          'br_misp_retired.near_call',
          'sw_prefetch_access.t0',
          'load_hit_pre.sw_pf',
          'l2_rqsts.all_pf',
          'l2_rqsts.pf_miss',
          'instructions',
          'cpu-cycles',
          'uops_executed.thread',
          'resource_stalls.any',
          'uops_executed.thread',
          'uops_dispatched_port.port_0',
          'uops_dispatched_port.port_1',
          'uops_dispatched_port.port_2',
         ]

    def __init__(self, counter_set):
        self.val = counter_set


# Health check section
class HealthCheckTags(Enum):
    """
    Enum of health checks.
    """
    CARD_STATE = (1, 'CARD_STATE')
    CRASH_COUNT = (2, 'CRASH_COUNT')
    LOGS = (3, "LOGS")
    SNOOP = (4, "SNOOP")
    RAID = (5, "RAID")
    CARD_FAILURE = (6, "CARD_FAILURE")
    ALARM_COUNT = (7, "ALARM_COUNT")
    MEMORY_ERROR = (8, "MEMORY_ERROR")
    FABRIC = (9, "FABRIC")
    SUBSCRIBERS = (10, "SUBSCRIBERS")
    IP_BGP_STATE = (11, "IP_BGP_STATE")
    BGP_BFD_COUNT = (12, "BGP_BFD_COUNT")
    KPI = (13, "KPI")
    ICSR_STATE = (14, "ICSR_STATE")
    PORT_UTILIZATION = (15, "PORT_UTILIZATION")
    RAID_AVAILABLE = (16, "RAID_AVAILABLE")
    TASK_RESOURCES = (17, "TASK_RESOURCES")
    BULKSTATS = (18, "BULKSTATS")
    LOGICAL_PORT_UTILIZATION = (19, "LOGICAL_PORT_UTILIZATION")
    NPU_UTILIZATION = (20, "NPU_UTILIZATION")
    SNMP = (21, "SNMP")
    RCT = (22, "RCT")
    LAG = (23, "LAG")
    LICENSE = (24, "LICENSE")
    SRP_CALL_LOSS = (25, "SRP_CALL_LOSS")
    SRP_SWOVR_EVENT = (26, "SRP_SWOVR_EVENT")
    SESSCSTRL_RECONCILIATION = (27, "SESSCSTRL_RECONCILIATION")
    SRP_MON_STATE = (28, "SRP_MON_STATE")
    SRP_CHECKPOINT_STATS = (29, "SRP_CHECKPOINT_STATS")
    SRP_CHECKPOINT_STATS_VERBOSE = (30, "SRP_CHECKPOINT_STATS_VERBOSE")
    OPENFLOW_CONNECTIONS = (31, "OPENFLOW_CONNECTIONS")
    FEMGR_CONNECTIONS = (32, "FEMGR_CONNECTIONS")
    IP_INTERFACE = (33, "IP_INTERFACE")
    IP_NEIGHBORS = (34, "IP_NEIGHBORS")
    IP_ROUTES = (35, "IP_ROUTES")
    CLOUD_DI_NETWORK_CONNECTIONS = (36, "CLOUD_DI_NETWORK_CONNECTIONS")
    CARD_COUNT = (37, "CARD_COUNT")
    BOND_INFO = (38, "BOND_INFO")
    IFTASK = (39, "IFTASK")
    SDR_COLLECT = (40, "SDR_COLLECT")
    VPP_SHOW_ERRORS = (41, "VPP_SHOW_ERRORS")
    SX_PEERS_STATUS = (42, "SX_PEERS_STATUS")
    VPP_SHOW_DPDK_BUFFER = (43, "VPP_SHOW_DPDK_BUFFER")
    VPP_BOOT_PARAM = (44, "VPP_BOOT_PARAM")
    VPP_INTF_Q = (45, "VPP_INTF_Q")
    VPP_HW_INTF_ATTRIB = (46, "VPP_HW_INTF_ATTRIB")

    def __init__(self, tag_val, tag_name):
        self.tag_val = tag_val
        self.tag_name = tag_name


SYSTEM_HEALTH_CHECK_LIST = [HealthCheckTags.CARD_STATE.tag_name,
                            HealthCheckTags.CRASH_COUNT.tag_name,
                            HealthCheckTags.LOGS.tag_name,
                            HealthCheckTags.SNOOP.tag_name,
                            HealthCheckTags.RAID.tag_name,
                            HealthCheckTags.RAID_AVAILABLE.tag_name,
                            HealthCheckTags.CARD_FAILURE.tag_name,
                            HealthCheckTags.ALARM_COUNT.tag_name,
                            HealthCheckTags.MEMORY_ERROR.tag_name,
                            HealthCheckTags.FABRIC.tag_name,
                            HealthCheckTags.TASK_RESOURCES.tag_name,
                            HealthCheckTags.BULKSTATS.tag_name,
                            HealthCheckTags.SNMP.tag_name,
                            HealthCheckTags.RCT.tag_name,
                            HealthCheckTags.LICENSE.tag_name,
                            HealthCheckTags.CLOUD_DI_NETWORK_CONNECTIONS.tag_name,
                            HealthCheckTags.CARD_COUNT.tag_name,
                            HealthCheckTags.BOND_INFO.tag_name,
                            HealthCheckTags.IFTASK.tag_name,
                            HealthCheckTags.SDR_COLLECT.tag_name]

SESSION_HEALTH_CHECK_LIST = [HealthCheckTags.SUBSCRIBERS.tag_name,
                             HealthCheckTags.KPI.tag_name,
                             HealthCheckTags.PORT_UTILIZATION.tag_name,
                             HealthCheckTags.NPU_UTILIZATION.tag_name,
                             HealthCheckTags.LAG.tag_name,
                             HealthCheckTags.SESSCSTRL_RECONCILIATION.tag_name]

PROTO_HEALTH_CHECK_LIST = [HealthCheckTags.IP_BGP_STATE.tag_name,
                           HealthCheckTags.IP_INTERFACE.tag_name,
                           HealthCheckTags.IP_NEIGHBORS.tag_name,
                           HealthCheckTags.IP_ROUTES.tag_name,
                           HealthCheckTags.BGP_BFD_COUNT.tag_name]

ICSR_HEALTH_CHECK_LIST = [HealthCheckTags.ICSR_STATE.tag_name,
                          HealthCheckTags.SRP_CALL_LOSS.tag_name,
                          HealthCheckTags.SRP_SWOVR_EVENT.tag_name,
                          HealthCheckTags.SRP_MON_STATE.tag_name,
                          HealthCheckTags.SRP_CHECKPOINT_STATS.tag_name,
                          HealthCheckTags.SRP_CHECKPOINT_STATS_VERBOSE.tag_name]

VTP_HEALTH_CHECK_LIST = [HealthCheckTags.KPI.tag_name,
                         HealthCheckTags.CRASH_COUNT.tag_name]

CUPS_HEALTH_CHECK_LIST = [HealthCheckTags.SX_PEERS_STATUS.tag_name]

VPP_SYSTEM_HEALTH_CHECK_LIST = [HealthCheckTags.VPP_SHOW_ERRORS.tag_name,
                                HealthCheckTags.VPP_BOOT_PARAM.tag_name,
                                HealthCheckTags.VPP_SHOW_DPDK_BUFFER.tag_name,
                                HealthCheckTags.VPP_INTF_Q.tag_name,
                                HealthCheckTags.VPP_HW_INTF_ATTRIB.tag_name]

VPP_HEALTH_CHECK_LIST = VPP_SYSTEM_HEALTH_CHECK_LIST

# Need to create yaml files for all SI/DI swlab testbeds
# Eventually this map should be built dynamically by reading
# the lab database.
LABDB_CHASSIS_TYPE_MAP = {'MARS_5500': ['swch{}'.format(id) for id in range(21, 28)],
                          'ARES_5500': ['swch{}'.format(id) for id in range(71, 77)],
                          #'VPC_DI': ['swch{}'.format(id) for id in itertools.chain(range(41,46), range(91, 98))],
                          'VPC_DI': ['swch{}'.format(id) for id in [41, 43, 45, 95]],
                          'VPC_SI': ['swch{}'.format(id) for id in itertools.chain(range(31, 35), range(81, 89))]}

class QosPolicyList(Enum):
    """
    Enum of QosPolicyList.
    """
    QOS_POLICY_LIST = ['dscp-derived', 'qci-derived']
    L2MarkNodes = ['dpdk-input', 'memif-input']

    def __init__(self, params):
        self.val = params
