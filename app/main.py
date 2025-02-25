import socket  # noqa: F401


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    conn, _addrs = server_socket.accept() 
    if conn:
        data = conn.recv(1024)
        request_line = data.decode().split("\r\n")[0]
        path = request_line.split(" ")[1]
        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\b")
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
