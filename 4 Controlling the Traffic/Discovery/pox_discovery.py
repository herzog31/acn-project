'''
Created on 15.01.2015
ACN Project
POX Discovery Controller

@author: Group 19
'''

from pox.core import core
import pox.topology.topology
import pox.openflow.discovery
import pox.openflow.topology
from pox.lib.util import dpidToStr
from pprint import pprint

class NetworkTopology:

	"""
	Network Topology class

	Includes event handler functionality and DOT file creation
	"""

	def __init__(self):
		# Create empty topology
		self.topology = None
		# Create empty dict for switches
		self.listSwitches = {}
		# Create empty list for links
		self.linkList = []
		# Fill topology with data from Topology & Openflow Topology modules
		core.listen_to_dependencies(self, ['topology'], short_attrs=True)

	def createDOTfile(self):
		"""
		Creates a DOT graph from the topology
		"""

		content = "graph Network {\n"
		# Add all switches
		for s in self.listSwitches:
			switch = self.listSwitches[s]
			content += "\tsubgraph cluster_s" + str(switch.dpid) +" {\n\t\tlabel=\"" + dpidToStr(switch.dpid) + "\";\n"
			# Add ports of switches
			for p in switch.ports:
				content += "\t\tport" + str(switch.dpid) + "_" + str(p) + "[label=\"port: "+ str(p) +"\\n"+str(switch.ports[p].hwAddr)+"\", shape=box];\n"
			content += "\t}\n"
		# Add links between switches
		for link in self.linkList:
			content += "\tport" + str(link.dpid1) + "_" + str(link.port1) + " -- port" + str(link.dpid2) + "_" + str(link.port2) + "\n"
		content += "}"

		return content

	def saveToFile(self, fileContent, fileName):
		"""
		Saves a given fileContent to a file named fileName
		"""
		file = open(fileName, 'w')
		file.write(fileContent)
		file.close()

	def printTopology(self):
		"""
		Updates the DOT graph file and prints out current topology
		"""

		# Filename to save the DOT graph
		fileName = "graph.gv"
		# Create DOT graph
		dotFile = self.createDOTfile()
		# Save DOT graph into file
		self.saveToFile(dotFile, fileName)

		# Print all switches
		for s in self.listSwitches:
			switch = self.listSwitches[s]
			print "Switch ", dpidToStr(switch.dpid)
			print "\t Ports"
			# Print ports of switches
			for p in switch.ports:
				print "\t\tName", switch.ports[p].name, "No", switch.ports[p].number, "MAC", switch.ports[p].hwAddr, "Entites", switch.ports[p].entities
		# Print all links
		print "Links"
		for link in self.linkList:
			print "\t", link

	def _handle_removeSwitch(self, event):
		# Handler for SwitchLeave event
		print "Incoming SwitchLeave Event"
		# Remove switch
		self.removeSwitch(event.entity.dpid)
		# Refresh topology
		self.printTopology()

	def _handle_connectionDown(self, event):
		# Handler for ConnectionDown event
		print "Incoming ConnectionDown"
		# Remove switch
		self.removeSwitch(event.dpid)
		# Refresh topology
		self.printTopology()

	def _handle_newSwitch(self, event):
		# Handler for SwitchJoin event
		print "Incoming SwitchJoin Event"
		switch = event.switch
		# Add new switch to dict
		self.listSwitches[switch.dpid] = event.switch
		# Refresh topology
		self.printTopology()

	def _handle_linkEvent(self, event):
		# Handler for LinkEvent event
		print "Incoming LinkEvent"
		if event.added:
			# Add new link
			self.addLink(event.link)
		elif event.removed:
			# Remove existing link
			self.removeLink(event.link)
		
		# Refresh topology
		self.printTopology()

	def removeLink(self, linkRemove):
		# Removes linkRemove from linkList
		# Makes sure that both s1 -> s2 and s2 -> s1 are removed
		for link in self.linkList:
			if  ((link.dpid1 == linkRemove.dpid1 and link.dpid2 == linkRemove.dpid2 and link.port1 == linkRemove.port1 and link.port2 == linkRemove.port2)
				or
				(link.dpid2 == linkRemove.dpid1 and link.dpid1 == linkRemove.dpid2 and link.port2 == linkRemove.port1 and link.port1 == linkRemove.port2)):
				self.linkList.remove(link)

	def addLink(self, linkAdd):
		# Adds linkAdd to linkList
		# Makes sure that only one link between two switches is added
		for link in self.linkList:
			if  ((link.dpid1 == linkAdd.dpid1 and link.dpid2 == linkAdd.dpid2 and link.port1 == linkAdd.port1 and link.port2 == linkAdd.port2)
				or
				(link.dpid2 == linkAdd.dpid1 and link.dpid1 == linkAdd.dpid2 and link.port2 == linkAdd.port1 and link.port1 == linkAdd.port2)):
				return
		self.linkList.append(linkAdd)		

	def removeSwitch(self, switchRemove):
		# Remove switchRemove from switch dict if it exists
		if self.listSwitches.has_key(switchRemove):
			del self.listSwitches[switchRemove]


def launch():
	# Instatiate NetworkTopology class
	topo = NetworkTopology()
	# Print empty topology
	topo.printTopology()

	# Start Openflow Discovery module
	pox.openflow.discovery.launch()
	# Start POX Topology module
	pox.topology.launch()
	# Start Openflow Topology module
	pox.openflow.topology.launch()

	def addEventListeners():
		# Event listener for adding / removing Links
		core.openflow_discovery.addListenerByName("LinkEvent", topo._handle_linkEvent)
		# Event listener for adding switches
		core.topology.addListenerByName("SwitchJoin", topo._handle_newSwitch)
		# Event listener for removing switches
		core.topology.addListenerByName("SwitchLeave", topo._handle_removeSwitch)
		core.openflow.addListenerByName("ConnectionDown", topo._handle_connectionDown)

	# Add event listeners as soon as Openflow Discovery is loaded
	core.call_when_ready(addEventListeners, "openflow_discovery")