import socket
import random
import sys

def syn_scan(target_ip, port):
    try:
        # TCP 소켓 생성
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SYN 패킷 구성
        source_port = 777
        tcp_packet = b"\x00\x00" + source_port.to_bytes(2, "big")  # TCP 헤더 (Source Port)
        tcp_packet += port.to_bytes(2, "big")  # TCP 헤더 (Destination Port)
        tcp_packet += b"\x00\x00\x00\x00"  # TCP 헤더 (Sequence Number)
        tcp_packet += b"\x00\x00\x00\x00"  # TCP 헤더 (Acknowledgment Number)
        tcp_packet += b"\x50\x02\x00\x00"  # TCP 헤더 (Data Offset, Flags, Window Size)
        tcp_packet += b"\x00\x00\x00\x00"  # TCP 헤더 (Checksum, Urgent Pointer)

        # 패킷 전송 및 타임아웃 설정
        tcp_socket.settimeout(2)
        tcp_socket.connect((target_ip, port))
        tcp_socket.send(tcp_packet)

        # 응답 처리
        response = tcp_socket.recv(4096)
        tcp_socket.close()
        print(port)
        print(response)
        if response != b'':
            print(port)
            print(response)
            if b"SSH" in response:
                print(f"Port : {port} / SSH")    
            elif b"HTTP" in response:
                print(f"Port : {port} / HTTP")
            elif b"SMTP" in response:
                print(f"Port : {port} / SMTP")    
            elif b"MySQL" in response: 
                print(f"Port : {port} / MySQL")
            elif b"FTP" in response:
                print(f"Port : {port} / FTP")
            elif b"+OK" in response:
                print(f"Port : {port} / POP3")

            return f"Port {port} is open\n{response}"
        else:
            return f"Port {port} is closed\n{response}"
        
        

    
    except Exception as e:
        return f"Port {port} state is unknown. Error: {str(e)}"

