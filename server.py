import socket
import os
import subprocess
import DNS.cache_data as c_data
import DNS.cache as c
import time

IP = 'localhost'
PORT = 53

if __name__ == "__main__":
    os.popen("chcp 65001")
    cache = c.Cache()
    cache.create()
    run = True
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((IP, PORT))
        print("Server is running...")
        while(run):
            try:
                conn, addr = s.recvfrom(1024)
            except Exception:
                continue
            request = bytes.decode(conn)
            if request in cache.ip_data.keys():
                data = cache.get_data_by_ip(request)
                answer = data.data
            elif request in cache.domein_name_data.keys():
                data = cache.get_data_by_name(request)
                answer = data.data
            else:
                try:
                    process = subprocess.Popen(["nslookup", "-query=SOA", request], stdout=subprocess.PIPE)
                    answer = process.communicate()[0]
                except Exception:
                    s.sendto(answer, addr)
                    continue
                output = str(answer).split('\\r\\n')
                ttl = 0
                for i in output:
                    if "ttl" in i.lower():
                        ttl = i.split('=')[1].split(' ')[1]
                data = c_data.cache_data(ttl, answer, time.time())
                if ttl != 0:
                    cache.add_data_by_name(request, data)
                    cache.save()
            #print(output)
            s.sendto(answer.decode().encode(), addr)


