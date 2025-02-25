import socket  # noqa: F401


def echo_endpoint(path: str):
    data = path.split("/")[-1]
    return data

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    conn, _addrs = server_socket.accept() 
    if conn:
        data = conn.recv(4096)
        request_line = data.decode().split("\r\n")[0]
        path = request_line.split(" ")[1]
        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif path.startswith("/echo"):
            result = echo_endpoint(path)
            conn.sendall(result.encode())
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
