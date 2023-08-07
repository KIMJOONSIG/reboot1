from myscanner import portscan
from SYNscan import syn_scan
from FINscan import fin_scan
from NULLscan import null_scan
import threading
import concurrent.futures
import pyfiglet as f
import socket
import sys

# console font
print(f.figlet_format('Reboot', font='slant'))
print("Copyright © team Reboot\n")

def main():
    numbers = range(0, 10000)
    num_threads = 100

    try:
        # input host
        target_host = input('Input target Host : ')
        target_ip = socket.gethostbyname(target_host)
        
        # select scanning type
        scan_type = ''
        while scan_type != 'default' and scan_type != 'SYN' and scan_type != 'FIN' and scan_type != 'NULL':
            scan_type = input('Select scanning type [default/SYN/FIN/NULL] : ')
        
        # scanning 
        print(f"\nScanning target : {target_ip}")
        if scan_type == 'default':
            with concurrent.futures.ThreadPoolExecutor(max_workers = num_threads) as executor:
                futures = [executor.submit(portscan, target_ip, number) for number in numbers]

                for future in concurrent.futures.as_completed(futures): 
                    result = future.result()

                    if "open" in result:
                        print(result)

        if scan_type == 'SYN':
            with concurrent.futures.ThreadPoolExecutor(max_workers = num_threads) as executor:
                futures = [executor.submit(syn_scan, target_ip, number) for number in numbers]

                for future in concurrent.futures.as_completed(futures): 
                    result = future.result()

                    if "open" in result:
                        print(result)
            print(result)

        if scan_type == 'FIN':
            with concurrent.futures.ThreadPoolExecutor(max_workers = num_threads) as executor:
                futures = [executor.submit(fin_scan, target_ip, number) for number in numbers]

                for future in concurrent.futures.as_completed(futures): 
                    result = future.result()

                    if "open" in result:
                        print(result)
            print(result)

        if scan_type == 'NULL':
            with concurrent.futures.ThreadPoolExecutor(max_workers = num_threads) as executor:
                futures = [executor.submit(null_scan, target_ip, number) for number in numbers]

                for future in concurrent.futures.as_completed(futures): 
                    result = future.result()

                    if "open" in result:
                        print(result)
            print(result)
             
    except KeyboardInterrupt:
        print("Exit Program")
        sys.exit()


if __name__ == "__main__":
    main()