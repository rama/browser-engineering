import socket
import ssl


class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        self.host, url = url.split("/", 1)

        if ":" in self.host:
            self.host, port = self.host.split(":")
            self.port = int(port)
        elif self.scheme == "https":
            self.port = 443
        else:
            self.port = 80
        if len(url) > 0:
            if url[0] != "/":
                self.path = "/" + url
            else:
                self.path = url
        else:
            self.path = "/"
        print(self.scheme, self.host, self.port, self.path)

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        s.connect((self.host, self.port))

        request = f"GET {self.path} HTTP/1.1\r\n"
        request += f"Host: {self.host}\r\n"
        request += f"Connection: close\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        print(version, status, explanation)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        s.close()
        return content

    def lex(self, body):
        text = ""
        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif not in_tag:
                text += c
        return text


def load(url):
    body = url.request()
    print(url.lex(body))


if __name__ == "__main__":
    import sys

    load(URL(sys.argv[1]))
