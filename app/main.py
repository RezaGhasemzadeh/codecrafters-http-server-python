import socket  # noqa: F401


def echo_endpoint(path: str):
    response_body = path.split("/")[-1]
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode()
    return response


def user_agent_endpoint(request):
    _, *headers, _ = request.split("\r\n")
    value = ""
    for h in headers:
        if h:
            splitted_header = h.split(":")
            header_key = h[0]
            if header_key == "User-Agent":
                value = splitted_header[1]
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
    return response
    
    

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    conn, _addrs = server_socket.accept() 
    if conn:
        data = conn.recv(4096).decode()
        request_line = data.split("\r\n")[0]
        path = request_line.split(" ")[1]
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo"):
            response = echo_endpoint(path)
        elif path.startswith("/user-agent"):
            response = user_agent_endpoint(data)
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        conn.sendall(response)


if __name__ == "__main__":
    main()
