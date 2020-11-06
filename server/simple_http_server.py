
from server.base_http_server import BaseHTTPServer
import sys

class SimpleHTTPServer(BaseHTTPServer):

    def __init__(self, server_address, handler_class):
        self.server_name = 'SimpleHTTPServer'
        self.version = 'v0.1'
        BaseHTTPServer.__init__(self, server_address, handler_class)


if __name__ == '__main__':
    defaultport = 8888
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port >= 1024 and port <= 65535:
                defaultport = port
            else:
                print('port should great than 1024 but less then 65535')
                print('set deafult port 8888')
        except Exception as e:
            print('port set err',sys.argv[1])
            print('set deafult port 8888')
    from handler.simple_http_handler import SimpleHTTPRequestHandler

    SimpleHTTPServer(('127.0.0.1', defaultport), SimpleHTTPRequestHandler).serve_forever()
