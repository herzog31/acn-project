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

	def __init__(self):
		self.topology = None
		self.listSwitches = {}
		self.linkList = []
		core.listen_to_dependencies(self, ['topology'], short_attrs=True)

	def createDOTfile(self):
		content = "graph Network {\n"
		for s in self.listSwitches:
			switch = self.listSwitches[s]
			content += "\tsubgraph cluster_s" + str(switch.dpid) +" {\n\t\tlabel=\"" + dpidToStr(switch.dpid) + "\";\n"
			for p in switch.ports:
				content += "\t\tport" + str(switch.dpid) + "_" + str(p) + "[label=\"port: "+ str(p) +"\\n"+str(switch.ports[p].hwAddr)+"\", shape=box];\n"
			content += "\t}\n"
		for link in self.linkList:
			content += "\tport" + str(link.dpid1) + "_" + str(link.port1) + " -- port" + str(link.dpid2) + "_" + str(link.port2) + "\n"
		content += "}"

		return content

	def saveToFile(self, fileContent, fileName):
		file = open(fileName, 'w')
		file.write(fileContent)
		file.close()

	def printTopology(self):
		fileName = "graph.gv"
		dotFile = self.createDOTfile()
		self.saveToFile(dotFile, fileName)

		for s in self.listSwitches:
			switch = self.listSwitches[s]
			print "Switch ", dpidToStr(switch.dpid)
			print "\t Ports"
			for p in switch.ports:
				print "\t\tName", switch.ports[p].name, "No", switch.ports[p].number, "MAC", switch.ports[p].hwAddr, "Entites", switch.ports[p].entities
		print "Links"
		for link in self.linkList:
			print "\t", link

	def _handle_removeSwitch(self, event):
		print "Incoming SwitchLeave Event"
		self.removeSwitch(event.entity.dpid)
		self.printTopology()

	def _handle_connectionDown(self, event):
		print "Incoming ConnectionDown"
		self.removeSwitch(event.dpid)
		self.printTopology()

	def _handle_newSwitch(self, event):
		print "Incoming SwitchJoin Event"
		switch = event.switch
		self.listSwitches[switch.dpid] = event.switch
		self.printTopology()

	def _handle_linkEvent(self, event):
		print "Incoming LinkEvent"
		if event.added:
			self.addLink(event.link)
		elif event.removed:
			self.removeLink(event.link)
		
		self.printTopology()

	def removeLink(self, linkRemove):
		for link in self.linkList:
			if  ((link.dpid1 == linkRemove.dpid1 and link.dpid2 == linkRemove.dpid2 and link.port1 == linkRemove.port1 and link.port2 == linkRemove.port2)
				or
				(link.dpid2 == linkRemove.dpid1 and link.dpid1 == linkRemove.dpid2 and link.port2 == linkRemove.port1 and link.port1 == linkRemove.port2)):
				self.linkList.remove(link)

	def addLink(self, linkAdd):
		for link in self.linkList:
			if  ((link.dpid1 == linkAdd.dpid1 and link.dpid2 == linkAdd.dpid2 and link.port1 == linkAdd.port1 and link.port2 == linkAdd.port2)
				or
				(link.dpid2 == linkAdd.dpid1 and link.dpid1 == linkAdd.dpid2 and link.port2 == linkAdd.port1 and link.port1 == linkAdd.port2)):
				return
		self.linkList.append(linkAdd)		

	def removeSwitch(self, switchRemove):
		if self.listSwitches.has_key(switchRemove):
			del self.listSwitches[switchRemove]


def launch():
	topo = NetworkTopology()
	topo.printTopology()

	pox.openflow.discovery.launch()
	pox.topology.launch()
	pox.openflow.topology.launch()

	def addEventListeners():
		core.openflow_discovery.addListenerByName("LinkEvent", topo._handle_linkEvent)
		core.topology.addListenerByName("SwitchJoin", topo._handle_newSwitch)
		core.topology.addListenerByName("SwitchLeave", topo._handle_removeSwitch)
		core.openflow.addListenerByName("ConnectionDown", topo._handle_connectionDown)

	core.call_when_ready(addEventListeners, "openflow_discovery")