import socket
import random

def fin_scan(target_ip, port):
    try:
        # TCP raw 소켓 생성
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # FIN 패킷 구성
        ip_header = b"\x45\x00\x00\x28" # IP 헤더 (Version, IHL, TOS, Total Length)
        ip_header += b"\x00\x00\x40\x00" # IP 헤더 (Identification, Flags, Fragment Offset)
        ip_header += b"\x40\x06\x00\x00" # IP 헤더 (TTL, Protocol, Header Checksum)
        ip_header += b"\x00\x00\x00\x00" # IP 헤더 (Source IP)

        # IP 문자열을 이진형태로 변환하여 헤더에 추가
        ip_header += socket.inet_aton(target_ip) # IP 헤더 (Destination IP)


        tcp_header = b"\x00\x00" + port.to_bytes(2, "big") # TCP 헤더 (Source Port)
        tcp_header += port.to_bytes(2, "big") # TCP 헤더 (Destination Port)
        tcp_header += b"\x00\x00\x00\x00" # TCP 헤더 (Sequence Number)
        tcp_header += b"\x00\x00\x00\x00" # TCP 헤더 (Acknowledgment Number)
        tcp_header += b"\x50\x01\x00\x00" # TCP 헤더 (Data Offset, Flags, Window Size)
        tcp_header += b"\x00\x00\x00\x00" # TCP 헤더 (Checksum, Urgent Pointer)

        # 패킷 전송
        raw_socket.sendto(ip_header + tcp_header, (target_ip, port))

        # 응답 처리
        response, _ = raw_socket.recvfrom(4096)

        if response:
            tcp_flags = int.from_bytes(response[33:34], "big")
            if tcp_flags == 20: # RST 응답 확인
                return f"Port {port} is closed."
            
        return f"Port {port} is open or filtered."
    
    except socket.timeout:
        return f"Port {port} is filtered."
    except Exception as e:
        return f"Port {port} state is unknown. Error: {str(e)}"


