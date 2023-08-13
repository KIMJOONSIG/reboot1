from scapy.layers.inet import IP, TCP
from scapy.all import sr1

def xmas_scan(target_ip, target_port):
    packet = IP(dst=target_ip) / TCP(dport=target_port, flags="FPU")
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return f"Port {target_port} is open or filtered (no response)."
    elif response.haslayer(TCP):
        if response[TCP].flags == 0x14: # RST, ACK 플래그가 설정되어 있는지 확인
            return f"Port {target_port} is closed."
        else:
            return f"Port {target_port} is open or filtered."
    else:
        return f"Received unexpected response for port {target_port}: {response.summary()}"



# Xmas 스캔 함수 호출
  # 예시로 IP 주소와 포트를 수정해서 호출해주세요


#target_ip = "183.111.182.232" # 대상 호스트 IP

#for target_port in range(10001): #0부터 10000까지의 포트 범위

