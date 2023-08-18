import socket

def half_scan(target_ip, target_port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 타임아웃 설정 (0.5초로 설정, 연결을 기다리지 않음)
        sock.settimeout(0.5)
        # 포트에 연결 시도
        result = sock.connect_ex((target_ip, target_port))
        
        if result == 0:
            return f"Port {target_port} is OPEN"
        else:
            return None

        

    except socket.error:
        return None


