import socket  # noqa: F401


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    conn, _addrs = server_socket.accept() 
    if conn:
        conn.sendall(b"HTTP/1.1 200 OK\r\n")


if __name__ == "__main__":
    main()
