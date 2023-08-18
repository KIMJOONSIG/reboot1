from scapy.layers.inet import IP, TCP
from scapy.all import sr1
import socket

def ack_scan(target_ip, target_port):
    packet = IP(dst=target_ip) / TCP(dport=target_port, flags="A")
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return False
    elif response.haslayer(TCP):
        if response[TCP]. flags & 4: # RST 플래그가 설정되어 있는지 확인
            return True
        else:
            return False
    else:
        return False

def null_scan(target_ip, target_port):
    if ack_scan(target_ip, target_port)==False: return None
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        
        # 포트 연결 시도
        result = sock.connect_ex((target_ip, target_port))
        
        # FIN, URG, PSH 플래그 비트 설정
        flags = socket.MSG_OOB | socket.MSG_PEEK | socket.MSG_DONTROUTE
        bytes_sent=sock.send(b'', flags)
        # 데이터 전송 (Xmas 패킷)
        
        
        # 응답 받기
        response = sock.recv(1024)
        sock.close()
        if bytes_sent== 1:
            return f"Port {target_port} is open."
        else:
            return None
    except Exception as e:
        
        if "WinError 10045" in str(e):
            return f"Port {target_port} is open."
        else:return None


# NULL 스캔 함수 호출
#print(null_scan("183.111.182.232", 80))  # 예시로 IP 주소와 포트를 수정해서 호출해주세요
#target_ip = "183.111.182.232" # 대상 호스트 IP


# for i in range(1,100):
#     print(null_scan("183.111.182.232",i))