import tkinter as tk
from tkinter import scrolledtext
import socket
import os
import subprocess
import sys
import ssl

def isDataSafe(command):
    allowed_commands = ['dir', 'echo', 'type', 'mkdir', 'del', 'ipconfig']

    if 'sudo' in command:
        print("Error: Command contains 'sudo'. Not allowed.")
        return False

    if command.split()[0] not in allowed_commands:
        print("Error: Command not allowed.")
        return False

    return True

def start_server(host, port):
    s = socket.socket()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # Replace with your actual certificate and key files

    s.bind((host, port))
    s.listen(5)

    print("Server listening on port:", port)

    conn, addr = s.accept()
    print("Connection established with:", addr)

    try:
        # Wrap the socket with SSL
        conn = ssl_context.wrap_socket(conn, server_side=True)
        print("SSL handshake completed successfully.")
    except ssl.SSLError as e:
        print("SSL handshake failed:", e)
        conn.close()
        sys.exit()

    currentWD = os.getcwd() + "> "
    conn.send(str.encode(currentWD))

    while True:
        data = conn.recv(1024)
        if data[:5].decode("utf-8") == 'quit':
            print("Exiting...")
            conn.close()
            sys.exit()
        if len(data) > 0 and isDataSafe(data.decode("utf-8")):
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            currentWD = os.getcwd() + "> "
            conn.send(str.encode(output_str + currentWD))
            print(output_str)

def on_start_server_click():
    host = host_entry.get()
    port = int(port_entry.get())
    start_server(host, port)

# Create the GUI
root = tk.Tk()
root.title("Server GUI")

# Host entry
host_label = tk.Label(root, text="Host:")
host_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
host_entry = tk.Entry(root)
host_entry.grid(row=0, column=1, padx=5, pady=5)

# Port entry
port_label = tk.Label(root, text="Port:")
port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=5, pady=5)

# Start server button
start_server_button = tk.Button(root, text="Start Server", command=on_start_server_click)
start_server_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Output text area
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()
