'''
Created on 08.12.2014
ACN Project
Mininet Topology

@author: Group 19
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
import argparse


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
		# Connect hA:1 to s1:1
		self.addLink(hostA, s1, bw=1, delay='1ms')
		# Connect s3:1 to hB:1
		self.addLink(s3, hostB, bw=1, delay='1ms')

		# High BW Link
		# Connect s1:2 to s2:1
		self.addLink(s1, s2, bw=1.0/2, delay='20ms')
		# Connect s2:2 to s3:2
		self.addLink(s2, s3, bw=1.0/2, delay='20ms')

		# Mid BW Link
		# Connect s1:3 to s4:1
		self.addLink(s1, s4, bw=1.0/8, delay='10ms')
		# Connect s4:2 to s3:3
		self.addLink(s4, s3, bw=1.0/8, delay='10ms')

		# Low BW Link
		# Connect s1:4 to s3:4
		self.addLink(s1, s3, bw=1/32, delay='1ms')

def write_to_file(values, filename):
    file = open(filename, 'w')

    if values is None or not values:
        file.write("")
    else:
        for value in values:
            file.write("{0}\n".format(value))

    file.close()
    print len(values), "results were saved to", filename

def run():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--protocol",
		help="Execute measurements for given protocol. Can be FTP, HTTP or SSH.",
		type=str)
	parser.add_argument(
		"--iterations",
		help="Number of measurements that should be executed. DEFAULT: 1",
		type=int,
		default=1)
	parser.add_argument(
		"--file",
		help="Filename where the results should be saved. Eg. ftp_results.txt",
		type=str)
	args = parser.parse_args()

	topo = MininetTopology()
	net = Mininet(topo=topo, link=TCLink, switch=OVSSwitch)
	net.start()

	print "Configure OVS switches"
	s1, s2, s3, s4 = net.get('s1', 's2', 's3', 's4')
	# Disable Flood at s1:2 port connected to S2
	s1.dpctl("mod-port", 2, "no-flood")
	# Disable Flood at s2:1 port connected to S1
	s2.dpctl("mod-port", 1, "no-flood")
	# Disable Flood at s3:3 port connected to S4
	s3.dpctl("mod-port", 3, "no-flood")
	# Disable Floot at s4:2 port connected to S3
	s4.dpctl("mod-port", 2, "no-flood")

	# print "Dumping host connestions"
	# dumpNodeConnections(net.hosts)
	for host in net.hosts:
		print "Host", host.name, "has IP address", host.IP(), "and MAC address", host.MAC()

	print "Testing network connectivity"
	net.pingAll()

	# print "Testing bandwidth between h1 and h2"
	hostA, hostB = net.get('hA', 'hB')
	# net.iperf((hostA, hostB))

	if(args.protocol and args.protocol == "FTP"):
		print "Testing FTP protocol"
		# Start FTP server on hostB in the background and get PID
		hostB.cmd('python ftp_server.py --ip 10.0.0.2 &')
		pid = int(hostB.cmd('echo $!'))
		ftp_values = []
		for i in xrange(args.iterations):
			print "Iteration {}/{}".format(i+1, args.iterations)
			# Start FTP client on hostA
			time_result = hostA.cmd('python ftp_client.py --ip 10.0.0.2')
			ftp_values.append(float(time_result))
		if(args.file):
			write_to_file(ftp_values, args.file)
		print "Results:", ftp_values
		# Kill FTP server
		hostB.cmd('kill', pid)

	if(args.protocol and args.protocol == "HTTP"):
		print "Testing HTTP protocol"
		# Start HTTP server on hostB in the background and get PID
		hostB.cmd('python http_server.py --server_ip 10.0.0.2 &')
		pid = int(hostB.cmd('echo $!'))
		http_values = []
		for i in xrange(args.iterations):
			print "Iteration {}/{}".format(i+1, args.iterations)
			# Start HTTP client on hostA
			time_result = hostA.cmd('python http_client.py --server_ip 10.0.0.2')
			http_values.append(float(time_result))
		if(args.file):
			write_to_file(http_values, args.file)
		print "Results:", http_values
		# Kill HTTP server
		hostB.cmd('kill', pid)

	if(args.protocol and args.protocol == "SSH"):
		print "Testing SSH protocol"
		# Start SSH server on hostB in the background and get PID
		hostB.cmd('python ssh_server.py --ip 10.0.0.2 &')
		pid = int(hostB.cmd('echo $!'))
		ssh_values = []
		for i in xrange(args.iterations):
			print "Iteration {}/{}".format(i+1, args.iterations)
			# Start SSH client on hostA
			time_result = hostA.cmd('python ssh_client.py --ip 10.0.0.2')
			ssh_values.append(float(time_result))
		if(args.file):
			write_to_file(ssh_values, args.file)
		print "Results:", ssh_values
		# Kill SSH server
		hostB.cmd('kill', pid)

	# Stop mininet
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	run()
