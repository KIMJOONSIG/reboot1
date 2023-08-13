from scapy.layers.inet import IP, TCP
from scapy.all import sr1

def fin_scan(target_ip, target_port):
    packet = IP(dst=target_ip) / TCP(dport=target_port, flags="F")
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return f"Port {target_port} is open or filtered."
    elif response.haslayer(TCP):
        if response[TCP].flags == 0x14:  # RST, ACK 플래그가 설정된 응답 확인
            return f"Port {target_port} is closed."
        else:
            return f"Port {target_port} is open or filtered."
    else:
        return f"Port {target_port} is open or filtered."

# FIN 스캔 함수 호출
#print(fin_scan("127.0.0.1", 80))  # 예시로 IP 주소와 포트를 수정해서 호출해주세요



