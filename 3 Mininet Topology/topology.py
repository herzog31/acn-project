from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class MininetTopology(Topo):
	def __init__(self, **opts):
		Topo.__init__(self, **opts)

		# Hosts
		hostA = self.addHost('hA', ip='10.0.0.1/24')
		hostB = self.addHost('hB', ip='10.0.0.2/24')

		# Switches
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')

		# Host Links
		self.addLink(hostA, s1, bw=1, delay='1ms')
		self.addLink(s3, hostB, bw=1, delay='1ms')

		# High BW Link
		# self.addLink(s1, s2, bw=1.0/2, delay='20ms')
		# self.addLink(s2, s3, bw=1.0/2, delay='20ms')

		# Mid BW Link
		self.addLink(s1, s4, bw=1.0/8, delay='10ms')
		self.addLink(s4, s3, bw=1.0/8, delay='10ms')

		# Low BW Link
		# self.addLink(s1, s3, bw=1.0/32, delay='1ms')
		

def test():
	topo = MininetTopology()
	net = Mininet(topo=topo, link=TCLink)
	net.start()

	print "Dumping host connestions"
	dumpNodeConnections(net.hosts)

	print "Testing network connectivity"
	net.pingAll()

	print "Testing bandwidth between h1 and h2"
	hostA, hostB = net.get('hA', 'hB')

	print "Host", hostA.name, "has IP address", hostA.IP(), "and MAC address", hostA.MAC()
	print "Host", hostB.name, "has IP address", hostB.IP(), "and MAC address", hostB.MAC()

	net.iperf((hostA, hostB))
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	test()
