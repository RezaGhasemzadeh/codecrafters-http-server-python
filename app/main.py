import socket
import threading 
import sys
import gzip


CRLF = "\r\n"
METHODS = ["GET", "POST", "PUT", "DELETE", "UPDATE"]
COMPRESSION_SCHEMES_SUPPORTED = ("gzip", )
STATUS_CODES = {200: "OK", 201: "Created", 404: "Not Found", 400: "Bad Request"}


def create_response(status_code=200, body="", headers=None, include_content_encoding=False):
    response_line = f"HTTP/1.1 {status_code} {STATUS_CODES[status_code]}"
    response_headers = ""
    response_body = ""
    if include_content_encoding:
        headers["Content-Encoding"] = "gzip"
        compressed_body = str(gzip.compress(body.encode()))

    if body:
        if include_content_encoding:
            response_body = compressed_body
        else:
            response_body = body

    if headers:
        if "Content-Length" in headers.keys():
            headers["Content-Length"] = str(len(response_body))

        for header_key, header_value in headers.items():
            response_headers += header_key + ":" + header_value + CRLF

    final_response = CRLF.join([response_line, response_headers, response_body]).encode()

    return final_response




def echo_endpoint(path: str, headers):
    content_encoding_header = False

    if "Accept-Encoding" in headers.keys():
        encoding_schemes = headers["Accept-Encoding"][0].split(",")
        for es in encoding_schemes:
            if es.strip() in COMPRESSION_SCHEMES_SUPPORTED:
                content_encoding_header = True
                break
    response_body = path.split("/")[-1]
    response = create_response(status_code=200, headers={"Content-Type": " text/plain", "Content-Length": None}, body=response_body, include_content_encoding=content_encoding_header)
    return response


def user_agent_endpoint(headers):
    response_body = headers["User-Agent"][0]
    response = create_response(status_code=200, headers={"Content-Type": " text/plain", "Content-Length": None}, body=response_body, include_content_encoding=False)
    return response
    
    
def parse_request(request):
    request_info = {"method": "", "path": "", "headers": dict(), "body": ""}
    request_line, *request_headers = request.split(CRLF)

    if request_headers[-1]:
        request_info["body"] = request_headers[-1]

    if request_line.split(" ")[0] in METHODS:
        request_info["method"] = request_line.split(" ")[0]
    else:
        return None
    
    if request_line.split(" ")[1]:
        request_info["path"] = request_line.split(" ")[1]

    else:
        return None
    
    for header in request_headers[0:len(request_headers) - 1]:
        if header:
            header_key = header.split(":")[0]
            header_value = header.split(":")[1].strip()
            request_info["headers"][header_key] = [header_value]

    return request_info


def Get_method_files_endpoint(path):
    direc = sys.argv[2]
    file_name = f"{direc}" + path.split("/")[-1]
    file_content = ""
    print(direc, file_name)
    try:
        with open(file_name, "r") as file:
            file_content = file.read()

        response = create_response(status_code=200, headers={"Content-Type": " application/octet-stream", "Content-Length": None}, body=file_content, include_content_encoding=False)

    except Exception:
        response = create_response(status_code=404, body="", headers=None, include_content_encoding=None)
    return response


def Post_method_file_endpoint(request_body, path):
    direc = sys.argv[2]
    file_name = f"{direc}" + path.split("/")[-1]
    print(direc, file_name)
    try:
        with open(file_name, "w") as file:
            file.write(request_body)
        response = create_response(status_code=201, body="", headers=None, include_content_encoding=None)
    except Exception:
        response = create_response(status_code=400, body="", headers=None, include_content_encoding=None)
    return response


def handle_request(conn):
    data = conn.recv(4096).decode()
    request_info = parse_request(data)
    if not request_info:
        return None

    elif request_info["path"] == "/":
        response = create_response(status_code=200, body="", headers=None, include_content_encoding=None)

    elif request_info["path"].startswith("/echo"):
        response = echo_endpoint(request_info["path"], request_info["headers"])

    elif request_info["path"].startswith("/user-agent"):
        response = user_agent_endpoint(request_info["headers"])

    elif request_info["path"].startswith("/files") and request_info["method"] == "GET":
        response = Get_method_files_endpoint(request_info["path"])

    elif request_info["path"].startswith("/files") and request_info["method"] == "POST":
        response = Post_method_file_endpoint(request_info["body"], request_info["path"])

    else:
        response = create_response(status_code=404, body="", headers=None, include_content_encoding=None)

    conn.sendall(response)
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    while True:
        conn, _addrs = server_socket.accept()
        threading.Thread(target=handle_request, args=(conn,)).start()
        


if __name__ == "__main__":
    main()
