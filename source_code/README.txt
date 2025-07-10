Project Title: SDN-Based Honeypot Deployment and Traffic Analysis

Overview:
This project implements a security architecture integrating a Software-Defined Networking (SDN) controller with a honeypot to capture malicious traffic and log unauthorized access attempts. The project is structured into five stages: (1) SDN Controller Setup, (2) Open vSwitch Configuration, (3) Honeypot Deployment, (4) Traffic Monitoring and Log Collection, and (5) Log Analysis and Reporting.

--------------------------------------------------------------------------------
Stage 1: SDN Controller Setup

- Installed Docker on the SDN VM to facilitate running the Ryu SDN controller in a containerized environment.
- Downloaded the Ryu controller Docker image from osrg/ryu.
- Created a custom Ryu application named ip_randomizer.py inside the directory ~/ryu-apps.
- The ip_randomizer.py application listens for incoming packets and prints the source IP addresses to the console, simulating basic traffic logging.
- Verified the controller by running it using the following command:

sudo docker run -it --rm -v ~/ryu-apps:/ryu-apps -p 6633:6633 osrg/ryu ryu-manager /ryu-apps/ip_randomizer.py

- Confirmed that the controller initializes correctly and logs incoming packets in real-time on the console.

--------------------------------------------------------------------------------
Stage 2: Open vSwitch (OVS) Configuration

- Installed Open vSwitch on the SDN VM.
- Created a new virtual bridge named br0 using the command:

sudo ovs-vsctl add-br br0

- Set the bridge’s controller to point to the local Ryu controller using:

sudo ovs-vsctl set-controller br0 tcp:127.0.0.1:6633

- Verified that the bridge is connected to the controller using:

sudo ovs-vsctl show

- Added the physical interface enp0s1 to the bridge with:

sudo ovs-vsctl add-port br0 enp0s1

- Enabled the bridge interface using:

sudo ip link set dev br0 up

- Verified the status of interfaces and connectivity using ip link show.
- Confirmed that devices in the test network (Attack VM, SDN VM, Honeypot VM) were able to ping each other.

--------------------------------------------------------------------------------
Stage 3: Honeypot Deployment (Cowrie)

- Deployed the Cowrie SSH honeypot inside a Docker container on the Honeypot VM.
- Downloaded the official cowrie/cowrie Docker image.
- Started the Cowrie container using:

sudo docker run -d -p 2222:2222 --name cowrie cowrie/cowrie

- Mounted the Cowrie logs directory to a host folder for external access:

sudo docker run -d -p 2222:2222 --name cowrie -v ~/cowrie-log:/cowrie/var/log cowrie/cowrie

- Verified that the honeypot container is running using:

sudo docker ps

- Confirmed that the honeypot is listening for SSH connections on port 2222.
- Simulated SSH attacks from the Attack VM by connecting with:

ssh -p 2222 root@<honeypot-ip>

- Observed that the Cowrie honeypot captured the fake login attempt and generated corresponding logs inside ~/cowrie-log.

--------------------------------------------------------------------------------
Stage 4: Traffic Monitoring and Log Collection

- Monitored the log output from Cowrie using:

tail -f ~/cowrie-log/cowrie.log

- Confirmed that each login attempt and command entered by the attacker is logged by Cowrie.
- Checked additional log files including cowrie.json (if generated) for structured data about attacks.
- Validated that logs are continuously written during interaction sessions between the attacker and the honeypot.
- Ensured that the honeypot recorded various attack patterns including SSH brute force attempts, invalid commands, and fake shell interactions.
- Created backups of log files for later analysis in stage 5.

--------------------------------------------------------------------------------
Stage 5: Log Analysis and Reporting

- Created a Python script named parse_logs.py to parse the cowrie.log file.
- The script extracts key details such as:
   - IP addresses of attackers
   - Timestamps of login attempts
   - Usernames and passwords tried
   - Commands issued inside the fake shell
- Ran the parser to produce a CSV file summarizing all captured login attempts.
- Analyzed the number of unique attackers, number of failed login attempts, and most common credentials used.
- Included visualizations (e.g., bar charts, tables) inside the final report to summarize attacker behavior.
- Reflected on the types of attacks observed, the value of honeypots for deception, and how captured logs could inform IDS/IPS systems.

--------------------------------------------------------------------------------
Usage Instructions:

1. Launch the Ryu controller on the SDN VM:

sudo docker run -it --rm -v ~/ryu-apps:/ryu-apps -p 6633:6633 osrg/ryu ryu-manager /ryu-apps/ip_randomizer.py

2. Configure Open vSwitch on the SDN VM:

bash ovs_setup.sh

3. Start the Cowrie honeypot on the Honeypot VM:

bash cowrie_run.sh

4. From the Attack VM, attempt SSH connections to the honeypot:

ssh -p 2222 root@<honeypot-ip>

5. Monitor the logs on the Honeypot VM:

tail -f ~/cowrie-log/cowrie.log

6. Analyze captured logs:

python3 parse_logs.py

--------------------------------------------------------------------------------
Conclusion:

This project demonstrates a functional integration of SDN control with a deception honeypot to enable dynamic and programmable traffic monitoring in a virtualized network environment. The system successfully intercepted unauthorized SSH connection attempts, recorded attacker activity, and provided log data suitable for security analysis. This setup can serve as a foundational experiment for further research in software-defined security, automated response systems, and honeypot-based intelligence gathering.

