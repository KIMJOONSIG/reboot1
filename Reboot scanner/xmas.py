import socket

def xmas_scan(target, port):
    try:
        # 소켓 생성
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 타임아웃 설정
        
        # 포트 스캔 시도
        s.connect((target, port))
        
        # XMAS 패킷 생성
        xmas_packet = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

        # 패킷 전송
        s.send(xmas_packet)

        # 응답 확인
        response = s.recv(1024)
        if not response:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
        
        # 소켓 닫기
        s.close()
    except socket.timeout:
        print(f"Port {port} is filtered")
    except ConnectionRefusedError:
        print(f"Port {port} is closed")

# 대상 호스트와 포트 설정
target_host = "127.0.0.1"
target_port = 53

# XMAS 스캔 수행
xmas_scan(target_host, target_port)
