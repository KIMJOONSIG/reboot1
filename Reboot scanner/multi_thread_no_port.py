import ipaddress
import os
import threading
import queue
from datetime import datetime

ping_timeout = 2

def icmp_ping(target):
    response = os.system("ping -c 1 -W {} {} > /dev/null".format(ping_timeout, target))
    return response

def worker(q, results):
    while True:
        target = q.get()
        if target is None:
            break
        if icmp_ping(target):
            results.append("Host {} 활성화 되어 있습니다.".format(target))
        else:
            results.append("Host {} 활성화 되어 있지 않습니다.".format(target))
        q.task_done()

def ping_scan(ip_input):
    start_time = datetime.now()
    q = queue.Queue()
    results = []

    threads = []
    for i in range(30):
        t = threading.Thread(target=worker, args=(q, results))
        t.setDaemon(True)
        t.start()
        threads.append(t)
    
    try:
        ip_range = list(ipaddress.IPv4Network(ip_input))
        if "/" in ip_input:
            for host in ip_range:
                q.put(str(host))  # ipaddress.IPv4Network 객체를 문자열로 변환하여 큐에 추가
        else:
            q.put(ip_input)
    except ValueError:
        try:
            ipaddress.IPv4Address(ip_input)
            q.put(ip_input)
        except ipaddress.AddressValueError:
            return "올바른 IP대역 혹은 IP를 입력해주세요."
    
    q.join()

    # 스레드 종료 신호 보내기
    for _ in range(30):
        q.put(None)
    for t in threads:
        t.join()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    word=""
    for result in results:
        word=word+result+"\n"
        
    
    return word+"Scanning Completed in: " + str(duration)