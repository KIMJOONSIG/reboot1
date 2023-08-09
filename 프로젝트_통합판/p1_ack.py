from scapy.layers.inet import IP, TCP
from scapy.all import sr1

def ack_scan(target_ip, target_port):
    packet = IP(dst=target_ip) / TCP(dport=target_port, flags="A")
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return f"port {target_port} is filtered (no response)."
    elif response.haslayer(TCP):
        if response[TCP]. flags & 4: # RST 플래그가 설정되어 있는지 확인
            return f"Port {target_port} is unfiltered (received RST)."
        else:
            return f"Port {target_port} response was unexpected: {response[TCP].flags}"
    else:
        return f"Received unexpected response for port {target_port}: {response.summary()}"

#target_ip = "183.111.182.232" # 대상 호스트 IP

#for target_port in range(10001): #0부터 10000까지의 포트 범위
