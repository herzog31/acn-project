'''
Created on 15.01.2015
ACN Project
Mininet Topology for Discovery

@author: Group 19
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
from mininet.node import RemoteController

class MininetTopology(Topo):

    """
    This class implements the mininet topology.
    """

    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        # Add the hosts with ip addresses
        hostA = self.addHost('hA', ip='10.0.0.1/24')
        hostB = self.addHost('hB', ip='10.0.0.2/24')

        # Add the switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Host Links
        # Connect hA:1 to s1:1
        self.addLink(hostA, s1)
        # Connect s3:1 to hB:1
        self.addLink(s3, hostB)

        # High BW Link
        # Connect s1:2 to s2:1
        self.addLink(s1, s2)
        # Connect s2:2 to s3:2
        self.addLink(s2, s3)

        # Mid BW Link
        # Connect s1:3 to s4:1
        self.addLink(s1, s4)
        # Connect s4:2 to s3:3
        self.addLink(s4, s3)

        # Low BW Link
        # Connect s1:4 to s3:4
        self.addLink(s1, s3)

def run():
    # Create mininet topology
    topo = MininetTopology()
    net = Mininet(topo=topo, switch=OVSSwitch, controller=RemoteController)
    net.start()

    # Print all hosts with their ip and mac addresses
    for host in net.hosts:
        print "Host", host.name, "has IP address", host.IP(), \
            "and MAC address", host.MAC()

    # Execute pingAll() command to check connectivity
    # print "Testing network connectivity"
    # net.pingAll()

    # print "Testing bandwidth between h1 and h2"
    # hostA, hostB = net.get('hA', 'hB')
    # net.iperf((hostA, hostB))

    # Stop mininet
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
