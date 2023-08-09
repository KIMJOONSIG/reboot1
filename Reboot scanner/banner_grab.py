import requests
import socket

def get_headers_from_ip(ip_address): #ip-api를 활용한 header 정보 수집
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url) #url 요청값
    
    if response.status_code == 200: #응답 코드가 정상일 때
        header_info = response.json() #응답 값을 json 형식으로 반환
        return header_info
    else: #응답 코드가 '200'이 아닌 경우
        print("Failed to fetch header information.")
        return None

def get_hostname_from_domain(ip_address): #hostname 수집
    try:
        hostname = socket.gethostbyaddr(ip_address) #ip주소를 통해 hostnamer 수집
        return hostname
    except socket.herror: #socket 에러 시
        errorlist=['Failed to resolve hostname.']
        return errorlist

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

ip_address = input("Enter an IP address or domain: ") #IP 혹은  domain 정보 입력
header_info = get_headers_from_ip(ip_address) #IP header 수집 함수로 전달
hostname = get_hostname_from_domain(ip_address) #Hostname 수집 함수로 전달

port = input("Enter a port (press Enter to skip): ")  # 포트 번호를 입력 (입력하지 않고 Enter를 누르면 빈 문자열)

if port: #포트 번호가 있을 시
    port = int(port)
    Banner = get_Banner(ip_address, port) #서비스와 해당 서비스 버전 수집하는 함수로 전달
else:
    Banner = None

if header_info: #출력 형태
    print("===== {} Information =====".format(ip_address))
    #print(f"IP Address: {header_info['query']}")
    print(f"Country: {header_info['country']}")
    print(f"Timezone: {header_info['timezone']}")

if hostname:
    print(f"Hostname: {hostname[0]}")

if Banner:
    print(f"Banner: {Banner}")