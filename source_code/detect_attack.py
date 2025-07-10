import json
import time

log_file = "/home/honeypot-vm/cowrie-logs/cowrie.json"

def detect_failed_logins():
    with open(log_file, "r") as f:
        f.seek(0,2)  # Move to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
                event = json.loads(line)
                if event.get("eventid") == "cowrie.login.failed":
                    print(f"Attack detected from {event.get('src_ip')}")
                    trigger_ip_change(event.get("src_ip"))
            except:
                continue

def trigger_ip_change(attacker_ip):
    print("Triggering IP randomization for honeypot!")
    with open("/tmp/ip_change_flag", "w") as flag:
        flag.write(attacker_ip)

detect_failed_logins()
