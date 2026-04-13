# Project 14: Link Failure Detection and Recovery using SDN

## 1. Problem Statement
In traditional networking, link failures often lead to significant downtime and require manual reconfiguration or slow legacy protocols. This project demonstrates how **Software-Defined Networking (SDN)** can automate fault tolerance and path restoration. Using a **Triangle Topology**, the goal is to implement a system where a central **POX Controller** dynamically detects a link failure between two switches via OpenFlow and automatically reroutes traffic through a backup path to maintain connectivity.

---

## 2. Topology & Infrastructure
The network is emulated in Mininet and follows a triangle design to provide redundancy.
**Screenshot Placeholder:** [![Uploading image.png…]()]

* **Hosts:** `h1` (10.0.0.1), `h2` (10.0.0.2)
* **Switches:** `s1`, `s2`, `s3` (Open vSwitches)
* **Controller:** Remote POX Controller (127.0.0.1)

### Path Logic:
- **Primary Path:** `h1` <-> `s1` <-> `s2` <-> `h2`
- **Backup Path:** `h1` <-> `s1` <-> `s3` <-> `s2` <-> `h2`

---

## 3. Setup and Execution Steps

1.  **Initialize the POX Controller:**
    In Terminal 1, run the controller with the necessary modules for discovery and loop prevention:
    ```bash
    ./pox.py forwarding.l2_learning openflow.discovery openflow.spanning_tree --hold-down=2
    ```

2.  **Launch the Network Topology:**
    In Terminal 2, execute the custom Mininet script:
    ```bash
    sudo python3 topo.py
    ```

3.  **Monitor Traffic with Wireshark:**
    Open Wireshark on the `loopback (lo)` interface and filter by `openflow_v1` to observe the control channel.

4.  **Execute the Test:**
    - Start a ping from `h1` to `h2`.
    - Manually bring down the primary link using `link s1 s2 down`.
    - Observe the automatic recovery and traffic rerouting.

---

## 4. Proof of Execution

### A. Connectivity & Recovery (Ping/iperf Results)
Initially, the pings show low latency. When the `s1-s2` link is disabled, the pings pause briefly during the **STP Convergence** period and then resume automatically via the backup switch `s3`.

> **Screenshot Placeholder:** [Upload screenshot showing pings resuming with a change in RTT]

**Analysis:** The Round Trip Time (RTT) increases after recovery (e.g., from 0.05ms to ~10ms+) because the data packets must now travel through an additional switch (`s3`).

### B. Flow Table Verification
We used `ovs-ofctl` to inspect the Flow Tables on `s1` to prove the controller modified the data plane rules.

- **Pre-Failure:** Flow rule matches Destination IP and outputs to the port connected to `s2`.
- **Post-Failure:** Flow rule is updated by the controller to output to the port connected to `s3`.

> **Screenshot Placeholder:** [Upload screenshot of 'sh ovs-ofctl dump-flows s1' output]

### C. Wireshark Logs (Link Detection)
The "Detection" phase is validated by the **`OFPT_PORT_STATUS`** message. This is an asynchronous message sent by the switch to the POX controller to report that a link is down.

> **Screenshot Placeholder:** [Upload your Wireshark screenshot showing the OFPT_PORT_STATUS packet]

---

## 5. Conclusion
The project successfully demonstrates the core advantage of SDN: **Centralized Control Plane Logic**. By separating the control logic from the physical switches, the POX controller was able to detect a link failure in real-time and push new flow rules to the switches, achieving recovery with zero manual configuration.
