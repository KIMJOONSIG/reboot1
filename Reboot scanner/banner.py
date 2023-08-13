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
def get_Banner(ip_address, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip_address, port))
        Banner = sock.recv(1024).decode('utf-8')
        sock.close()
        return Banner
    except (socket.timeout, ConnectionRefusedError):
        return "Connection failed."

# IP 주소와 포트를 이용하여 정보를 수집하는 함수
def get_information(ip_address, port=None):
    # IP 주소로부터 헤더 정보 수집
    header_info = get_headers_from_ip(ip_address)
    # IP 주소로부터 호스트네임 수집
    hostname = get_hostname_from_domain(ip_address)
    Banner = get_Banner(ip_address, int(port)) if port else None
    
    # 포트가 제공된 경우, 포트를 사용하여 서비스 배너 정보 수집
    if port: #포트 번호가 있을 시
        port = int(port)
        Banner = get_Banner(ip_address, port) #서비스와 해당 서비스 버전 수집하는 함수로 전달
    else:
        Banner = None
        
    word=""
        
    if header_info:
        word=word+f"Country: {header_info['country']}"+"\n"
        word=word+f"Timezone: {header_info['timezone']}"+"\n"
    if hostname:
        word=word+f"Hostname: {hostname[0]}"+"\n"
    if Banner:
        word=word+f"Banner: {Banner}"+"\n"

    
    
    return word

#print(get_information("183.111.182.232",80))