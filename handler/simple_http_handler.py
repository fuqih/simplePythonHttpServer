# -*- encoding=utf-8 -*-


import os
import json
import time
from urllib import parse

from handler.base_http_handler import BaseHTTPRequestHandler


RESOURCES_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                              '../resources')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, server, request, client_address):
        BaseHTTPRequestHandler.__init__(self, server, request, client_address)

    def do_GET(self):
        found, resource_path = self.get_resources(self.path)
        if not found:
            self.write_error(404)
            self.send()
        else:
            with open(resource_path, 'rb') as f:
                fs = os.fstat(f.fileno())
                # 文件的长度
                clength = str(fs[6])
                self.write_response(200)
                self.write_header('Content-Length', clength)
                # 避免跨域问题
                self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                                  (self.server.server_address[0], self.server.server_address[1]))
                self.end_headers()
                while True:
                    buf = f.read(1024)
                    if not buf:
                        break
                    self.write_content(buf)
                # self.send()

    def do_POST(self):
        # 从请求取出数据
        # tempdata = self.decode(self.body)
        # print(tempdata)
        # print("显示所有的headers")
        # print(self.headers)
        # for k, v in self.headers.items():
        #     print(k , v)

        # #如果这是一个文件上传请求
        # if 'uploadfilename' in self.headers:
        #     self.post_resources()
        # else:
        body=self.body
        if not body:
            body=r'{"msg":"no data in request body"}'
        body = json.loads(body)
        body['now servertime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print("一个post请求")
        response = json.dumps(body)
        # 组成应答报文
        self.write_response(200)
        self.write_header('Content-Length', len(response))
        self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                          (self.server.server_address[0], self.server.server_address[1]))
        self.end_headers()
        self.write_content(response)

    # 判断并获取资源
    def get_resources(self, path):
        resource_path = self.get_resource_path(path)
        abs_resource_path = os.path.join(RESOURCES_PATH, resource_path)
        if os.path.exists(abs_resource_path) and os.path.isfile(abs_resource_path):
            return True, abs_resource_path
        else:
            return False, abs_resource_path

    #解析路径
    def get_resource_path(self,path):
        url_result = parse.urlparse(path)
        resource_path = str(url_result[2])
        if resource_path.startswith('/'):
            resource_path = resource_path[1:]
        return resource_path

    # 从客户端上传资源
    # 根据Post请求的uploadfilename,targetpath字段创建文件
    def post_resources(self):
        filename = self.headers['uploadfilename']
        #相对资源目录
        resource_path = self.get_resource_path(self.path)
        #绝对资源目录
        abs_resource_path = os.path.join(RESOURCES_PATH, resource_path)
        # if not abs_resource_path.endswith("/"):
        #     abs_resource_path="%s/"%(abs_resource_path)
        #包括文件名的完整目录
        abs_file_path   = os.path.join(abs_resource_path, filename)
        print('上传文件目录:')
        print(resource_path,filename,abs_file_path)
        if os.path.isfile(abs_file_path):
            response = {'message': '上传路径已有文件', 'code': -1}
            self.write_response(404)
            response = json.dumps(response)
            self.write_header('Content-Length', len(response))
            self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                              (self.server.server_address[0], self.server.server_address[1]))
            self.end_headers()
            self.write_content(response)
        else:
            with open(abs_file_path,'wb') as f:
                print(type(self.body))
                f.write(self.encode(self.body))
            print("文件上传完成")
            response = {'message': 'file upload succeed', 'code': 0}
            self.write_response(200)
            response = json.dumps(response)
            self.write_header('Content-Length', len(response))
            self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                              (self.server.server_address[0], self.server.server_address[1]))
            self.end_headers()
            self.write_content(response)