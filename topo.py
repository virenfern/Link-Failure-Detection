#!/usr/bin/python

# Import necessary Mininet modules
from mininet.topo import Topo                        # Base class for defining topologies
from mininet.net import Mininet                      # Core class to create and manage the network
from mininet.node import RemoteController, OVSSwitch # Remote SDN controller and Open vSwitch
from mininet.link import TCLink                      # Traffic-controlled links (supports bandwidth/delay settings)
from mininet.cli import CLI                          # Interactive command-line interface for the network
from mininet.log import setLogLevel                  # Logging utility to control verbosity


class TriangleTopo(Topo):
    """
    Custom topology class that creates a triangle-shaped network:
    
        h1 -- s1 -- s2 -- h2
                \       /
                 s3----
    
    - h1 connects to s1, h2 connects to s2
    - Primary path between switches: s1 <-> s2 (direct)
    - Backup path between switches:  s1 <-> s3 <-> s2
    """

    def build(self):
        # ── Switches ──────────────────────────────────────────────────────────
        s1 = self.addSwitch('s1')   # Switch 1: entry point for host h1
        s2 = self.addSwitch('s2')   # Switch 2: entry point for host h2
        s3 = self.addSwitch('s3')   # Switch 3: intermediate/backup relay switch

        # ── Hosts ─────────────────────────────────────────────────────────────
        h1 = self.addHost('h1', ip='10.0.0.1')  # Host 1 with static IP
        h2 = self.addHost('h2', ip='10.0.0.2')  # Host 2 with static IP

        # ── Host-to-Switch Links ───────────────────────────────────────────────
        self.addLink(h1, s1)   # h1 connects directly to s1
        self.addLink(h2, s2)   # h2 connects directly to s2

        # ── Switch-to-Switch Links (Triangle) ─────────────────────────────────
        # Primary path: direct link between s1 and s2 (shortest route)
        self.addLink(s1, s2)

        # Backup path: traffic can be rerouted through s3 if the primary fails
        self.addLink(s1, s3)   # s1 <-> s3 (first leg of backup path)
        self.addLink(s3, s2)   # s3 <-> s2 (second leg of backup path)


def run():
    """
    Instantiates the topology, connects to the POX SDN controller,
    starts the network, launches the CLI, and cleanly shuts down on exit.
    """

    topo = TriangleTopo()   # Build the triangle topology defined above

    # Create the Mininet network with:
    #   - Our custom triangle topology
    #   - A remote POX controller listening on localhost:6633
    #   - OVSSwitch (Open vSwitch) as the switch type
    #   - TCLink to allow per-link bandwidth/delay/loss parameters
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
        switch=OVSSwitch,
        link=TCLink
    )

    net.start()   # Bring up all switches, hosts, and links

    print("*** Topology is up. Starting CLI...")

    CLI(net)      # Open an interactive CLI so you can run commands (e.g. pingall, iperf)

    net.stop()    # Tear down the network cleanly when the CLI is exited


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    setLogLevel('info')   # Set Mininet log verbosity to 'info' (options: debug, info, warning, error)
    run()                 # Launch the network
