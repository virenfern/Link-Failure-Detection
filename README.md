Project 14: Link Failure Detection and Recovery using SDN
1. Problem Statement
In traditional networking, link failures can lead to significant downtime and manual reconfiguration. This project demonstrates how Software-Defined Networking (SDN) can automate fault tolerance. Using a Triangle Topology, the goal is to implement a system where a central controller (POX) dynamically detects a link failure between two switches and reroutes traffic through a backup path without manual intervention, ensuring high availability.
<img width="602" height="328" alt="Picture1" src="https://github.com/user-attachments/assets/e9c2e97f-92af-4d8b-853d-9c6f89cf17e4" />

2. Methodology & TopologyThe network consists of three Open vSwitches ($s1, s2, s3$) and two hosts ($h1, h2$).Primary Path: $h1 \to s1 \to s2 \to h2$Backup Path: $h1 \to s1 \to s3 \to s2 \to h2$Tools Used:Mininet: Network emulation.POX Controller: Python-based SDN controller.OpenFlow: Communication protocol between the control plane and data plane.Wireshark: Packet analysis and verification.
3.Setup and Execution Steps
Initialize the Controller:
Start the POX controller with the Spanning Tree and Discovery modules:

Bash
./pox.py forwarding.l2_learning openflow.discovery openflow.spanning_tree --hold-down=2
Launch Topology:
Run the custom Python topology script:

Bash
sudo python3 topo.py
Establish Traffic:
Initiate a ping between hosts to establish the primary flow:

Bash
mininet> h1 ping h2
Simulate Failure:
Manually disable the active link:

Bash
mininet> link s1 s2 down


