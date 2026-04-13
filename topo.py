#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class TriangleTopo(Topo):
    def build(self):
        # Add 3 Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add 2 Hosts
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')

        # Connect Hosts to Switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)

        # Create Triangle Connections between Switches
        # Primary Path: s1-s2
        self.addLink(s1, s2)
        # Backup Path: s1-s3 and s3-s2
        self.addLink(s1, s3)
        self.addLink(s3, s2)

def run():
    topo = TriangleTopo()
    # Connect to the POX controller running on the same VM (127.0.0.1)
    net = Mininet(topo=topo, 
                  controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
                  switch=OVSSwitch,
                  link=TCLink)
    
    net.start()
    print("*** Topology is up. Starting CLI...")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()