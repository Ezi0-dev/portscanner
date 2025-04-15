import socket
import time

target = input("Enter the IP address you wish to scan: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print (f"\nScanning {target} from port {start_port} to {end_port}...\n")
start_time = time.time()

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    result = s.connect_ex((target, port))
    if result == 0:
        print (f"Port {port} is OPEN")
    s.close()

end_time = time.time()
print(f"\nScan finished in {round(end_time - start_time, 2)} seconds")