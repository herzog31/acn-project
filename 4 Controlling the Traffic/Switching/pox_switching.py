'''
Created on 16.01.2015
ACN Project
POX Network Controller

@author: Group 19
'''

from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.ethernet import ethernet


# Get the Logger for POX
log = core.getLogger()


class PacketSwitching:

    '''
    Packet Switching class

    Switches packets over one of the three paths.
    '''

    ftp_port = 10021
    ssh_port = 10022
    http_port = 10080
    hostA_ip = "10.0.0.1"
    hostB_ip = "10.0.0.2"
    other_bw = "low"

    def __init__(self, ftp_bw, ssh_bw, http_bw):
        '''
        '''
        self.ftp_bw = ftp_bw
        self.ssh_bw = ssh_bw
        self.http_bw = http_bw

    def _handle_PacketIn(self, event):
        '''
        Handles incoming packets on a switch. Returns the switching decision.
        '''
        dpid = event.dpid
        in_port = event.port
        packet = event.parsed
        con = event.connection
        out_port = self.__get_out_port(self.other_bw, dpid, in_port)

        if packet.type == ethernet.IP_TYPE:
            tcpp = event.parsed.find('tcp')
            if not tcpp is None:
                
                ftp_out_port = self.__get_out_port(self.ftp_bw, dpid, in_port)
                ssh_out_port = self.__get_out_port(self.ssh_bw, dpid, in_port)
                http_out_port = self.__get_out_port(self.http_bw, dpid, in_port)
                print "Out Ports: FTP %s, SSH %s, HTTP %s, Rest %s" % (str(ftp_out_port), str(ssh_out_port), str(http_out_port), str(out_port))

                if packet.payload.srcip == self.hostA_ip and tcpp.dstport == self.ssh_port and not ssh_out_port is None:
                    print "SSH Packet from A -> B"
                    self.install_forwarding_rule(con, packet.payload.srcip, None, None, tcpp.dstport, ssh_out_port)
                    self.send_packet_to_port(ssh_out_port, event)
                    return

                if packet.payload.srcip == self.hostB_ip and tcpp.srcport == self.ssh_port and not ssh_out_port is None:
                    print "SSH Packet from B -> A"
                    self.install_forwarding_rule(con, packet.payload.srcip, None, tcpp.srcport, None, ssh_out_port)
                    self.send_packet_to_port(ssh_out_port, event)
                    return

                if packet.payload.srcip == self.hostA_ip and tcpp.dstport == self.ftp_port and not ftp_out_port is None:
                    print "FTP Packet from A -> B"
                    self.install_forwarding_rule(con, packet.payload.srcip, None, None, tcpp.dstport, ftp_out_port)
                    self.send_packet_to_port(ftp_out_port, event)
                    return

                if packet.payload.srcip == self.hostB_ip and tcpp.srcport == self.ftp_port and not ftp_out_port is None:
                    print "FTP Packet from B -> A"
                    self.install_forwarding_rule(con, packet.payload.srcip, None, tcpp.srcport, None, ftp_out_port)
                    self.send_packet_to_port(ftp_out_port, event)
                    return

                if packet.payload.srcip == self.hostA_ip and tcpp.dstport == self.http_port and not http_out_port is None:
                    print "HTTP Packet from A -> B"
                    self.install_forwarding_rule(con, packet.payload.srcip, None, None, tcpp.dstport, http_out_port)
                    self.send_packet_to_port(http_out_port, event)
                    return

                if packet.payload.srcip == self.hostB_ip and tcpp.srcport == self.http_port and not http_out_port is None:
                    print "HTTP Packet from B -> A"
                    self.install_forwarding_rule(con, packet.payload.srcip, None, tcpp.srcport, None, http_out_port)
                    self.send_packet_to_port(http_out_port, event)
                    return

                print "IP Source: %s, IP Dest: %s, TCP Source: %s, TCP Destination: %s" % (str(packet.payload.srcip), str(packet.payload.dstip), str(tcpp.srcport), str(tcpp.dstport))

        if out_port < 0:
            #log.error("Unable to detect out_port for switch %s with in_port %s!" % (dpidToStr(dpid), str(in_port)))
            return

        # Sending packet to the outgoing port
        self.send_packet_to_port(out_port, event)

    def send_packet_to_port(self, out_port, event):
        log.debug("Sending packet to out_port")
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

    def install_forwarding_rule(self, con, nw_src, nw_dst, tp_src, tp_dst, out_port):
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

        # Set protocol to TCP
        log.debug("nw_proto = 6")
        msg.match.nw_proto = 6

        # Set Source-IP
        log.debug("nw_src = %s" % nw_src)
        msg.match.nw_src = nw_src

        # Set Destination-IP
        log.debug("nw_dst = %s" % nw_dst)
        msg.match.nw_dst = nw_dst

        # Set TCP Source Port
        log.debug("tp_src = %s" % tp_src)
        msg.match.tp_src = tp_src

        # Set TCP Destination Port
        log.debug("tp_dst = %s" % tp_dst)
        msg.match.tp_dst = tp_dst

        # Set outgoing port(s)
        log.debug("out_port = %s" % out_port)
        msg.actions.append(of.ofp_action_output(port=out_port))

        # Send message to switch
        con.send(msg)

    def __get_out_port(self, bandwidth, dpid, in_port):
        '''
        This function returns the out_port for every switch. In case no valid
        out_port can be found, a negative value will be returned. The function
        checks whether the source and destination are the ones expected. The
        out_port is chosen according to the bandwidth that is currently set.
        '''

        if bandwidth == "high":  # Finding out_port for "high" bandwidth
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
        elif bandwidth == "med":  # Finding out_port for "med" bandwidth
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
        elif bandwidth == "low":  # Finding out_port for "low" bandwidth
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


def launch(ftp_bw, ssh_bw, http_bw):
    '''
    Standard launch-function for POX. The launch
    function requires the bandwidth to be set!
    '''
    # Check whether bandwidth was set correctly
    if ftp_bw != "low" and ftp_bw != "med" and ftp_bw != "high" and ssh_bw != "low" and ssh_bw != "med" and ssh_bw != "high" and http_bw != "low" and http_bw != "med" and http_bw != "high":
        print "Error: Bandwidth was not correctly set! Use --ftp_bw={low|med|high} --ssh_bw={low|med|high} --http_bw={low|med|high}"
        return

    # Create instance
    switching = PacketSwitching(ftp_bw, ssh_bw, http_bw)

    # Event listener for adding / removing Links
    core.openflow.addListenerByName(
        "PacketIn",
        switching._handle_PacketIn)
