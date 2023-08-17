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
        word=""
        #word+=f"Port : {port}"+'\n'
        #word+=f"Port : {response}"+'\n'
        if response != b'':
            
            if b"SSH" in response:
                word+=f"Port : {port} / SSH"+'\n'  
            elif b"HTTP" in response:
                word+=f"Port : {port} / HTTP"+'\n'
            elif b"SMTP" in response:
                word+=f"Port : {port} / SMTP"+'\n'  
            elif b"MySQL" in response: 
                word+=f"Port : {port} / MySQL"+'\n'
            elif b"FTP" in response:
                word+=f"Port : {port} / FTP"+'\n'
            elif b"+OK" in response:
                word+=f"Port : {port} / POP3"+'\n'

            return word+f"Port {port} is open\n"
        else:
            return None
        
        

    
    except Exception as e:
        return None



