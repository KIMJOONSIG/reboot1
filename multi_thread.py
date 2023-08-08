from datetime import datetime
import queue
import threading
import ipaddress
import socket
import os

ports = {21, 22, 80, 5000, 7000}
ping_timeout = 3

def scanner(target):
    #pimg 명령으로 해당 호스트 활성 여부 점검
    alive = os.system("ping -c 1 -W {} {} > /dev/null".format(ping_timeout, target))
    if alive == 0: #ping 명령어에 대한 응답이 성공하면 0 변환
        #작업 시간 및 로그 기록
        timelog = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timelog + ": target host " + str(target) + " 활성화 되어 있습니다.")
        #포트 스캔 실시
        open_ports = [] #개발된 포트를 저장할 리스트 생성

        for port in ports: #진단할 포트 목록 순회
            #소켓 생성
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #해당 IP 대상으로 포트 점검
            result = sock.connect_ex((str(target), port))
            #0이 반환되면 개방된 포트라는 의미
            if result == 0:
                open_ports.append(port)
            sock.close()

        if open_ports:        
            print("---------->> Open Ports " + ", ".join(map(str, open_ports)))
        else:
            print("열린 포트 없음.")
            #현재의 소켓 연결을 닫고 다음 포트 스캔 수행

def worker(): #스레드가 수행할 작업을 명시하는 함수
    while True: #무한 루프로 작업 대기열의 모든 작업을 반복 처리
        #작업 대기실에서 호스트 IP를 하나씩 가져와 표적 삼음
        target = q.get()
        #유효하지 않은 호스트인 경우 루프를 탈출하고 스레드 종료
        if target is None:
            break
        scanner(target)
        #해당 호스트에 대한 스캔 작업을 완료했다는 task_done 선호
        q.task_done()

if __name__ == "__main__":
    start_time = datetime.now() #작업 시작 시간 기록

    #큐 자료 구조를 사용해 작업 대기열을 생성
    q = queue.Queue()

    #스레드를 30개 생성
    threads = []
    for i in range(30):
        #각 스레드가 함수를 수행하도록 설정
        t = threading.Thread(target=worker)
        #스레드가 백그라운드에서 실행되도록 데몬으로 지정
        t.setDaemon(True)
        #해당 스레드 작업을 실시
        t.start()
        #스레드 관리 목록에 저장
        threads.append(t)

    ip_input = input("원하는 IP 대역 혹은 원하는 IP를 넣으세요 (ex) 192.168.0.0/24 or 192.168.0.1): ")
    try:
        ip_range = list(ipaddress.IPv4Network(ip_input))
        for host in ip_range: #범위 내의 모든 IP에 대해 점검 실시
            q.put(host) #해당 호스틑 IP를 작업 대기열에 추가
    except ValueError: #입력이 IP 대역이 아닌 개별 IP인 경우
        try:
            ipaddress.IPv4Address(ip_input) # 입력이 유효한 ip인지 확인
            q.put(ip_input)
        except ipaddress.AddressValueError:
            print("올바른 IP대역 혹은 IP를 입력해주세요.")
            exit(1)
    #대기열에 추가돼 있는 작업들이 모두 완료될 때까지 대기
    q.join()

    #스레드 파괴 작업
    for i in range(30):
        q.put(None) #대기열에 빈 작업을 할당해 정리
    for t in threads: #진행 중이던 모든 스레드가 전부 종료될 때까지 대기
        t.join()
    end_time = datetime.now() #작업 종료 시간 기록

    #종료 메시지와 수행 시간 표출
    print("Scanning Completed in : " + str(end_time - start_time))