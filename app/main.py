import socket  # noqa: F401
import requests


def echo_endpoint(path: str):
    response_body = path.split("/")[-1]
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
    return response
    

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
            server_response = echo_endpoint(path)
            conn.sendall(server_response.encode())
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
