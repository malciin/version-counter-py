from http.server import BaseHTTPRequestHandler
from version_maintainer import VersionMaintainer

class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, version_maintainer: VersionMaintainer):
        self.__version_maintainer = version_maintainer
    
    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)

    def do_POST(self):
        print('POST')
        prefix = self.__read_body()
        version = self.__version_maintainer.get_version_number(prefix)

        self.__send_text(str(version) + '\r\n')

    def do_PATCH(self):
        prefix = self.__read_body()
        version = self.__version_maintainer.bump_version_number(prefix)

        self.__send_text(f"Next version for '{prefix}' will be '{version}'" + '\r\n')

    def __read_body(self) -> str:
        body_length = self.headers.get('Content-Length')
        
        return self.rfile.read(int(body_length)).decode(encoding='utf8')

    def __send_text(self, text: str):
        text_bytes = text.encode(encoding='utf8')

        self.send_response(200)
        self.send_header("Content-Length", str(len(text_bytes)))
        self.send_header("Content-Type", "plain/text")
        self.end_headers()
        self.wfile.write(text_bytes)
