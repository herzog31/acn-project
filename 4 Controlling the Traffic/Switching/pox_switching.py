'''
Created on 16.01.2015
ACN Project
POX Network Controller

@author: Group 19
'''

from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of

# Get the Logger for POX
log = core.getLogger()


class PacketSwitching:

    '''
    Packet Switching class

    Switches packets over one of the three paths.
    '''

    def __init__(self, bandwidth):
        '''
        '''
        self.bandwidth = bandwidth

    def _handle_PacketIn(self, event):
        '''
        Handles incoming packets on a switch. Returns the switching decision.
        '''
        dpid = event.dpid
        in_port = event.port
        packet = event.parsed
        con = event.connection
        log.debug("Switch %s received a packet on %s" %
                  (dpidToStr(dpid), str(in_port)))

        log.debug("DUMP: %s" % packet.dump())

        # Get outgoing port for current switch according to the selected
        # path/bandwidth
        out_port = self.__get_out_port(dpid, in_port)

        log.debug("out_port: %s" % (str(out_port)))

        if out_port < 0:
            log.error("Unable to detect" +
                      " out_port for switch %s!" % (dpidToStr(dpid)))
            return

        # Install forwarding rule if the packet is an IPv4-Packet
        if packet.type == 0x0800:
            log.debug("Installing forwarding rule...")
            src_ip = packet.payload.srcip
            dst_ip = packet.payload.dstip
            self.install_forwarding_rule(
                con, src_ip, dst_ip, out_port)

        # Sending packet to the outgoing port
        log.debug("Sending packet to out_port")
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        con.send(msg)

    def install_forwarding_rule(self, con, nw_src, nw_dst, out_port):
        '''
        This function installs a forwarding rule for
        the switch according to the path that is currently set.
        '''
        log.debug("Installing forwarding rule:")

        # Set message to install forwarding rule
        msg = of.ofp_flow_mod()

        # Set ethertype to IPv4
        log.debug("dl_type = 0x0800")
        msg.match.dl_type = 0x0800

        # Set Source-IP
        log.debug("nw_src = %s" % nw_src)
        msg.match.nw_src = nw_src

        # Set Destination-IP
        log.debug("nw_dst = %s" % nw_dst)
        msg.match.nw_dst = nw_dst

        # Set outgoing port(s)
        log.debug("out_port = %s" % out_port)
        msg.actions = [of.ofp_action_output(port=out_port)]

        # Send message to switch
        con.send(msg)

    def __get_out_port(self, dpid, in_port):
        '''
        This function returns the out_port for every switch. In case no valid
        out_port can be found, a negative value will be returned. The function
        checks whether the source and destination are the ones expected. The
        out_port is chosen according to the bandwidth that is currently set.
        '''

        if self.bandwidth == "high":  # Finding out_port for "high" bandwidth
            if dpid == 1 and in_port == 1:
                return 2
            elif dpid == 2 and in_port == 1:
                return 2
            elif dpid == 3 and in_port == 2:
                return 1
            elif dpid == 3 and in_port == 1:
                return 2
            elif dpid == 2 and in_port == 2:
                return 1
            elif dpid == 1 and in_port == 2:
                return 1
        elif self.bandwidth == "med":  # Finding out_port for "med" bandwidth
            if dpid == 1 and in_port == 1:
                return 3
            elif dpid == 4 and in_port == 1:
                return 2
            elif dpid == 3 and in_port == 3:
                return 1
            elif dpid == 3 and in_port == 1:
                return 3
            elif dpid == 4 and in_port == 2:
                return 1
            elif dpid == 1 and in_port == 3:
                return 1
        elif self.bandwidth == "low":  # Finding out_port for "low" bandwidth
            if dpid == 1 and in_port == 1:
                return 4
            elif dpid == 3 and in_port == 4:
                return 1
            elif dpid == 3 and in_port == 1:
                return 4
            elif dpid == 1 and in_port == 4:
                return 1
        else:  # No valid out_port could be generated
            return -1


def launch(bw):
    '''
    Standard launch-function for POX. The launch
    function requires the bandwidth to be set!
    '''
    # Check whether bandwidth was set correctly
    if bw is None and (bw != "low" or bw != "med" or bw != "high"):
        log.error("Error: Bandwidth was not correctly set! " +
                  "Use --bw={low|med|high}")
        return

    # Create instance
    switching = PacketSwitching(bw)

    # Event listener for adding / removing Links
    core.openflow.addListenerByName(
        "PacketIn",
        switching._handle_PacketIn)
