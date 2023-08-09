import ipaddress #ipaddress 모듈을 import하여 IP 주소 및 대역을 다룸
import os # os 모듈을 import하여 운영체제 관련 기능을 사용할 수 있음
import threading # queue 모듈을 import하여 multi threading 기능을 사용할 수 있음
import queue # queue 모듈을 import하여 작업 큐를 사용할 수 있음
from datetime import datetime #datetime 모듈에서 datetime 클래스를 import하여 현재 시간을 기록할 수 있음

ping_timeout = 2 #ICMP ping 타임아웃 시간을 2초로 제한

def icmp_ping(target):           # icmp ping 활용하여 해당 ip 활성여부 점검
    response = os.system("ping -c 1 -W {} {} > /dev/null".format(ping_timeout, target))
    return response == 0 # ping 결과값이 0이면 활성화된 호스트임을 나타냄

def worker(): 
    while True:
        target = q.get() # 작업 대기열에서 IP 주소를 가져옴
        if target is None:
            break
        if icmp_ping(target): # None 값이 들어오면 스레드를 종료함
            print("Host {} 활성화 되어 있습니다.".format(target)) # 활성화된 호스트를 출력
        q.task_done()

if __name__ == "__main__":
    start_time = datetime.now() # 작업 시작 시간을 기록
    q = queue.Queue() # 작업 대기열을 생성함
    
    threads = []
    for i in range(30):
        t = threading.Thread(target=worker) # worker 함수를 스레드의 타겟으로 설정함
        t.setDaemon(True) # 스레드를 백그라운드에서 실행되도록 설정함
        t.start() # 스레드를 시작함
        threads.append(t) # 스레드를 관리하는 리스트에 추가함
    
    ip_input = input("원하는 IP 대역 혹은 원하는 IP를 넣으세요 (ex) 192.168.0.0/24 or 192.168.0.1): ")
    try:
        ip_range = list(ipaddress.IPv4Network(ip_input)) # 입력된 대역을 IP 주소 리스트로 변환함
        for host in ip_range:
            q.put(host) # 작업 대기열에 각 IP 주소를 추가함
    except ValueError:
        try:
            ipaddress.IPv4Address(ip_input) # 입력된 값이 IP 주소인지 확인함
            q.put(ip_input) # IP 주소이면 작업 대기열에 추가함
        except ipaddress.AddressValueError:
            print("올바른 IP대역 혹은 IP를 입력해주세요.")
            exit(1) # 유효하지 않은 입력이면 프로그램을 종료함
    
    q.join() # 모든 작업이 완료될 때까지 대기함
    
    for i in range(30):
        q.put(None) # None 값을 작업 대기열에 추가해 스레드를 종료함
    for t in threads:
        t.join() # 모든 스레드가 종료도리 때까지 대기함
    end_time = datetime.now() # 작업 종료 시간을 기록함
    
    print("Scanning Completed in : " + str(end_time - start_time)) # 작업 시간을 출력

