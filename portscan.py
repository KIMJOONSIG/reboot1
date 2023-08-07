import socket
# 스캔할 호스트 및 포트 범위 설정
target_host = 'localhost' # 대상 호스트
start_port = 1 # 스캔 시작 포트
end_port = 100 # 스캔 종료 포트
# 포트 스캔 함수
def scan_port(host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 타임아웃 설정 (1초)
        sock.settimeout(1)
        # 포트 스캔 시도
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Couldn't connect to server.")
        sys.exit()
# 메인 함수
def main():
    try:
        # 호스트 이름 확인
        target_ip = socket.gethostbyname(target_host)
        print(f"Scanning target: {target_ip}\n")
        # 포트 스캔 반복
        for port in range(start_port, end_port + 1):
            scan_port(target_ip, port)
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
if __name__ == '__main__':
    main()