import socket
import threading 
import sys


CRLF = "\r\n"
METHODS = ["GET", "POST", "PUT", "DELETE", "UPDATE"]


def echo_endpoint(path: str):
    response_body = path.split("/")[-1]
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-length: {len(response_body)}\r\n\r\n{response_body}".encode()
    return response


def user_agent_endpoint(headers):
    response_body = headers["User-Agent"][0]
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode()
    return response
    
    
def parse_request(request):
    request_info = {"method": "", "path": "", "headers": dict(), "body": ""}
    request_line, *request_headers = request.split(CRLF)

    if request_line.split(" ")[0] in METHODS:
        request_info["method"] = request_line.split(" ")[0]
    else:
        return None
    
    if request_line.split(" ")[1]:
        request_info["path"] = request_line.split(" ")[1]

    else:
        return None
    
    for header in request_headers:
        if header:
            header_key = header.split(":")[0]
            header_value = header.split(":")[1].strip()
            request_info["headers"][header_key] = [header_value]

    return request_info


def files_endpoint(path):
    direc = sys.argv[2]
    file_name = f"/{direc}/" + path.split("/")[-1]
    file_content = ""
    with open(file_name, "r") as file:
        file_content = file.read()

    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content}".encode()
    return response


def handle_request(conn):
    data = conn.recv(4096).decode()
    request_info = parse_request(data)
    if not request_info:
        return None

    elif request_info["path"] == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()

    elif request_info["path"].startswith("/echo"):
        response = echo_endpoint(request_info["path"])

    elif request_info["path"].startswith("/user-agent"):
        response = user_agent_endpoint(request_info["headers"])

    elif request_info["path"].startswith("/files"):
        response = files_endpoint(request_info["path"])

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    conn.sendall(response)
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    while True:
        conn, _addrs = server_socket.accept()
        threading.Thread(target=handle_request, args=(conn,)).start()
        


if __name__ == "__main__":
    main()
