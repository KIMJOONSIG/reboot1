from scapy.layers.inet import IP, TCP
from scapy.all import *

def fin_scan(target_ip, port_range):
    for port in port_range:
        # FIN 플래그가 설정된 TCP 패킷 생성
        packet = IP(dst=target_ip) / TCP(dport=port, flags="F")

        # 패킷 전송하고 응답 받기
        response = sr1(packet, timeout=1, verbose=0)

        if response:
            tcp_layer = response.getlayer(TCP)
            # RST 플래그가 설정된 응답이면 포트가 닫혀 있음
            if tcp_layer and tcp_layer.flags == 0x4:
                print(f"Port {port} is closed.")
            else: 
                print(f"Port {port} is filtered.")
        else:
            print(f"Port {port} is filtered.")
        
if __name__=="__main__":
    target_ip = "183.111.182.232"
    port_range = range(1, 10001)
    fin_scan(target_ip, port_range)