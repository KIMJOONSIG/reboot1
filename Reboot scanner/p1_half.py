from scapy.layers.inet import IP, TCP
from scapy.all import sr1, send

def half_scan(target_ip, target_port):
    # SYN 플래그를 설정하여 패킷 생성
    packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return f"Port {target_port} is filtered or no response."
    elif response.haslayer(TCP):
        if response[TCP].flags == 0x12:  # SYN, ACK 플래그가 설정된 응답 확인
            send_rst = IP(dst=target_ip) / TCP(dport=target_port, flags="R")
            send(send_rst)  # RST 패킷 전송
            return f"Port {target_port} is open."
        elif response[TCP].flags == 0x14:  # RST 플래그만 설정된 응답 확인
            return f"Port {target_port} is closed."
        else:
            return f"Port {target_port} is filtered or no response."
    else:
        return f"Port {target_port} is filtered or no response."




