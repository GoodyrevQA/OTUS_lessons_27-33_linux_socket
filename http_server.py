import socket
import re
import random


def random_port():
    return random.randint(20000, 30000)


CODES = {
    200: 'OK',
    201: 'CREATED',
    400: 'BAD_REQUEST',
    404: 'NOT_FOUND',
    500: 'INTERNAL_SERVER_ERROR',
    503: 'SERVICE_UNAVAILABLE'
}


# Create a TCP server socket
end_of_stream = '\r\n\r\n'

def handle_client(connection, client_addr):
    client_data = ''
    with connection:
        for _ in range(10**6):
            data = connection.recv(1024)

            if not data:
               break
            client_data += data.decode()

            ans = client_data.strip()
            ans = ans.split('\r\n')
            rm = re.search(r"(?P<method>[A-Z]+) ", ans[0])
            request_method = rm.group('method')

            st = re.search(r"status=(?P<status>\d+) ", ans[0])
            if st:
                status = int(st.group('status'))
            else:
                status = 200

            if end_of_stream in client_data:
                break

        http_response = f"HTTP/1.0 {status} {CODES[status]}\r\n\r\n"
        http_response += f'Request Method: {request_method}\r\n'
        http_response += f'Request Source: {client_addr}\r\n'
        http_response += f'Response Status: {status} {CODES[status]}\r\n'

        for hdr in ans[2:]:
            http_response += f"{hdr}\r\n"
        
        http_response += f"\r\n"

        connection.sendall(http_response.encode())


with socket.socket() as server_socket:
    # Bind the tcp socket to an IP and port

    some_random_port = random_port()
    print('listening port:', some_random_port)

    server_socket.bind(("127.0.0.1", some_random_port))
    # Keep listening
    server_socket.listen()

    while True: # Keep accepting connections from clients
        (client_connection, client_address) = server_socket.accept()
        handle_client(client_connection, client_addr=client_address)
