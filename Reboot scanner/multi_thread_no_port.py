import ipaddress
import os
import threading
import queue
from datetime import datetime

ping_timeout = 2

def icmp_ping(target):
    response = os.system("ping -c 1 -W {} {} > /dev/null".format(ping_timeout, target))
    return response == 0

def worker():
    while True:
        target = q.get()
        if target is None:
            break
        if icmp_ping(target):
            print("Host {} 활성화 되어 있습니다.".format(target))
        q.task_done()

if __name__ == "__main__":
    start_time = datetime.now()
    q = queue.Queue()
    
    threads = []
    for i in range(30):
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()
        threads.append(t)
    
    ip_input = input("원하는 IP 대역 혹은 원하는 IP를 넣으세요 (ex) 192.168.0.0/24 or 192.168.0.1): ")
    try:
        ip_range = list(ipaddress.IPv4Network(ip_input))
        for host in ip_range:
            q.put(host)
    except ValueError:
        try:
            ipaddress.IPv4Address(ip_input)
            q.put(ip_input)
        except ipaddress.AddressValueError:
            print("올바른 IP대역 혹은 IP를 입력해주세요.")
            exit(1)
    
    q.join()
    
    for i in range(30):
        q.put(None)
    for t in threads:
        t.join()
    end_time = datetime.now()
    
    print("Scanning Completed in : " + str(end_time - start_time))

