import socket
import ssl
import sys

def start_client():
    s = socket.socket()
    server_ip = input("Enter server IP address: ")
    port = 9999

    try:
        s.connect((server_ip, port))
        print("Connected to server.")

    except socket.error as msg:
        print("Connection failed. Error:", str(msg))
        sys.exit()

    # Create SSL context with cert_reqs
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE  # Set the desired verification mode

    # Wrap the socket with SSL
    s = ssl_context.wrap_socket(s, server_hostname=server_ip)

    while True:
        cmd = input("Enter a command (or 'quit' to exit): ")
        if cmd == 'quit':
            s.send(str.encode("quit"))
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            s.send(str.encode(cmd))
            server_response = str(s.recv(1024), "utf-8")
            print(server_response, end="")

if __name__ == "__main__":
    start_client()
