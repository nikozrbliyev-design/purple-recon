import socket
import threading
from queue import Queue
import sys

print("="*45)
print("   PurpleEye v1.0 - Banner Grabber & Scanner")
print("="*45)

target = input("[+] Hədəf İP və ya Domain: ")
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[-] Qeyri-vaqif domain!")
    sys.exit()

print(f"[*] Skan edilir: {target_ip}")

print_lock = threading.Lock()
queue = Queue()

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            try:
                s.send(b"Hello\r\n")
                banner = s.recv(1024).decode().strip('\n\r')
                banner_info = f" -> Banner: {banner}"
            except:
                banner_info = " -> Banner tapılmadı"
                
            with print_lock:
                print(f"[+] Port {port} AÇIQ {banner_info}")
        s.close()
    except:
        pass

def threader():
    while True:
        worker = queue.get()
        scan_port(worker)
        queue.task_done()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8080]
for port in common_ports:
    queue.put(port)

queue.join()
print("\n[*] Skan bitdi!")
