import socket
from telnetlib import Telnet


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def read_until(s, delim=b':'):
    buf = b''
    while not buf.endswith(delim):
        buf += s.recv(1)
    return buf


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('<address here>', 5300))
    data = read_until(sock, delim=b'? ')
    for line in data.decode('ascii').splitlines():
        print(line)
        if "I ran" in line:
            miles = line.split()[2]
            runtime = line.split()[4]
            min_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(get_sec(runtime)/int(miles), 60))
            pace = str(min_time) + ' minutes/mile\n'
            # pace = str(min_time)
            pace = bytes(pace, encoding='utf-8')
            print('sending:', pace)
            sock.send(pace)
            sock.sendall(b'\n')
            t = Telnet()
            t.sock = sock
            t.interact()
    sock.close()


# ===== Main
if __name__ == "__main__":
    main()

