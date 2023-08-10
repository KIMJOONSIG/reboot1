import socket
import random
import sys


def null_scan(target_ip, target_port):
    try:
        # TCP raw 소켓 생성, 해당 스캔은 별도의 플래그 설정이 없다
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = raw_socket.connect_ex((target_ip, target_port))

        if result == 0:
            return f"Port {target_port} is open."
        else:
            return f"Port {target_port} is closed or filtered."

    except socket.timeout:
        return f"Port {target_port} is closed."

    except Exception as e:
        return f"Port {target_port} state is unknown. Error: {str(e)}"