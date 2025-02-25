import socket


CRLF = "\r\n"
METHODS = ["GET", "POST", "PUT", "DELETE", "UPDATE"]
STATUS_CODES = {404: "Not Found", 200: "OK"}


def echo_endpoint(path: str):
    response_body = path.split("/")[-1]
    response = create_response(200, response_body)
    return response


def user_agent_endpoint(headers):
    response_body = headers["User-Agent"][0]
    response = create_response(200, response_body)
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
    
    
def create_response(status_code=200, body=None):
    response_line = f"HTTP/1.1 {status_code} {STATUS_CODES[status_code]}"
    headers = ""
    if body:
        headers = f"Content-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    response = CRLF.join([response_line, headers]).encode()
    return response


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    while True:
        conn, _addrs = server_socket.accept()
        data = conn.recv(4096).decode()
        request_info = parse_request(data)
        if not request_info:
            break

        elif request_info["path"] == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"

        elif request_info["path"].startswith("/echo"):
            response = echo_endpoint(request_info["path"])

        elif request_info["path"].startswith("/user-agent"):
            response = user_agent_endpoint(request_info["headers"])

        else:
            response = create_response(404, body=None)

        conn.sendall(response)


if __name__ == "__main__":
    main()
