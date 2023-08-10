import socket
import random

def fin_scan(target_ip, port):
    try:
        # TCP raw 소켓 생성
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        tcp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        source_port = random.randint(1024, 65535) # 랜덤한 소스 포트 선택

        # FIN 패킷 구성
        source_port = 777
        tcp_packet = b"\x00\x00" + source_port.to_bytes(2, "big")  # TCP 헤더 (Source Port)
        tcp_packet += port.to_bytes(2, "big")  # TCP 헤더 (Destination Port)
        tcp_packet += b"\x00\x00\x00\x00"  # TCP 헤더 (Sequence Number)
        tcp_packet += b"\x00\x00\x00\x00"  # TCP 헤더 (Acknowledgment Number)
        tcp_packet += b"\x50\x01\x00\x00"  # TCP 헤더 (Data Offset, Flags, Window Size)
        tcp_packet += b"\x00\x00\x00\x00"  # TCP 헤더 (Checksum, Urgent Pointer)

        # 패킷 전송 및 타임아웃 설정
        tcp_socket.settimeout(2)
        tcp_socket.connect((target_ip, port))
        tcp_socket.send(tcp_packet)

        # 응답 처리
        response = tcp_socket.recv(4096)
        tcp_socket.close()

        if response == b'':
            return f"Port {port} is open"
            
        return f"Port {port} is open or filtered."
    
    except socket.timeout:
        return f"Port {port} is filtered."
    except Exception as e:
        return f"Port {port} state is unknown. Error: {str(e)}"

def  main():
    target_ip = input("Enter the target IP address: ")
    ports_to_scan = [80, 443, 8080]  # 스캔하려는 포트 목록
    
    print(f"Scanning target: {target_ip}")
    for port in ports_to_scan:
        result = fin_scan(target_ip, port)
        print(result)

if __name__ == "__main__":
    main()


