import socket

#포트 번호와 서비스 매핑
port_services = {
    20: "FTP Data Transfer",
    21: "FTP Control Command",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",
    3389: "RDP",
    5432: "PostgreSQL",
    3306: "MySQL",
    1521: "Oracle",
    27017: "MongoDB",

}

def null_scan(target_ip, target_port):
    try:
        # TCP raw 소켓 생성, 해당 스캔은 별도의 플래그 설정이 없다
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = raw_socket.connect_ex((target_ip, target_port))

        if result == 0:
            service = port_services.get(target_port, "Unknown")
            return f"Port {target_port} ({service}) is open."
        else:
            return f"Port {target_port} is closed or filtered."

    except socket.timeout:
        return f"Port {target_port} is closed."

    except Exception as e:
        return f"Port {target_port} state is unknown. Error: {str(e)}"







