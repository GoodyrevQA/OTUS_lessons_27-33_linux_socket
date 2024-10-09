import socket
import random
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = "127.0.0.1"
PORT = random.randint(10000, 20000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print(f"Binding server on {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:

        conn.send("Hello, I am server!".encode("utf-8"))

        while True:

            data = conn.recv(1024)
            print("Received", data, "from", addr)

            if not data or data == b"close":
                print("Got termination signal", data, "and closed connection")
                conn.close()

            # Get message and revert it and send it back
            data = data.decode("utf-8")[::-1]
            conn.send(data.encode("utf-8"))

            # Log message what we send back
            logging.info(f"Sent '{data}' to {addr}")

