from scapy.all import IP, TCP, sr1

def scan_firewall(target_ip, target_port):
    # TCP SYN 스캔 수행
    syn_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
    syn_response = sr1(syn_packet, timeout=1, verbose=0)

    if syn_response is not None and syn_response.haslayer(TCP) and syn_response[TCP].flags == 0x12: # SYN-ACK 응답
        print(f"Port {target_port} is open.")
    else:
        print(f"Port {target_port} is closed or filtered.")

    # ACK 스캔 수행
    ack_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="A")
    ack_response = sr1(ack_packet, timeout=1, verbose=0)

    if ack_response is None:
        print(f"Port {target_port} is likely filtered by a firewall (no response to ACK).")
    elif ack_response[TCP].flags & 4: # RST 응답
        print(f"Port {target_port} is unfiltered (received RST).")
    else:
        print(f"Port {target_port} response was unexpected: {ack_response[TCP].flags}")

target_ip = "183.111.182.232" # 대상 호스트 IP
target_ports = range(10001) # 0부터 10000까지의 포트 범위

for target_port in target_ports:
    scan_firewall(target_ip, target_port)
