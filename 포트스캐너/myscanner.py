import socket
import sys

def portscan(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)

        result = sock.connect_ex((host, port))
        if result == 0:
            sock.close()
            return f"Port {port} is open"
        else:
            sock.close()
            return ""

    except KeyboardInterrupt:
        print("Exit Program")
        sys.exit()
    except socket.gaierror:
        print("Host is not invalid")
        sys.exit()
    except socket.error:
        print("Could not connect to server")
        sys.exit()


            
