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
            return f"Port {port} is open"
        else:
            return f"Port {port} is closed"
        
        # 소켓 닫기
        s.close()
    except socket.timeout:
        return f"Port {port} is filtered"
    except ConnectionRefusedError:
        return f"Port {port} is closed"


