import requests
import socket

# IP 주소로부터 헤더 정보를 가져오는 함수
def get_headers_from_ip(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        header_info = response.json()
        return header_info
    else:
        return None

# IP 주소로부터 호스트네임을 가져오는 함수
def get_hostname_from_domain(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return ['Failed to resolve hostname.']

# IP 주소와 포트로부터 서비스 배너 정보를 가져오는 함수
def get_banner(ip_address, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip_address, port))
        banner = sock.recv(1024).decode('utf-8')
        sock.close()
        return banner
    except (socket.timeout, ConnectionRefusedError):
        return "Connection failed."

# IP 주소와 포트를 이용하여 정보를 수집하는 함수
def get_information(ip_address, port=None):
    # IP 주소로부터 헤더 정보 수집
    header_info = get_headers_from_ip(ip_address)
    # IP 주소로부터 호스트네임 수집
    hostname = get_hostname_from_domain(ip_address)
    banner = None
    
    # 포트가 제공된 경우, 포트를 사용하여 서비스 배너 정보 수집
    if port is not None:
        port = int(port)
        banner = get_banner(ip_address, port)
    
    return header_info, hostname, banner
