from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import urllib.parse
import time
import io

import scrap 

HOST_NAME = ''
PORT_NUMBER = 9000

class ReportHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        parsed_url = urllib.parse.urlparse(self.path)
        if (parsed_url.path == '/report'):
            query = urllib.parse.parse_qs(parsed_url.query)
            report_name = query['name'][0]
            print(report_name)
            content = scrap.get_latest(report_name)
            if content is not None:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                self.wfile.write(b'\n')
                return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'\n')

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), ReportHandler)
    print(f"Server Starts - {HOST_NAME}:{PORT_NUMBER}, use <Ctrl-C> to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.shutdown()
    print(f"Server stopped")
